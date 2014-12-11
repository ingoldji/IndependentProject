
###STEP 5 - CORRELATION ANALYSIS

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

#keeping only numeric columns
numState <-stateData[,c(2:6,8:15)]

#converting columns into separate vectors
lapply(names(numState), function(x) assign(x, numState[, x], envir = .GlobalEnv))

#carrying out tests
cor.test(perCapDomestConsump,PerCapitaGSDP)
cor.test(perCapDomestConsump,InfantMortality)
cor.test(perCapDomestConsump,LiteracyRate)
cor.test(perCapDomestConsump,PercFarFrmWater)
cor.test(perCapDomestConsump,PercHouseholdsRural)
cor.test(perCapDomestConsump,PercPoverty)
cor.test(perCapDomestConsump,RuralRoadInfra)
