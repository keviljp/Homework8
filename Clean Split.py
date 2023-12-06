# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:39:38 2023

@author: josh
"""
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