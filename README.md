# MingmanYuan_Final_Project

## Project Overview

This project is aimed to


## About H1-B

The H1B is an employment-based, non-immigrant visa category for temporary foreign workers in the United States.For a foreign national to apply for H1B visa, an US employer must offer a job and petition for H1B visa with the US immigration department.This is the most common visa status applied for and held by international students once they complete college/ higher education (Masters, Ph.D.) and work in a full-time position.

## Input Datasets

### H1B data

Annual data provided by the office of foreign labor of the US Department of labor. This disclosure data consists of selected information extracted from nonimmigrant and immigrant application tables within the Office of Foreign Labor Certification's case management systems. The data sets are available in the Microsoft Excel (.xlsx) file format and organized by the federal fiscal year (October 1 through September 30).

#### Data Source

For detailed information of this dataset, refer to: 
https://www.dol.gov/agencies/eta/foreign-labor/performance

#### Variables

I dowloaded the H1B disclosure data of 2016 and 2018 by using their respective urls in my code. These two datasets are in the same struture, and the primary key of each dataset is CASE_NUMber. Other important variables include CASE_STATUS, JOB_TITLE, EMPLOYER_STATE, WORKSITE_STATE, PREVAILING_WAGE and etc.

### American Community Survey(ACS) data

The American Community Survey (ACS) is an annual survey taken by the U.S. Census Bureau.ACS data provides information about jobs and occupations, educational attainment, veterans, whether people own or rent their homes, and other topics. The ACS data are released in two waves each year. The first wave released is the 1-year dataset which includes geographic areas with populations of 65,000 or more. The second wave is the 5-year dataset (combining 5 years of survey data) which includes all geographic areas down to the block group level. In this project, I chose the 1-year dataset.

#### Data Source

For detailed information of this dataset, refer to: 
https://www.census.gov/programs-surveys/acs/data/summary-file.html


#### Variables

ACS Data collected incudes social, economic, housing and population data. For detailed explanation of all variables, refer to https://api.census.gov/data/2015/acs/acs1/subject/variables. In this project, I'd like to know the education level distribution among the immgragtion population of each state for two indiviudal year - 2016 and 2018, therefore I have extracted five variables from two yearly (2015 and 2017) state datasets, including  B07009_036E, B07009_035E, B07009_034E, B07009_033E, B07009_032E - indicating in that year the percentage of immigration population of each state who have obtained Graduate or professional degree, Bachelor's degree, Some college or associate's degree, High school graduate (includes equivalency) and Less than high school graduate accordingly.

### State Tech and Science Index data

#### Data Source

#### Variables

### State Geo Data

#### Data Source

#### Variables

## Final Clean Datasets

## Self-defined Funcions

## Data Pre-processing

## Modeling

### Modeling result

### 






