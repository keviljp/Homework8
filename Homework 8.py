# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:01:22 2023

@author: josh and nate
Dec. 6, 2023
CSC 221B
HW 8

Part B
We chose a data set that consists of US regional deaths from 2016-2023. In this set, we have entries from 52+ US regions along with the death type, death count, the year, and the
unweighted total of deaths. In our project we will have two different plots.

In plot 1, we have the type of death and year computed with the total number of deaths. This will aim to help understand trends for deaths over the years and 
if there are increases or decreases and how we can explain this phenomena. 

In plot 2, we have the average number of deaths per 100,000 from select causes by region. This will aim to help understand the regional trends in illness as 
well as where resources should be focused to correct these trends. 
"""


#put libraries here: 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import csv


'''
coding for graph 2: This graph will be a 3D graph of total deaths by cause by year. 
'''
#this is a dictionary that will organize the death type, death count, and year data
deathsByYearType = {}

#this will open a clean "unweighted" file that has data of deaths from 2016-2023. This has the death type, the region, the year, and the cound. There are over 250,000 entries
try:
    with open("Regions Clean.csv", 'r') as clean:
        for line in clean:
            line = line.strip("\n").split(",")
            year = line[3]
            death_type = line[5]
            deaths = int(line[6])

            if year not in deathsByYearType:
                deathsByYearType[year] = {death_type: deaths}
            else:
                if death_type not in deathsByYearType[year]:
                    deathsByYearType[year][death_type] = deaths
                else:
                    deathsByYearType[year][death_type] += deaths
except FileNotFoundError:
    print("File not found. Please check the file path or file name.")
except Exception as e:
    print(f"An error occurred: {e}")

#this creates a 3-d plot and figure
fig = plt.figure(figsize=(7, 8))
ax = fig.add_subplot(111, projection='3d')

#this will extract the unique years and the unique deaths listed in the file
years = list(deathsByYearType.keys())
types = list(set(death_type for value in deathsByYearType.values() for death_type in value.keys()))
types.sort()

#colors for the bar
colors = ['b', 'g', 'r', 'y', 'm', 'c']

bar_width = 0.5 
bar_offset = 0.25 

#this creates bars using the bar3d method. It will take each year and the death type as the x and y axis and the z axis is the number of deaths.
for i, year in enumerate(years):
    for j, death_type in enumerate(types):
        if death_type in deathsByYearType[year]:
            ax.bar3d(i - bar_offset, j - bar_offset, 0, bar_width, bar_width, deathsByYearType[year][death_type], color=colors[j % len(colors)])

#x-axis ticks and labels
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years, rotation=45)
ax.tick_params(axis='x', pad=5)

#y-axis ticks and labels
ax.set_yticks(range(len(types)))
ax.set_yticklabels(types, rotation=-25, va='baseline', ha='center')  # Adjust rotation and horizontal alignment
ax.tick_params(axis='y', pad=62)

#label the 3 axis
ax.set_xlabel('Year', labelpad=15)
ax.set_ylabel('Death Type', labelpad=80)
ax.set_zlabel('Number of Deaths', labelpad=15)

#how to change view of the 3-d plot
ax.view_init(30, 120)

#these are the limits for the respective axis
ax.set_xlim(-0.5, len(years) - 0.5)
ax.set_ylim(-0.5, len(types) - 0.5)
ax.set_zlim(0, max([deathsByYearType[year][death_type] for year in deathsByYearType for death_type in deathsByYearType[year]]) * 1.1)

#this will display the 3-d graph in a compact layout
plt.tight_layout()
plt.show()

# this is a DataFrame from deathsByYearType
df = pd.DataFrame(deathsByYearType)

# this transpose the df to have years as rows and death types as columns
df = pd.DataFrame(deathsByYearType).transpose()

# place the columns alphabetically 
df = df.reindex(sorted(df.columns), axis=1)

# Display 
with pd.option_context('display.max_columns', None):
    print(df)

#the program for plot 2 has ended.




'''
coding for graph 1: This graph will be total deaths per region scaled by percent of the
us population made up by that region in that year. 
'''
'''
This function reads the cleaned and combined census data file, iterating line by line
dividing the state population in that year by 100,000 and assigning that value to the year key in 
the dictionary in the region key of the RegionMultFactor dictionary.
'''
def adjust():
    RegionMultFactor = {}
    with open ("census_data.csv", 'r') as census:
        data = csv.reader(census)
        next(data)
        for line in data:
            Year = 2015
            years = {}
            num = len(line)
            if line[0] == "Puerto Rico":
                for num in range(1,num):
                    years[Year] = round(int(line[num])/100000,4)
                    Year+=1
            else: 
                for num in range(1,num):
                    years[Year] = round(int(line[num])/100000,4)
                    Year+=1
            if line[0] not in RegionMultFactor:
                RegionMultFactor[line[0]] = years
    return RegionMultFactor

RegionMultFactor = adjust()

'''
This secton opens  the clean death data region file and iterates line by line creating
a dictionary for each region where the keys are years and the values are total deathhs 
and putting it in a dictionary where the regions are the keys and the other dictionaries
are the values. 
'''
RegionsCount = {}
with open ("Regions Clean.csv", 'r') as clean:
    for line in clean:
        line = line.strip("\n").split(",")
        year = line[3]
        region = line[0]
        deaths = int(line[6])
        if region not in RegionsCount:
            RegionsCount[region] = {}
        else:
            if year not in RegionsCount[region]:
                RegionsCount[region][year] =deaths
            else:
                RegionsCount[region][year] += deaths

#This recombines New York City to New York because its not that Important, 
#its just another city.

for year in RegionsCount['New York City']:
    RegionsCount["New York"][year]+=RegionsCount['New York City'][year]
RegionsCount.pop('New York City')

'''
This section adjusts the death counts by year by region by  the population
density by year by region and adds the adjusted number in the region's key in
the Finals dictionary. The final number is divided by 9 so it is on an average 
per year basis. The result is a dictionary of regions and their deaths per  
100,000 people by the causes specified in graph 1. 
'''
Finals = {}
for region in RegionsCount:
    if region not in Finals:
        Finals[region]= 0
    for year in RegionsCount[region]:
        Finals[region]+= RegionsCount[region][year]/(RegionMultFactor[region][int(year)]*9)

regions = list(Finals.keys())
deathTotals = list(Finals.values())

plt.figure(figsize=(14, 9)) 
plt.bar(range(len(Finals)), deathTotals, tick_label=regions, width = .7)
plt.subplots_adjust(top=.5)
plt.ylim(0, max(deathTotals) + 30) 
plt.xticks(rotation=55, ha='right', fontsize=12) 
plt.yticks(fontsize=10)
plt.xlabel('Region', fontsize=12)
plt.ylabel('Deaths per 100,000', fontsize=12)
plt.title('Deaths Per 100,000 by Region Between 2015-2023 From Select Causes', fontsize = 14)
plt.show()

'''
This program is similar to the original used to clean the CDC file. We deleted columns from the CDC
file that we didnt need, and iterated through it, writing any line with unweighted data to this 
"Clean.csv" file that is shown here. From there we split that document into a Regions document and a 
United states document to be used with our Graps. Shown here is the code to split the Clean.csv document.
'''
'''
with open ('UnitedStates Clean.csv',"w") as doink:
    doink.write('')
with open ('Regions Clean.csv',"w") as doink:
    doink.write('')
US = open ('UnitedStates Clean.csv',"a")
Regions = open ('Regions Clean.csv',"a")

with open ("Clean.csv", 'r') as clean:
    for line in clean:
        line = line.strip("\n").split(",")
        region = line[0]
        if region == 'United States':
            final = ",".join(line)
            US.write(final+"\n")
        else:
            final = ",".join(line)
            Regions.write(final+"\n")
US.close()
Regions.close()
'''

#the program for plot 1 has ended.

#How were we creative?
"""We used python's matplotlib's 3d graphing capability to display a three dimensional approach to visualizing the trends in mortality among 2015-2023. In addition, we"""
