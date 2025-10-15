# Airflow example

This repository contains an example of using Airflow to do the following process:

* Create a table in a PostgreSQL database
* Check if an API is available (https://jsonplaceholder.typicode.com/users)
* Obtain user data from the API
* Save the user data in the PostgreeSQL database

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (choose based on your OS):
  - [Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [macOS (Intel/Apple Silicon)](https://docs.docker.com/desktop/install/mac-install/)
  - [Linux (Docker Engine)](https://docs.docker.com/engine/install/)

- [Docker Engine](https://docs.docker.com/engine/) (for Linux-based systems)

- [UV (optional)](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)



## Steps to run the project


### Create virtual environment

´´´bash
uv venv --python 3.11
´´´


### Activate virtual environment

#### macOS/Linux:
´´´bash
source .venv/bin/activate
´´´

#### Windows (PowerShell):
´´´bash
.venv\Scripts\Activate.ps1
´´´


### Install Apache Airflow

´´´bash
uv pip install apache-airflow==3.0.0
´´´


### Run the project

´´´bash
docker compose up
´´´

After that you'll be able to access Airflow in your browser [Here](localhost:8080/), and you'll see a login screen, so to access the main Airflow dashboard type the default credentials:

* user: airflow
* password: airflow

You´ll have to add the postgre connection through the Airflow web UI.


## Providers for Airflow

You can find providers to install [Here](https://registry.astronomer.io/providers) if you need to interact with other services, and set the connections in Airflow. For this example, you need Redshift SQL Hook provider, for installing it, run the following command

´´´bash
uv pip install apache-airflow-providers-postgres==6.1.3
´´´


## Test a task

To test a task without running an entire DAG and saving the run metadata, go to the scheduler container and execute:

´´´bash
bin/bash
airwflow tasks test <task_name> <task_id>
´´´