# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 11:59:00 2014

@author: Jillian
"""

###STEP 3 - EXPLORATORY GRAPHING

#Importing  master dataset back in as a data frame
import MySQLdb as myDB
import pandas as pd
import pylab as pl

#establishing a connection to the database
conn = myDB.connect(host='localhost',user='root', passwd='root',db='IndepProject')

#reding the SQL table
Data = pd.read_sql("SELECT * from IndiaStateData", conn)

#resetting the key to index by state abbreviation
Data = Data.set_index('StateAbbrev')

#creating graph of domestic consumption and electricity generated
GeneratedConsumedComp =  Data[["perCapElectricGen","population","perCapDomestConsump"]]
PerCapElectricGeneratedConsumed = GeneratedConsumedComp[["perCapElectricGen","perCapDomestConsump"]]
graph = PerCapElectricGeneratedConsumed.plot(kind='bar', stacked=False, title='Per Capita Power Generation and Domestic Consumption by State')

#prepping data for scatter plots 
consump = Data['perCapDomestConsump'].tolist()
literacy = Data['LiteracyRate'].tolist()
poverty = Data['PercPoverty'].tolist()
percElect = Data['PercTownVillagElectrif'].tolist()

Data2 = Data[Data.PercHouseholdsRural != 'none']
rural = Data2['PercHouseholdsRural'].tolist()
consump2 = Data2['perCapDomestConsump'].tolist()

Data3 = Data[Data.PerCapitaGSDP != 'none']
Data3.PerCapitaGSDP = Data3.PerCapitaGSDP.astype(float)
wealth = Data3['PerCapitaGSDP'].tolist()
consump3 = Data3['perCapDomestConsump'].tolist()

Data4 = Data[Data.InfantMortality != 'none']
infantMort = Data4['InfantMortality'].tolist()
consump4 = Data4['perCapDomestConsump'].tolist()

Data5 = Data[Data.RuralRoadInfra != 'none']
Data5.RuralRoadInfra = Data5.RuralRoadInfra.astype(float)
roadDensityWeighted = Data5['RuralRoadInfra'].tolist()
roadDensityWBstat = Data5['RuralRoadDensity'].tolist()
consump5 = Data5['perCapDomestConsump'].tolist()

Data6 = Data[Data.PercFarFrmWater != 'none']
waterAvail = Data6['PercFarFrmWater'].tolist()
consump6 = Data6['perCapDomestConsump'].tolist()

#defining a function for scatter plots
def scatter(x,y,z):
    pl.figure(n)    
    pl.scatter(y, x, s=100)
    pl.xlabel('Per Capita Domestic Consumption', fontsize=22)
    pl.ylabel(z, fontsize=22)
    pl.show()

#creating scatter plots
n = "rural"
scatter(rural, consump2, "% Households Rural")
n ="literacy"
scatter(literacy, consump, "Literacy Rate")
n= "wealth"
scatter(wealth, consump3, "Per Capita GSDP")
n= "ruralRoadDensity_weighted"
scatter(roadDensityWeighted,consump5, "Rural Road Density: Weighted")
n= "ruralRoadDensity_WB"
scatter(roadDensityWBstat,consump5, "Rural Road Density: WB Stat")
n="water access"
scatter(waterAvail, consump6, "% Households Far from Water")
n= "poverty"
scatter(poverty, consump, "Poverty Rate")
n= 'InfantMortality'
scatter(infantMort, consump4, "Infant Mortality Rate")
n= 'PercentElectified'
scatter(percElect, consump, "% Towns/Villages Electrified")



