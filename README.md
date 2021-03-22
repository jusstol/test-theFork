# TheFork technical interview
![](https://img.shields.io/badge/language-python-brightgreen)
![](https://img.shields.io/badge/version-1.0-blue)
![](https://img.shields.io/badge/interview-technical_test-important)

## Prerequisite
You must have Docker with Docker Compose installed on your machine.

## How to setup
Once you have cloned this repository, make sure you are in its root directory and run the following command to install the project :

```bash
make build
```

That's it. The docker compose process will pull two images and create a network of two containers (it takes about 5min to complete).

## What is created
The project and its two containers look like this :

```text
name: python                                name: database
+-------------------------+                 +--------------------+
|                         |     INSERT      |                    |
|      Supervisord        +---------------->+                    |
|                         |                 |                    |
|           +             |                 |    PostgresSQL     |
|                         |     SELECT      |      database      |
|    Jupyter Notebooks    +---------------->+                    |
|                         |                 |                    |
+-------------------------+                 +--------------------+
FROM : continuumio/miniconda3:latest        FROM: postgres:latest
```

Two exposed WEB UIs from the `python` container :  
 * (9001) Supervisor : a process control system where one service equals one Python process
 * (8888) Jupyter Notebooks : two notebooks are availaible in this project

One exposed relational database from the `database` container.
 * (5432) MySQL : open source, reliability, feature robustness, and performance

## How to use the pipeline
1. Connect to Jupyter Notebook (http://localhost:8888)

To connect to Jupyter Notebooks you need to use a token that has been displayed
close to the end of the installation process. Look for something like this :

```text
python_1    |     To access the notebook, open this file in a browser:
python_1    |         file:///root/.local/share/jupyter/runtime/nbserver-12-open.html
python_1    |     Or copy and paste one of these URLs:
python_1    |         http://bfd65f6da6fe:8888/?token=5c201b6cc74e67bf3f464f23ecc333c2f9f4cc416d856967
python_1    |      or http://127.0.0.1:8888/?token=5c201b6cc74e67bf3f464f23ecc333c2f9f4cc416d856967
```

Copy the long hash after `token=` and paste it into Jupyter Notebooks UI.

2. Open the first notebook called _1\_check\_database.ipnyb_
3. Run all cells (click Cell / Run all)

You should see errors telling you that the table does not exist. That's normal, you will know push data and 
start the pipeline.

4. Move your CSV file (bookings.csv) into ./data/in
5. Go to Supervisor (http://localhost:9001) and click `RESTART ALL` to start all steps of the pipeline.
6. They will all start after one minute. You can read log messages in the ./log directory that has been created
7. Once all jobs are finished, you can take a look at the ./data/out folder to find the _monthly\_restaurants\_report.csv_ file
8. Go back to Jupyter on the _1\_check\_database.ipnyb_ notebook
9. Re run all cells. You should see 5 lines extracted from the the `monthly_restaurants_report` table to prove we can query the database.
10. You can now open the second notebook called _2\_data\_analysis.ipnyb_, run all cells and read the small analysis.

## Python code structure
The structure of the code is made in an evolutionary way. It is easily possible to add a new pipeline 
in `jobs` as long as it has a `run()` function with the correct arguments. For each pipeline, it is possible 
to configure the execution frequency, the name of the file accepted as input or where to output data.

```text
src
├── conf
│   ├── __init__.py
│   ├── config.py           <- pipelines settings
│   └── env.py              <- environment variables
├── jobs                    <- each module in job is an independant "pipepline"
│   ├── __init__.py
│   ├── compute_monthly_report.py
│   └── insert_monthly_report.py
├── main.py                 <- entrypoint
├── sql
│   ├── __init__.py
│   └── db.py               <- connection to "gensdeconfiance" database
└── utils                   <- package for all sorts of utilities
    ├── __init__.py
    └── fs.py               <- functions to interract with the file system
```

Everything related to the environment is variabilized and can be set in the _./env.conf_ file.

## Unit tests
To run all unit tests, the best is to create a virtual environment in which you can install all needed dependencies. Make sure you have `python3` on your machine.

Create the virtual environment with the following command :

```bash
make tests-env
```

Run all tests with :

```bash
make tests
```

## What or how to improve
To make this project even more production-ready, we could :
 * package the Python code into Python library (wheel)
 * manually create the table in the database and not infer their schemas from Pandas DataFrame.
 * catch more errors when parsing input files in case we receive a file having wrong column names for example
 * add CI/CD to build, test, anylize quality and deploy automatically (ex: Jenkins + SonarQube + Ansible)
 * improve logs readability (ex: Elastic Filebeat + Kibana)
 * monitor disk space usage and RAM
 * alert by mail or any webhook when a pipeline is down (Supervisor event listener)
 * remove input files instead of moving them (clean disk space)
 * add a Sphinx documentation
 * replace most of the Python + Supervisor logic by Apache Nifi for less code and more robustness

## How to clean
To remove all created container, hit Ctrl+C in the terminal window where you started the docker-compose, and run the following command :

```bash
docker-compose down
```

Manually remove the project images :

```bash
docker image rm test-thefork_python postgres continuumio/miniconda3
```
