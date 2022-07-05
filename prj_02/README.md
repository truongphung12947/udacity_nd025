# Disaster Response Pipeline

## Project Motivation

This project (Disaster Response Pipeline) is part of the Udacity Data Scientists Nanodegree Program. This project has provided enough dataset and some examples/code structure for me to deploy an ML pipeline from ETL, train a model and create a Web Interface for non-technical users to classify messages based on their content if there is a disaster in the message context. Through machine learning in real life, this project aims to classify messages sent by people who need help when a disaster happens. Every day there are numerous text, and chat via multiple messaging platforms, in order to classify this big data set will need many people to work for hours to know where or what happened in the message context to decide should they send help or not, all can be reduced by using ML technique, given output in seconds and send to local authorities or any agency for humanitarian assistance and disaster response

## Installation
This project require to install libraries
1. numpy
2. pandas
3. sklearn
4. nltk (with custom downloader)
5. sqlalchemy
6. flask
7. plotly

All installed version and dependencies can be found in requirements.txt

## Project Description
1. **ETL Pipeline**
- Loads the messages and categories datasets
- Merges the two datasets
- Cleans the data
- Stores it in a SQLite database

2. **ML Pipeline**
- Loads data from the SQLite database
- Splits the dataset into training and test sets
- Builds a text processing and machine learning pipeline
- Trains and tunes a model using GridSearchCV
- Outputs results on the test set
- Exports the final model as a pickle file

3. **Flask Web App**
- The web app also contains some visualizations that describe the data and input form for classification.

## File Descriptions
~~~~~~~
- app
    | - template
    | |- master.html  # main page of web app
    | |- go.html  # classification result page of web app
    |- run.py  # Flask file that runs app

- data
    |- disaster_categories.csv  # data to process 
    |- disaster_messages.csv  # data to process
    |- process_data.py
    |- InsertDatabaseName.db   # database to save clean data to

- models
    |- train_classifier.py
    |- classifier.pkl  # saved model 

- prep (for those who want to read researching process)
    |- categories.csv
    |- messages.csv
    |- classifier.pkl
    |- DisasterResponse.db
    |- etl_pipeline_preparation.ipynb
    |- ml_pipeline_preparation.ipynb
    
- requirements.txt
- README.md
~~~~~~~
## How to run

1. Run data/process_data.py to generate SQLite Database with cleaned data\
`python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db`
2. Run models/train_classifier.py to train and save model to file .pkl\
`python train_classifier.py DisasterResponse.db classifier.pkl`
3. Run python run.py in /app to start webapp and start to explore
