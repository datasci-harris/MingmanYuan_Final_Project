import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from bs4 import BeautifulSoup
import urllib.request as urllib2
import requests
import censusdata


path = os.getcwd()


def getFile(url, filename, path):
    response = requests.get(url)
    with open(os.path.join(path, filename), 'wb') as ofile:
        ofile.write(response.content)


def getH1B(file_name):
    base = 'https://www.dol.gov'
    base_url = 'https://www.dol.gov/agencies/eta/foreign-labor/performance'
    html_page = urllib2.urlopen(base_url)
    soup = BeautifulSoup(html_page)
    file_link = ''
    for link in soup.findAll('a'):
        if file_name in link.text:
            file_link = base + link.get('href')
    global path
    getFile(file_link, file_name, path)


getH1B('H-1B FY2018.xlsx')
getH1B('H1B FY2016.xlsx')


def getTechIndex(filename):
    TechIndex = []
    for i in range(len(filename)):
        state_tech_and_science_org_url = 'http://statetechandscience.org/statetech.taf?page=overall-ranking&composite=tswf'
        html = urllib2.urlopen(state_tech_and_science_org_url).read()
        soup = BeautifulSoup(html)
    #  soup.find_all("table") will return a result set containing bs4.elements
    # When the index equal to 2, the function would extract data of Year 2018, which is inserted as the second element of bs4.element result set
    # When the index equal to 3, the function would extract data of Year 2016, which is inserted as the third element of bs4.element result set
        TechIndex1yr = soup.find_all("table")[i+2]
        state_index = []
    # each row of table2018/2016 is inserted in 'tr' tags
        for state_row in TechIndex1yr.findAll('tr'):
            # each cell of one particular row is inserted in 'td' tags, and created a new set columns to store values of all cell
            values = state_row.findAll('td')
            state_index_set = []
            for value in values:
                # store each element in the set columns in the new list output_row
                state_index_set.append(value.text)
            state_index.append(state_index_set)
        TechIndex.append(state_index)
    for m, n in zip(range(len(TechIndex)), range(len(filename))):
        global path
        with open(os.path.join(path, filename[n]), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(TechIndex[m])


getTechIndex(['State Technology and Sciencxe Index Y2018.csv',
              'State Technology and Sciencxe Index Y2016.csv'])


def downloadCensus(vars):
    # Dowload Year 2017 data from American Community Census website throught the official API
    # Since the H1b filings disclosed in Year2018 contains
    # Call this function while downloading Censusdata
    statedata = []
    for i in range(len([2017, 2015])):
        statedata.append(censusdata.download(
            'acs1', [2017, 2015][i], censusdata.censusgeo([('state', '*')]), vars))
    return statedata


statedata = downloadCensus(
    ['B07009_036E', 'B07009_035E', 'B07009_034E', 'B07009_033E', 'B07009_032E'])
# Variables' meaning refers to "https://api.census.gov/data/2015/acs/acs1/subject/variables"
# B07009_036E Moved from abroad!!Graduate or professional degree
# B07009_035E Moved from abroad!!Bachelor's degree
# B07009_034E Moved from abroad!!Some college or associate's degree
# B07009_033E Moved from abroad!!High school graduate (includes equivalency)
# B07009_032E Moved from abroad!!Less than high school graduate


def cleanCensus(statedata):
    # Convert the original state name format to plain text
    # Call this function after dowloading Census Data - downloadCensus()
    for i in range(len(statedata)):
        new_indices = []
        state = []
        for index in statedata[i].index.tolist():
            new_index = index.geo[0][1]
            new_indices.append(new_index)
            state_name = index.name
            state.append(state_name)
        statedata[i].index = new_indices
        statedata[i]['state'] = state
    return statedata
# Cite "https://towardsdatascience.com/mapping-us-census-data-with-python-607df3de4b9c"


statedata = cleanCensus(statedata)


def resetCensus(statedata, reset_ls):
    # Rename each column in Censusdata
    # Call this function after cleaning Census data - cleanCensus()
    for i in range(len(statedata)):
        column_list = statedata[i].columns
        for n, m in zip(range(len(column_list)), range(len(reset_ls))):
            statedata[i] = statedata[i].rename(columns={column_list[n]: reset_ls[m]})
    return statedata


reset_ls = ['move_from_abroad_Graduate_professional_degree_population_size',
            'move_from_abroad_Bachelor_degree_population_size',
            'move_from_abroad_college_associate_degree_population_size',
            'move_from_abroad_high_school_degree_population_size',
            'move_from_abroad_less_than_high_school_degree_population_size']
statedata = resetCensus(statedata, reset_ls)


def derivedColumns(statedata):
    # Call this function to creat new features based on existing features, after merting two tables together - mergeStateVote()
    for i in range(len(statedata)):
        # Create a new feature called 'total_move_from_abroad'
        statedata[i]['total_move_from_abroad'] = statedata[i].iloc[:, 0]+statedata[i].iloc[:, 1] + \
            statedata[i].iloc[:, 2]+statedata[i].iloc[:, 3] + \
            statedata[i].iloc[:, 4]
        # Create a new feature called 'percent_move_from_abroad_above_college_degree'
        statedata[i]['percent_move_from_abroad_above_college_degree'] = (
            statedata[i].iloc[:, 0]+statedata[i].iloc[:, 1])/statedata[i]['total_move_from_abroad']*100
        # Drop features that we no long need
        statedata[i] = statedata[i].drop(['move_from_abroad_Graduate_professional_degree_population_size',
                                          'move_from_abroad_Bachelor_degree_population_size',
                                          'move_from_abroad_college_associate_degree_population_size',
                                          'move_from_abroad_high_school_degree_population_size',
                                          'move_from_abroad_less_than_high_school_degree_population_size',
                                          'total_move_from_abroad'], axis=1)
        # Since we only extract one year data, meaning the length of statedata is 1.
        # Therefore we could store statedata[i] by statedata directly.
        return statedata


statedata = derivedColumns(statedata)
statedata[0].to_csv('2017_Census_State_data.csv', index=False)
statedata[1].to_csv('2015_Census_State_data.csv', index=False)
