
###STEP 4 - DECISION TREE ANALYSIS

#Bringing the table in from mySQL
library(RMySQL)

m<-dbDriver("MySQL");
con<-dbConnect(m,user='root',password='root',host='localhost',dbname='IndepProject');
res<-dbSendQuery(con, "select * from IndiaStateData")
StateData<- fetch(res)

#converting to data frame
stateData <- as.data.frame.matrix(StateData)

#removing unnecessary columns
stateData <-stateData[ -c(2:4, 7:9, 11:15, 27:28) ]

#converting the 'none' type to NAs
stateData[stateData == 'none'] <- NA

#converting columns to numeric that were brought in with 'none' observations 
for(i in c(2:6, 8:14)) {
stateData[,i] <- as.numeric(as.character(stateData[,i]))}

#decision tree method 1, parameters 1
library(rpart)
dt2_01 <- rpart(perCapDomestConsump ~ perCapElectricGen + PerCapitaGSDP + PercPoverty + PercHouseholdsRural+  PercTownVillagElectrif + PercFarFrmWater + LiteracyRate + InfantMortality +RuralRoadInfra, data=stateData)
print(dt2_01)
windows()
plot(dt2_01)
text(dt2_01)

#decision tree method 2, paramaters 1
library("partykit")
consumpTree <- ctree(perCapDomestConsump ~ perCapElectricGen + PerCapitaGSDP + PercPoverty + PercHouseholdsRural+  PercTownVillagElectrif + PercFarFrmWater + LiteracyRate + InfantMortality + RuralRoadInfra, data=stateData)
print(consumpTree)
windows()
plot(consumpTree)
library("strucchange")
sctest(consumpTree)

#decision tree method 1, parameters 2
library(rpart)
dt2_01 <- rpart(perCapDomestConsump ~ perCapElectricGen + PerCapitaGSDP + PercPoverty + PercHouseholdsRural+  PercTownVillagElectrif + PercFarFrmWater + LiteracyRate + InfantMortality +RuralRoadInfra, data=stateData,minsplit=9)
print(dt2_01)
windows()
plot(dt2_01)
text(dt2_01)

#decision tree method 2, paramaters 2
library("partykit")
consumpTree <- ctree(perCapDomestConsump ~ perCapElectricGen + PerCapitaGSDP + PercPoverty + PercHouseholdsRural+  PercTownVillagElectrif + PercFarFrmWater + LiteracyRate + InfantMortality + RuralRoadInfra, data=stateData, minsplit=9)
print(consumpTree)
windows()
plot(consumpTree)
library("strucchange")
sctest(consumpTree)
