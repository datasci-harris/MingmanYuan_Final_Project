# MingmanYuan_Final_Project

## Project Overview

This project performs basic explortary analysis on H1B visa cases in year 2016 and 2018, and try to build a model to predict the number of H1B visa cases in one year in the future. 

## About H1-B

The H1B is an employment-based, non-immigrant visa category for temporary foreign workers in the United States.For a foreign national to apply for H1B visa, an US employer must offer a job and petition for H1B visa with the US immigration department.This is the most common visa status applied for and held by international students once they complete college/ higher education (Masters, Ph.D.) and work in a full-time position.

## Input Datasets

### H1B data

Annual data provided by the office of foreign labor of the US Department of labor. This disclosure data consists of selected information extracted from nonimmigrant and immigrant application tables within the Office of Foreign Labor Certification's case management systems. The data sets are available in the Microsoft Excel (.xlsx) file format and organized by the federal fiscal year (October 1 through September 30). I dowloaded the H1B disclosure data of 2016 and 2018 by using their respective urls, and save them as excel files in the repo.

Note that the original downloaded H1B dataset for one year is around 250 MB, containing more than 65000+ rows. Though I've saved them as excel files in repo, it is quite time consuming to read the excel file, and I was unable to push these two files to github(without using Github LFS). For grading convenience, I save the subset dataset for each year as another two csv files (decreasing the file size to MB) - only contain variables used later. Therefore I would recommend reading the subset data files direcly once it takes long time to read the original H1B file on your computer. To do this, please comment out the data downloading code, download the 'H-1B FY2018 Sub.csv' and 'H-1B FY2016 Sub.csv', and then run codes in line100 and line 101.

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

This dataset is Geopandas Geodataframe. And two most important vairbales used later to merge two Geodataframes (via geopandas.sjoin) is State name(STUSPS) and Geometry.

### State Longitude and Latitude Data

To add the second layer in my spacial data plot, the longitude and latitude for each state is required. Therefore I built a web scraper via Beautiful Soup, and parsed the HTML to pick out the tables provided by google development that contains the geographic information of each state.

#### Data Soucre

For detailed information of this dataset, refer to: 
https://developers.google.com/public-data/docs/canonical/states_csv

#### Variables

The structure of this data is also clean - only contains the longtitude and latitude of each state.

## Final Clean Datasets

After merging H1B data, STSI data and ACS data by the key State Abbreviation, there are two final clean datasets - one for year 2016 and one for year 2018. Later I would use data for year 2016 as the training set, and data for 2018 as the tesing set. These two datasets have the exactly same strucutre, and the primary key of each is the state name. Each dataset has 50 rows (50 states) and six columns (H1B_Employer_Number, H1B_Average_Wage, TechSciScore, percent_move_from_abroad_above_college_degree, H1B_Case_Number and H1B_Case_Number_Percent). The last variable will be the target variable in the modeling part, and the first five variables are features.

## Self-defined Funcions

This session lists all the functions that I defined in this project, and gives brief introduction of the parameters and expected output of each function.

### Data Acquiring

#### getFile(url, filename, path)

Call this function within the function getH1B(file_name).

#### getH1B(file_name)

Call this function to download H1B data by url and save the file 'file_name' in the repo.

#### subH1B(dt)

Call this function to subset the original downloaded H1B data, aimed to keep variables that relevant to this project and shrink the data file size.

#### loadStateH1B(filename)

Call this function to read H1B subset data, rename the column name and do some aggregated calculation on case-level data. The output is a new dataframe based on state level.

#### getTechIndex(filename)

Call this function to dowload the STSI data on state level by parsing HTML, and save the file 'filename' in the repo.

#### downloadCensus(vars)

Dowload ACS data from American Community Census website throught the official API, and only extracted variables 'vars' from the whole official dataset.

#### storeStateCensus(statedata, filename)

Call this function to store the clean state census data 'statedata'as the file 'filename' in the repo.

#### getStatesLoc(filename)

Call this function to download the latitude and longitude of each US state, and save a csv file named 'filename' in the repo.

#### loadStateLoc(filename)

Call this function to read the State Locatoion.csv file into a clean dataframe

#### readZippedFile(url)

Call this function to download the USA States Choropleth data from 'url', unzip the zipped file, read .shp file and return a dataframe contains State geographic information.

### Data Pre-processing

#### cleanStateTech16(StateTech16)

Call this function to clean the whitespace in all cells of the feature State.

#### cleanStateTech(StateDT)

Call this function to transform the state names to state abbreviations for later merge.

#### cleanCensus(statedata)

Call this function to convert the original state name format to plain text.

#### resetCensus(statedata, reset_ls)

Call this function to rename each column in data 'statedate' by iterating the new column name list 'reset_ls'.

#### derivedColumns(statedata)

Call this function to creat new features based on existing features

### Plotting
 
#### mergeAll(StateH1B_agg, StateTech, StateCensus, StateLoc)

Call this function to merge four seperate clean data tables for each year together - the State Cencus data, the State Tech and Science Index data, the State Location data and the State H1B data.

#### plotMerge(Merge18, StateGeo)

Call this function to plot color code each US State's H1B filings on US map for year2018.

### Modeling

#### scaleMerge(Merge1, Merge2, scale_lst)

Call this funtion to rename columns names in two datasets Merge1 and Merge2, and conduct standarization on Merge2, the training data set for better modeling.

#### splitMerge(Merge1, Merge2)

Call this function to define the training and test datasets.

#### model(models)

Use four different algorithms to do modeling, and return the accuracy score to quantify the prediction quality.

## Modeling result








