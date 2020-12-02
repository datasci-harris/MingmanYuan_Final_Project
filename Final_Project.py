from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import zipfile
import io
from bs4 import BeautifulSoup
import urllib.request as urllib2
import requests
import censusdata
import geopandas
import sklearn.preprocessing as preprocessing


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

# The file 'H-1B FY2018.xlsx' is around 200 mb, which would take around 10 mins (~8 mins for 'H1B FY2016.xlsx')
# on my MacBook Air2020 to read, therefore I would not recommend reading this file directly. For grading purpose,
# I would suggest directly read the file 'H-1B FY2018 Sub.csv' which I have pre-stored in the repo. I also commented out
# the code (see below) which I have built and ran to transform the original data set to a smaller one. This subset H1b table only contains
# relevant columns that I would use later in the feature engineering and modeling process. And I apply this on H1B Y2016
# data as well.

# H1b2018 = pd.read_excel('H-1B FY2018.xlsx')
# H1b2016 = pd.read_excel('H1B FY2016.xlsx')


# def subH1B(dt):
#     dt = dt.loc[dt['CASE_STATUS'] == 'CERTIFIED'].filter(['CASE_NUMBER', 'EMPLOYER_NAME',
#                                                           'EMPLOYER_STATE', 'JOB_TITLE', 'SOC_CODE',
#                                                           'PREVAILING_WAGE', 'PW_UNIT_OF_PAY',
#                                                           'WORKSITE_STATE'], axis=1)
#     return dt


# H1b2018_sub = subH1B(H1b2018)
# H1b2018_sub.to_csv('H-1B FY2018 Sub.csv', index=False)

# H1b2016_sub = subH1B(H1b2016)
# H1b2016_sub.to_csv('H-1B FY2016 Sub.csv', index=False)


def loadStateH1B(filename):
    # filename 'H-1B FY2018 Sub.csv' and 'H-1B FY2016 Sub.csv'
    H1BDT = pd.read_csv(filename)
    H1BDT = H1BDT.dropna(axis=0, how='any')
    H1BDT['year'] = filename[7:11]
    H1BDT['Annual_Prevailing_Wage'] = 0
    H1BDT['Annual_Prevailing_Wage'] = np.where(H1BDT['PW_UNIT_OF_PAY'] == 'Year',
                                               H1BDT['PREVAILING_WAGE'], H1BDT['Annual_Prevailing_Wage'])
    H1BDT['Annual_Prevailing_Wage'] = np.where(H1BDT['PW_UNIT_OF_PAY'] == 'Hour', H1BDT['PREVAILING_WAGE']*2080,
                                               H1BDT['Annual_Prevailing_Wage'])
    H1BDT['Annual_Prevailing_Wage'] = np.where(H1BDT['PW_UNIT_OF_PAY'] == 'Week',
                                               H1BDT['PREVAILING_WAGE']*52, H1BDT['Annual_Prevailing_Wage'])
    H1BDT['Annual_Prevailing_Wage'] = np.where(H1BDT['PW_UNIT_OF_PAY'] == 'Month',
                                               H1BDT['PREVAILING_WAGE']*12, H1BDT['Annual_Prevailing_Wage'])
    H1BDT['Annual_Prevailing_Wage'] = np.where(H1BDT['PW_UNIT_OF_PAY'] == 'Bi-Weekly',
                                               H1BDT['PREVAILING_WAGE']*26, H1BDT['Annual_Prevailing_Wage'])

    H1BDT_agg1 = H1BDT.groupby(['WORKSITE_STATE']).agg(
        {'Annual_Prevailing_Wage': 'mean', 'CASE_NUMBER': 'count'})
    H1BDT_agg2 = H1BDT.groupby(['EMPLOYER_STATE']).agg({'EMPLOYER_STATE': 'count'})
    H1BDT_agg = H1BDT_agg1.merge(H1BDT_agg2, how='inner', left_on=[
                                 'WORKSITE_STATE'], right_on=H1BDT_agg2.index)
    H1BDT_agg = H1BDT_agg.rename(columns={'WORKSITE_STATE': 'StateAbb',
                                          'Annual_Prevailing_Wage': 'Avg_Annual_Prevailing_Wage',
                                          'EMPLOYER_STATE': 'Employer_Number'})
    return H1BDT_agg


StateH1B18 = loadStateH1B('H-1B FY2018 Sub.csv')
StateH1B16 = loadStateH1B('H-1B FY2016 Sub.csv')


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


def cleanStateTech16(StateTech16):
    # Call this function to clean the whitespace in all cells of the feature State
    # I did not define this function at first and until I got an error when I call the function mergeAll, one
    # lesson here is always check and clean your data after the download
    StateTech16['State'] = StateTech16['State'].str.strip()
    return StateTech16


