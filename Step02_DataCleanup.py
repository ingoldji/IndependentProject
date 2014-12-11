# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 10:07:30 2014

@author: Jillian
"""
###STEP 2.A - BRINGING IN THE WORLD BANK DATA AS A DATA FRAME AND PREPPING IT

import pandas as pd
import urllib2

#importing the csv R created
WBdata = pd.DataFrame.from_csv("C:/Users/Jillian/Documents/GWU/2014.Fall/T_Programming/IndependentProject/WBdata.csv")
#trimming whitespace from state names
WBdata["country"] = WBdata["country"].map(str.strip)
#dropping data that does not correspond to a particular state or territory
WBdata = WBdata[WBdata.country != "All States in India"] 
WBdata = WBdata[WBdata.country != "All Union Territories in India"]
WBdata = WBdata[WBdata.country != "Central Govt. Projects"]
WBdata = WBdata[WBdata.country != "D.V.C."]
WBdata = WBdata[WBdata.country != "Others"]
WBdata = WBdata[WBdata.country != "India"]
#correcting a spelling error in WB data and filling in the missing value for Puducherry's population
WBdata = WBdata.replace('Pudducherry', 'Puducherry')
WBdata['IN.EC.POP.TOTL'] = WBdata['IN.EC.POP.TOTL'].replace(0, 1247.953)
#creating an abbreviations column of state names for use in graphs
WBdata['StateAbbrev'] = WBdata['country'].str[:6]
#setting state abbreviations as the index for joins with domestic consumption data
WBdata = WBdata.set_index('StateAbbrev')

###STEP 2.B - DOWNLOADING DOMESTIC CONSUMPTION DATA AND PREPPING IT
 
myfile = urllib2.urlopen("http://mospi.nic.in/mospi_new/upload/SYB2014/CH-16-ENERGY/Table%2016.3.xls")
output = open('C:/Users/Jillian/Documents/GWU/2014.Fall/T_Programming/IndependentProject', 'wb')

url = "http://mospi.nic.in/mospi_new/upload/SYB2014/CH-16-ENERGY/Table%2016.3.xls"

u = urllib2.urlopen(url)
localFile = open('file.csv', 'w')
localFile.write(u.read())
localFile.close()

fileUrl = "http://mospi.nic.in/mospi_new/upload/SYB2014/CH-16-ENERGY/Table%2016.13.xls"
f = urllib2.urlopen(fileUrl)
data = f.read()
with open('C:/Users/Jillian/Documents/GWU/2014.Fall/T_Programming/IndependentProject/power3.xls', 'wb') as w:
    w.write(data)
xls = pd.ExcelFile('C:/Users/Jillian/Documents/GWU/2014.Fall/T_Programming/IndependentProject/power3.xls')
df = xls.parse('table 16.13 statewise', skiprows=11, index_col=None, na_values=['NA'])

#selecting columns of interest
domesticConsump = df.iloc[:,[0,8]]
#giving the columns appropriate names
domesticConsump = domesticConsump.rename(columns={'Unnamed: 0': 'state',' 2011-12.1': 'domesticCons'})
#dropping empty rows
domesticConsump = domesticConsump.dropna(subset=['state'])
#converting from unicode and trimming whitespace from state names
domesticConsump['state'] = domesticConsump['state'].apply(str)
domesticConsump['state'] = domesticConsump['state'].map(str.strip)
#removing unnecessary rows
domesticConsump = domesticConsump[domesticConsump.state != 'Union Territory:']
domesticConsump = domesticConsump[1:-2]
#unifying state names with those of the WB database
domesticConsump = domesticConsump.replace({'state' : { 'A. & N. Islands' : 'Andaman and Nicobar Islands', 'D. & N.Haveli' : 'Dadra and Nagar Haveli', 'Daman & Diu' : 'Daman and Diu', 'Jammu & Kashmir' : 'Jammu and Kashmir', 'Orissa' : 'Odisha', 'Uttara Khand' : 'Uttarakhand' }})
#making state abbreviations column
domesticConsump['StateAbbrev'] = domesticConsump['state'].str[:6]
#setting state abbreviations as index values
domesticConsump = domesticConsump.set_index('StateAbbrev')

###STEP 2.C - JOINING DATA INTO SINGLE DATABASE
#joining with WB data
CombinedData = WBdata.join(domesticConsump, how='left')

#removing the iloc and country columns
def drop(x):
    global CombinedData
    CombinedData = CombinedData.drop(x, axis=1)

drop('iso2c')
drop('iso2c.1')
drop('iso2c.2')
drop('country')

#giving columns more intuitive names
CombinedData = CombinedData.rename(columns={'IN.EC.POP.TOTL':'population', 'IN.ENRGY.ELEC.CAP':'InstalledCapacity', 'IN.ENRGY.ELEC.GEN': 'ElectricityGenerated', 'IN.EC.GSDP.PERCAP.NOM.USD': 'PerCapitaGSDP', 'IN.POV.HCR.EST.TOTL': 'PercPoverty', 'IN.FIN.HH.RURL': 'NumRuralHouseholds', 'IN.FIN.HH.TOTL': 'NumHouseholds', 'IN.POV.HH.DRKNGWATER.AWAY': 'HouseFarFrmWater', 'IN.POV.LIT.RAT.TOTL': 'LiteracyRate', 'IN.EDU.GR.ENRL.RATIO': 'EnrollmentRate', 'IN.TRANSPORT.RURLRD.DENSIT': 'RuralRoadDensity', 'IN.POV.INF.MORTRATE': 'InfantMortality', 'IN.ENRGY.TOWNS.ELECTRFIED.NUM': 'TownsElectified', 'IN.ENRGY.TOWNS.TOTL': 'NumTowns', 'IN.ENRGY.VILLAG.ELECTRFIED': 'VillagesElectrif', 'IN.ENRGY.VILLAG.TOTL':'NumVillages'})

#calculating new variables
def calc(x,y,z):
    global CombinedData
    CombinedData[x] = CombinedData[y]/CombinedData[z]
    
calc('perCapDomestConsump', 'domesticCons', 'population')
calc('PercHouseholdsRural','NumRuralHouseholds','NumHouseholds')
calc('PercFarFrmWater', 'HouseFarFrmWater', 'NumHouseholds')
calc('perCapElectricGen', 'ElectricityGenerated', 'population')
calc('RuralRoadInfra','RuralRoadDensity', 'PercHouseholdsRural')

CombinedData['PercTownVillagElectrif'] = (CombinedData['TownsElectified'] + CombinedData['VillagesElectrif'])/(CombinedData['NumTowns'] + CombinedData['NumVillages'])


###STEP 2.D - PREPPING FOR AND EXPORTING TO SQL
#Replacing NAs with none
CombinedData = CombinedData.fillna('none')
#Creating a surrogate key for use with SQL
CombinedData['key'] = list(range(len(CombinedData.index)))
CombinedData = CombinedData.reset_index('key')

import MySQLdb as myDB

conn = myDB.connect(host='localhost',user='root', passwd='root')
cursor = conn.cursor()
sql = 'CREATE DATABASE IF NOT EXISTS IndepProject;'
cursor.execute(sql)
cursor.close()

dbConnect = myDB.connect(host='localhost',
                            user='root',
                            passwd='root',
                            db='IndepProject')
                            
CombinedData.to_sql(con=dbConnect,
                name='IndiaStateData',
                if_exists='replace',
                flavor='mysql')
                
