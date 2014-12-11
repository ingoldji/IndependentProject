###STEP 1 - RETRIEVING DATA FROM WORLD BANK

#Using WDI to import all of the necessary data from the World Bank website
library("WDI")
I = c('IN.ENRGY.ELEC.CAP','IN.ENRGY.ELEC.GEN','IN.EC.POP.TOTL','IN.EC.GSDP.PERCAP.NOM.USD','IN.POV.HCR.EST.TOTL', 'IN.FIN.HH.RURL', 'IN.FIN.HH.TOTL', 'IN.POV.HH.DRKNGWATER.AWAY','IN.POV.LIT.RAT.TOTL','IN.ENRGY.TOWNS.ELECTRFIED.NUM', 'IN.ENRGY.TOWNS.TOTL', 'IN.ENRGY.VILLAG.ELECTRFIED', 'IN.ENRGY.VILLAG.TOTL')
dat = WDI(indicator= I, start=2011, end=2011)
J = c('IN.EDU.GR.ENRL.RATIO','IN.POV.INF.MORTRATE')
enroll = WDI(indicator = J, start=2012, end=2012)
roads = WDI(indicator = 'IN.TRANSPORT.RURLRD.DENSIT', start=2008, end=2008)
dat2 = cbind(dat,enroll,roads)

#removing unnecessary columns that were automatically imported
dat2$year <- NULL
dat2$year <- NULL
dat2$year <- NULL
dat2$country <- NULL
dat2$country <- NULL

#Creating a csv version of the file to use in Python
write.csv(dat2, file = "C:/Users/Jillian/Documents/GWU/2014.Fall/T_Programming/IndependentProject/WBdata.csv")
