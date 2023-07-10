# Covid19-Data-Visualisation

## Project Overview
For the MSc in Computing (Data Analytics) programme in I completed a Data Management and Visualisation Module.
As part of this module I had to complete a group project to explore, clean and visualise data on a particular topic.

For this project we chose to explore a Covid-19 dataset and achieved a grade of 100% on the assignment.

## Project Outline

### Python
Using the following packages we explored, cleaned and visualised the datasets:
* pandas
* datetime
* scipy
* matplotlib
* plotly

#### Populate the csv folder:
1. Go to https://health.google.com/covid-19/open-data/raw-data
2. Download: demographic.csv , econmony.csv, epidemiology.csv , index.csv. vaccinations.csv
3. Add all .csv files to the csv folder

#### How to generate the graph:
```
git clone https://github.com/AaronNolan/Covid19-Data-Visualisation.git
cd ca682-data-visualisation-project
pip3 install -r requirements.txt
cd python
python3 graph.py
python3 gdp_effectiveness.py
```

### Documentation
The pdf details the data used, the cleaning done and the visualisations made as well as justifications