StateTech18 = pd.read_csv('State Technology and Sciencxe Index Y2018.csv')
StateTech16 = pd.read_csv('State Technology and Sciencxe Index Y2016.csv')
StateTech16 = cleanStateTech16(StateTech16)


def cleanStateTech(StateDT):
    # Cite the dictionary from 'https://gist.github.com/rogerallen/1583593'
    # Call this function to transform the state names to state abbreviations for later merge
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }
    StateDT['abbrev'] = StateDT.State.replace(us_state_abbrev)
    return StateDT


StateTech18 = cleanStateTech(StateTech18)
StateTech16 = cleanStateTech(StateTech18)


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
        statedata[i] = statedata[i].rename(columns={'state': 'State'})
        # Since we only extract one year data, meaning the length of statedata is 1.
        # Therefore we could store statedata[i] by statedata directly.
    return statedata


def storeStateCensus(statedata, filename):
    statedata = derivedColumns(statedata)
    for m, n in zip(range(len(statedata)), range(len(filename))):
        statedata[m].to_csv(filename[n], index=False)


storeStateCensus(statedata, ['2017_Census_State_data.csv', '2015_Census_State_data.csv'])
StateCensus17 = pd.read_csv('2017_Census_State_data.csv')
StateCensus15 = pd.read_csv('2015_Census_State_data.csv')
StateCensus17 = cleanStateTech(StateCensus17)
StateCensus15 = cleanStateTech(StateCensus15)
# statedata = derivedColumns(statedata)
# statedata[0].to_csv('2017_Census_State_data.csv', index=False)
# statedata[1].to_csv('2015_Census_State_data.csv', index=False)


