# Weather ETL Pipeline with Airflow

This project implements an ETL (Extract, Transform, Load) pipeline that fetches weather data from the Open Meteo API for London and stores it in a PostgreSQL database using Apache Airflow.

## Project Structure
```
Airflow and Astro/
├── dags/
│   └── etlweather.py
└── docker-compose.yml
```

## Prerequisites
- Docker Desktop
- Astro CLI
- Python 3.x

## Setup and Installation

1. **Install Astro CLI**
```bash
curl -sSL install.astronomer.io | sudo bash
```

2. **Initialize the Project**
```bash
# Initialize a new Astro project
astro dev init
```

3. **Configure Connections**
After starting Airflow, set up these connections in the Airflow UI:
- `postgres_default`: PostgreSQL connection
- `open_meteo_api`: HTTP connection to Open Meteo API

## Running the Project

1. **Start the Project**
```bash
# Start all services
astro dev start

# View running containers
astro dev ps

# View logs
astro dev logs
```
![AstroDevStart]([images\astroDevStart.png](https://github.com/hrishikesh26/Astro_Airflow_Postgres_ETL/blob/main/images/astroDevStart.png))

### Image Description

The image shows a terminal window with a series of commands and outputs related to starting an Airflow project using Astro. The commands and outputs are as follows:

1. The command `astro dev start` is executed in the directory `C:\Users\hrish\Desktop\temp\Airflow and Astro`.
2. The terminal outputs the following messages:
   - "Project image has been updated"
   - "Project started"
   - "Airflow UI: http://localhost:8080"
   - "Postgres Database: postgresql://localhost:5432/postgres"
   - "The default Postgres DB credentials are: postgres:postgres"

The prompt in the terminal indicates that the environment is named `astro-env` and the base environment is active.

1. **Stop the Project**
```bash
astro dev stop
```

1. **Rebuild after Changes**
```bash
astro dev restart
```

## Project Components

### ETL Pipeline
- **Extract**: Fetches weather data from Open Meteo API for London
- **Transform**: Processes the raw weather data into structured format
- **Load**: Stores the transformed data in PostgreSQL database

![AriflowDash]([images\airflow_success_dash.png](https://github.com/hrishikesh26/Astro_Airflow_Postgres_ETL/blob/main/images/airflow_success_dash.png))

This snapshot demonstrates successfull running of the ETL pipline after setting up the connections.

### DAG Details
- DAG ID: `weather_etl_pipeline`
- Schedule: Daily
- Tasks:
  - `extract_weather_data`
  - `transform_weather_data`
  - `load_weather_data`

### Database Schema
```sql
CREATE TABLE weather_data (
    latitude FLOAT,
    longitude FLOAT,
    temperature FLOAT,
    windspeed FLOAT,
    weathercode INT,
    winddirection INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Docker Configuration
The project uses Docker Compose with two main services:
1. **Airflow**: Managed by Astro CLI
2. **PostgreSQL**: Runs on port 5432
   
![PostgresDockerContainer]([images\postgresdocker.png](https://github.com/hrishikesh26/Astro_Airflow_Postgres_ETL/blob/main/images/postgresdocker.png))

## Monitoring
- Access Airflow UI: `http://localhost:8080`
- Default credentials:
  - Username: `admin`
  - Password: `admin`

## Troubleshooting
If the DAG doesn't appear in the UI:
```bash
# Check logs for errors
astro dev logs

# Restart the environment
astro dev restart
```

## Postgres Database
This particular snapshot shows how the database is constantly updated with manual and scheduled triggers. I used DBviewer to setup postgres environment as database to view the transformed data. 
### Why Docker Includes PostgreSQL:
- *Airflow Uses PostgreSQL as Metadata Storage* – Airflow needs a database to store metadata like DAG runs, task instances, logs, and configurations. Many Airflow setups include PostgreSQL or MySQL for this purpose.
- *Dockerized Environments Are Isolated* – If you're running Airflow in Docker, it likely spun up a PostgreSQL container as part of the Astro dev setup, which helps keep all dependencies self-contained.

![PostgresDatabase]([images\dbviewer.png](https://github.com/hrishikesh26/Astro_Airflow_Postgres_ETL/blob/main/images/dbviewer.png))
>>>>>>> 47fd663 (initil commit: Adding my ETL project)
