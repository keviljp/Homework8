# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:01:22 2023

@author: josh
"""

"""
coding for graph 1: This graph will be total deaths per year accross all regions
"""
deathsByYearR = {}
with open ("Regions Clean.csv", 'r') as clean:
    for line in clean:
        line = line.strip("\n").split(",")
        year = line[3]
        deaths = int(line[6])
        if year not in deathsByYearR:
            deathsByYearR[year] = deaths
        else:
            deathsByYearR[year] += deaths

    
print("---------------------")

deathsByYearUS = {}
with open ("UnitedStates Clean.csv", 'r') as clean:
    for line in clean:
        line = line.strip("\n").split(",")
        year = line[3]
        deaths = int(line[6])
        if year not in deathsByYearUS:
            deathsByYearUS[year] = deaths
        else:
            deathsByYearUS[year] += deaths

for year in deathsByYearR:
    difference = deathsByYearUS[year]-deathsByYearR[year]
    print(year,"; US:", deathsByYearUS[year],"; Regions:", deathsByYearR[year],";", difference)

'''
coding for graph 2: This graph will be total deaths per region scaled by percent of the
us population made up by that region in that year. 
'''

'''
coding for graph 3: This graph will be a 3D graph of total deaths by cause by year. 
'''