def getStatesLoc(filename):
    # Call this function to download the latitude and longitude of each US state.
    # Extract the table from the website 'ttps://developers.google.com/public-data/docs/canonical/states_csv'
    # Call this function and save a csv file called 'filename' at the repo
    StatesLoc = []
    states_loc_url = 'https://developers.google.com/public-data/docs/canonical/states_csv'
    html = urllib2.urlopen(states_loc_url).read()
    soup = BeautifulSoup(html)
    #  soup.find_all("table") will return a result set containing bs4.elements
    #  Since there is only table on this website, I make the index equal to 0
    StatesLongLat = soup.find_all("table")[0]
    states_long_lat = []
    # each state is inserted in 'tr' tags
    for state_row in StatesLongLat.findAll('tr'):
        # each cell of one particular row is inserted in 'td' tags, and created a new set columns to store values of all cell
        values = state_row.findAll('td')
        state_long_lat_set = []
        for value in values:
            # store each element in the set columns in the new list output_row
            state_long_lat_set.append(value.text)
        states_long_lat.append(state_long_lat_set)
    StatesLoc.append(states_long_lat)
    for i in range(len(StatesLoc)):
        global path
        with open(os.path.join(path, filename), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(StatesLoc[i])


def loadStateLoc(filename):
    # Call this function to read the State Locatoion.csv file into a clean dataframe
    getStatesLoc(filename)
    StateLoc = pd.read_csv(filename, header=None)
    StateLoc.columns = ['stateabb', 'latitude', 'longitude', 'statename']
    return StateLoc


StateLoc = loadStateLoc('State Location.csv')


def mergeAll(StateH1B_agg, StateTech, StateCensus, StateLoc):
    # Call this function to merge four seperate clean data tables for each year together - the State Cencus data,
    # the State Tech and Science Index data, the State Location data and the State H1B data.
    H1BMergeIndex = StateH1B_agg.merge(StateTech, how='inner', left_on=[
                                       'StateAbb'], right_on=['abbrev'])
    H1BMergeIndex = H1BMergeIndex.drop(['abbrev'], axis=1)
    H1BMergeCencus = H1BMergeIndex.merge(StateCensus, how='inner', left_on=[
                                         'StateAbb'], right_on=['abbrev'])
    H1BMergeLoc = H1BMergeCencus.merge(StateLoc, how='inner', left_on=[
        'StateAbb'], right_on=['stateabb'])
    Merge = H1BMergeLoc.drop(['Rank', 'State_y',
                              'abbrev', 'stateabb', 'State_x'], axis=1)
    Merge = Merge.rename(columns={'Avg_Annual_Prevailing_Wage': 'H1B_Average_Wage',
                                  'CASE_NUMBER': 'H1B_Case_Number',
                                  'Employer_Number': 'H1B_Employer_Number',
                                  'statename': 'State',
                                  'Score': 'TechSciScore'})
    Merge = Merge[['State', 'StateAbb',
                   'H1B_Employer_Number', 'H1B_Average_Wage',
                   'TechSciScore', 'percent_move_from_abroad_above_college_degree',
                   'H1B_Case_Number',
                   'latitude', 'longitude']]
    return Merge


Merge18 = mergeAll(StateH1B18, StateTech18, StateCensus17, StateLoc)
Merge16 = mergeAll(StateH1B16, StateTech16, StateCensus15, StateLoc)

Merge16.to_csv('H1B Prediction Clean Data Year2016.csv', index=False)
Merge18.to_csv('H1B Prediction Clean Data Year2018.csv', index=False)


def readZippedFile(url):
    # Call this function to download the USA States Choropleth data from 'https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html'
    # To read zip file, cite 'https://medium.com/@loldja/reading-shapefile-zips-from-a-url-in-python-3-93ea8d727856'
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    global path
    z.extractall(path=path)
    filenames = [y for y in sorted(z.namelist())
                 for ending in ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
    dbf, prj, shp, shx = [filename for filename in filenames]
    usa = geopandas.read_file(shp)
    return usa


StateGeo = readZippedFile('https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_5m.zip')


def plotMerge(Merge18, StateGeo):
    # Call this function to plot color code each US State's H1B filings on US map for year2018
    # First change the normal dataframe Merge18 to geodataframe
    gMerge18 = geopandas.GeoDataFrame(Merge18, geometry=geopandas.points_from_xy(
        Merge18['longitude'], Merge18['latitude']))
    # Create a new column called 'H1B_Case_Number_Percent'
    gMerge18['H1B_Case_Number_Percent'] = gMerge18['H1B_Case_Number'] / \
        sum(gMerge18['H1B_Case_Number'])
    # Spacial join two geopandas geoDataFrame as we want one as the base layer and another as the second layor
    gMerge18.crs = StateGeo.crs
    sjoin_test = geopandas.sjoin(StateGeo, gMerge18, how='left')
    # Cite Prof Levy's code in class to do the plot
    fig, ax = plt.subplots(figsize=(30, 20))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    ax = sjoin_test[sjoin_test['NAME'].isin(['Aemrican Samoa',
                                             'Commonwealth of the Northern Mariana Islands',
                                             'District of Columbia',
                                             'Guam',
                                             'United States Virgin Islands',
                                             'Alaska',
                                             'Hawaii',
                                             'Puerto Rico']) == False].plot(ax=ax, column='H1B_Case_Number_Percent', legend=True, cax=cax)
    ax.axis('off')
    ax.set_title('Share of H1B filings')
    global path
    fig.savefig(path + '/H1B Filings Share Plot.png')


plotMerge(Merge18, StateGeo)


def scaleMerge(Merge1, Merge2, scale_lst):
    Merge = []
    Merge1 = Merge1.set_index(['State'])
    Merge1 = Merge1.drop(['StateAbb', 'latitude', 'longitude', 'geometry'], axis=1)
    Merge1['H1B_Case_Number_Percent'] = Merge1['H1B_Case_Number'] / sum(Merge1['H1B_Case_Number'])
    Merge2 = Merge2.set_index(['State'])
    Merge2 = Merge2.drop(['StateAbb', 'latitude', 'longitude'], axis=1)
    Merge2['H1B_Case_Number_Percent'] = Merge2['H1B_Case_Number'] / sum(Merge2['H1B_Case_Number'])
    sc_scale = preprocessing.StandardScaler().fit(Merge1[scale_lst])
    Merge1[scale_lst] = sc_scale.transform(Merge1[scale_lst])
    sc_scale = preprocessing.StandardScaler().fit(Merge2[scale_lst])
    Merge2[scale_lst] = sc_scale.transform(Merge2[scale_lst])
    Merge.append(Merge1)
    Merge.append(Merge2)
    return Merge


scale_lst = ['H1B_Average_Wage',
             'TechSciScore',
             'percent_move_from_abroad_above_college_degree',
             'H1B_Employer_Number']

Merge = scaleMerge(Merge18, Merge16, scale_lst)
Merge18 = Merge[0]
Merge16 = Merge[1]


def splitMerge(Merge1, Merge2):
    global X_train
    global Y_train
    global X_test
    global Y_test
    X_train = Merge1.drop(['H1B_Case_Number_Percent'], axis=1)
    Y_train = Merge1['H1B_Case_Number_Percent']
    X_test = Merge2.drop(['H1B_Case_Number_Percent'], axis=1)
    Y_test = Merge2['H1B_Case_Number_Percent']


X_train = pd.DataFrame()
X_test = pd.DataFrame()
Y_train = pd.DataFrame()
Y_test = pd.DataFrame()

splitMerge(Merge18, Merge16)
