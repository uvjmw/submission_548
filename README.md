# Code for submission 548

This project contains the code used for Submission 548. The codebase leverages Python 3.8 and Python 3.10 for different
components of the project. The primary focus of this project is to generate scenario data using the CARLA simulator,
which is executed within a Docker container.

### Requirements:

+ Python 3.8: Used for CARLA-related scripts and running CARLA in Docker.
+ Python 3.10: Used for all other packages and scripts.

### Installation

To install the required packages for this project, use the requirements.txt files located in the respective directories.
Install the dependencies using the following commands:

    pip install -r /requirements.txt

## CARLA

Ensure that Docker is installed and properly configured on your system.
For more detailed information on running CARLA in Docker, refer to
the [CARLA Docker documentation](https://carla.readthedocs.io/en/0.9.15/build_docker/).

The CARLA simulator is used to generate scenario data. The specific script and details are as follows:

Functionality:

+ Connects to CARLA version 0.9.15 running in a Docker container.
+ Generates scenarios at a four-way junction in Town 5.
+ Saves the generated scenarios as CSV files.

Execution:

+ Ensure that CARLA 0.9.15 Docker container is running.
+ Run the script from within an environment where CARLA is accessible.

Output:

+ .csv files containing the tracks of all objects for a given time on the specified intersection
+ .csv files containing all information from the traffic lights with the corresponding time signals

To run the script:

    python generate_scenario_data.py

The behavior of the script can be parameterized and modified using different command line options.
In the following the mandatory command line options for the scenario generation will be described:

* `--host`: Hostadress of the System running the CARLA Docker container.
* `-n`: Number of vehicles in the simulation
* `-w`: Number of walkers in the simulation.
* `--hero`: activating all objects in the simulation.

## Scenariodatabase

The database stores meta information(filepath, identifier, duration, ...)  about the scenarios used in this work.
The scenarios are stored in csv-files containing tracks of multiple objects.When communicating with the database,
the class in **DBController.py** is used. For extracting trajectory information from scenario files
**ScenarioGetter.py** is used.

## Car model

The car model simulates the behaviour and interaction between subsystems of the ego-vehicle for a given scenario at
the crossing. It it the main entry point for simulating the scenarios used in this paper.

To run the script:

    python CarModel.py

The behavior of the script can be parameterized and modified using different command line options.
In the following the mandatory command line options for the scenario generation will be described:

+ `--routing_id`: Database id of the routing for the ego-vehicle
* `--db-file`: Path to the sqlite database file
* `-dd`: Path to the directory holding the scenario files
* `-dds`: Path to the directory holding the signaling files

## RSU model

The RSU (Roadside Unit) model simulates the behavior of the roadside unit, which includes base functionaloity, localization, and
transmission functionalities. Below are the descriptions and usage instructions for each component of the RSU model:
Components

### RSULocalisation:
Sets a specific point for the RSU.
Detects all objects within a certain radius.

### RSUTransmission:
Mimics the transmission properties in the state chart.
Simulates the communication properties and processes.

### RSUModel:

Calls all relevant functions from rsu_local and rsu_transmission.
Integrates the localization and transmission functionalities.
This is the main script to run for simulating the complete RSU model.
To run the integrated RSU model:

    python RSUModel.py

The behavior of the script can be parameterized and modified using different command line options.
In the following the mandatory command line options for the scenario generation will be described:

* `--signal_group`: ID of the traffic signal relevant for the routing of the ego-vehicle


## Signaling Model
The Signaling Model retrieves the relevant traffic signals within a scenario. 

## Utility scripts and Visualizers
This section includes scripts designed for data handling and visualization purposes.

### Read in Data:
+ Adds scenarios from various sources into an SQLite database.
+ Ensures the data is structured and stored properly for further use in simulations and analysis.

### Visualizers:
+ Visualizes the aggregated results stored in the SQLite database.
+ Helps in understanding and analyzing the data through graphical representations, making it easier to interpret and draw insights from the simulation results.