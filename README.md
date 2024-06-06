# Code for submission_548

The code used in submission 548 is present in this project.
python 3.8


## CARLA
generate_scenario_data.py
connects to carla 0.9.15 docker
generates scenarios at four way junction on town 5
saves them as csv
relevant calls aus pycharm

## Scenariodatabase
sql database for scenarios

## Car model
simulates the car arriving at crossing fpr set of ego vehicles for each routing

## RSU model
consists of base model, localisation and transmission

rsu_local: sets a point for rsu and detects all objects in radius

rsu_transmission: mimics the transmission properties in the state chart

rsumodel: calls all relevant funcitons
## Signaling Model
gets all signals in a scenarios from files


## Utility scripts
read in data: adds scenarios from vsc. to sqlite db

## Visualizers
Visualizes the aggregated results from sqlite