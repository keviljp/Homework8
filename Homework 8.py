# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:01:22 2023

@author: josh and nate
Dec. 6, 2023
CSC 221B
HW 8

Part B
We chose a data set that consists of US regional deaths from 2016-2023. In this set, we have entries from 52+ US regions along with the death type, death count, the year, and the unweighted total of deaths. In our project we will have two different plots.

In plot 1, ...
In plot 2, we have the type of death and year computed with the total number of deaths. This will aim to help understand trends for deaths over the years and if there are increases or decreases and how we can explain this phenomena. 
"""


#put libraries here: 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

'''
coding for graph 1: This graph will be total deaths per region scaled by percent of the
us population made up by that region in that year. 
'''





'''
coding for graph 2: This graph will be a 3D graph of total deaths by cause by year. 
'''

#this will open a clean "unweighted" file that has data of deaths from 2016-2023. This has the death type, the region, the year, and the cound. There are over 250,000 entries
deathsByYearType = {}
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

