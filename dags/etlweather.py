from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import dag
from datetime import datetime, timedelta
from airflow.utils import timezone

# location for the weather data from london
Latitude = '51.5074'
Longitude = '-0.1278'

POSTGRESS_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # use UTC now minus 1 day
    "start_date": timezone.utcnow() - timedelta(days=1),
}


# # DAG
# @dag(
#     dag_id='weather_etl_pipeline',
#     default_args=default_args,
#     schedule='@daily',
#     catchup=False)

@task
def extract_weather_data():
    """
    Extracts weather data from the Open Meteo API for London.
    """

    # Use the HttpHook to make a GET request to the Open Meteo API
    # and retrieve the weather data for London.
    # The API returns a JSON response containing hourly temperature data.
    # The HttpHook is configured with the connection ID 'open_meteo_api'.
    # The latitude and longitude for London are hardcoded as '51.5074' and '-0.1278', respectively.
    # The URL for the API request is constructed using these coordinates.
    http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')    
    # url = f'https://api.open-meteo.com/{endpoint}'
    # The endpoint is constructed using the latitude and longitude of London.
    endpoint = f'v1/forecast?latitude={Latitude}&longitude={Longitude}&current_weather=true'
    # Make the GET request to the Open Meteo API using the HttpHook.
    response = http_hook.run(endpoint)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Open Meteo API: {response.status_code}")
    return response.json()

@task
def transform_weather_data(weather_data):
    """
    Transforms the weather data to extract relevant information.
    """
    current_weather = weather_data['current_weather']
    transformed_data = {
        'latitude': Latitude,
        'longitude': Longitude,
        'temperature': current_weather['temperature'],
        'windspeed': current_weather['windspeed'],
        'weathercode': current_weather['weathercode'],
        'winddirection': current_weather['winddirection'],
    }
    return transformed_data

@task
def load_weather_data(transformed_data):
    """
    Loads the transformed weather data into a PostgreSQL database.
    """
    # Use the PostgresHook to insert the transformed data into the database.
    pg_hook = PostgresHook(postgres_conn_id=POSTGRESS_CONN_ID)
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # create table if it does not exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            weathercode INT,
            winddirection INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    # Insert the transformed data into the weather_data table.

    insert_query = """
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, weathercode, winddirection)
        VALUES (%s, %s, %s, %s, %s, %s);"""
    cursor.execute(insert_query, (
        transformed_data['latitude'],
        transformed_data['longitude'],
        transformed_data['temperature'],
        transformed_data['windspeed'],
        transformed_data['weathercode'],
        transformed_data['winddirection']
    ))
    conn.commit()
    cursor.close()  

@dag(
    dag_id='weather_etl_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False
)
def weather_etl_pipeline():
    """This function *is* your DAG; tasks get bound here."""
    raw = extract_weather_data()
    transformed = transform_weather_data(raw)
    load_weather_data(transformed)

# actually create the DAG object for Airflow to discover
dag = weather_etl_pipeline()