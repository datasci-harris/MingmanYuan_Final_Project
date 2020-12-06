# MingmanYuan_Final_Project

## Project Overview

This project is aimed to


## About H1-B

The H1B is an employment-based, non-immigrant visa category for temporary foreign workers in the United States.For a foreign national to apply for H1B visa, an US employer must offer a job and petition for H1B visa with the US immigration department.This is the most common visa status applied for and held by international students once they complete college/ higher education (Masters, Ph.D.) and work in a full-time position.

## Input Datasets

### H1B data

Annual data provided by the office of foreign labor of the US Department of labor. This disclosure data consists of selected information extracted from nonimmigrant and immigrant application tables within the Office of Foreign Labor Certification's case management systems. The data sets are available in the Microsoft Excel (.xlsx) file format and organized by the federal fiscal year (October 1 through September 30). I dowloaded the H1B disclosure data of 2016 and 2018 by using their respective urls, and save them as excel files in the repo.

Note that the original downloaded H1B dataset for one year is around 250 MB, containing more than 65000+ rows. Though I've saved them as excel files in repo, it is quite time consuming to read the excel file. For grading convenience, I save the subset dataset for each year as another two csv files (decreasing the file size to MB) - only contain variables used later, and read them direcly. To avoid repetition, I commented out the data download code, but feel free to run the download code and read the original files if you want!

#### Data Source

For detailed information of this dataset, refer to: 
https://www.dol.gov/agencies/eta/foreign-labor/performance

#### Variables

These two datasets are in the same struture, and the primary key of each dataset is CASE_NUMber. Other important variables include CASE_STATUS, JOB_TITLE, EMPLOYER_STATE, WORKSITE_STATE, PREVAILING_WAGE and etc.

### American Community Survey(ACS) data

The American Community Survey (ACS) is an annual survey taken by the U.S. Census Bureau.ACS data provides information about jobs and occupations, educational attainment, veterans, whether people own or rent their homes, and other topics. The ACS data are released in two waves each year. The first wave released is the 1-year dataset which includes geographic areas with populations of 65,000 or more. The second wave is the 5-year dataset (combining 5 years of survey data) which includes all geographic areas down to the block group level. In this project, I chose the 1-year dataset.

#### Data Source

For detailed information of this dataset, refer to: 
https://www.census.gov/programs-surveys/acs/data/summary-file.html


#### Variables

ACS Data collected incudes social, economic, housing and population data. For detailed explanation of all variables, refer to https://api.census.gov/data/2015/acs/acs1/subject/variables. In this project, I'd like to know the education level distribution among the immgragtion population of each state for two indiviudal year - 2016 and 2018, therefore I have extracted five variables from two yearly (2015 and 2017) state datasets, including  B07009_036E, B07009_035E, B07009_034E, B07009_033E, B07009_032E - indicating in that year the percentage of immigration population of each state who have obtained Graduate or professional degree, Bachelor's degree, Some college or associate's degree, High school graduate (includes equivalency) and Less than high school graduate accordingly.

### State Tech and Science Index data

The State Technology and Science Index (STSI) provides a benchmark for evaluating the knowledge economies of all 50 US states, and presents a snapshot of how state-level science and technology economies compare to one another at a specific time. And STSI is provided annually by The Milken Institute, a nonprofit, nonpartisan think tank. In this project, I chose the sub-index, Technology and Science Workforce (TSW) of STSI to indicate whether states have sufficient depth of high-caliber technical talent, represented by the share of workers in a particular field relative to total state employment. I built a web scraper via Beautiful Soup, and parsed the HTML to pick out the data tables of year 2018 and 2016.

#### Data Source

For detailed information of this dataset, refer to: 
http://statetechandscience.org/statetech.html

#### Variables

The structure of TSW is relatively simple comparing to the two previous datasets. STSI of each year only includes three variables, namely State, Rank and Score.

### State Geo Data

To add the base layer in my spacial data plot, I downloaded the USA state choropleth data using the url provided by the Census Bereau. And I extracted and read the shape file(.shp) among the downloaded zipped file folder by python programming. 

#### Data Source

For detailed information of this dataset, refer to: 
https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

#### Variables

This dataset is pandas Geo dataframe. And

### State Longitude and Latitude Data

To add the second layer in my spacial data plot, I need to first add longitude and latitude for each state, combine them as geo points and then 

#### Data Soucre

#### Variables

## Final Clean Datasets

## Self-defined Funcions

## Data Pre-processing

## Modeling

### Modeling result

### 






