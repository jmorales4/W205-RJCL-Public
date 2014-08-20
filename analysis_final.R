#############################################
# RJCL W205 Project
# analysis_final.R:  Correlating stock price changes with predictions from Twitter
# 08/17/2014
#############################################

### Set working directory
getwd();
setwd("C:/Berkeley MIDS/W205/Project/");
list.files();

library(ggplot2)
library(lubridate)


data <- read.csv("2014080900.csv",header=T)
data$dateOnly <- as.Date(data$datetime);
colnames(data)

### Stocks with most Tweets
stockTweetVolume <- tapply(data$tweetVolume,data$ticker,sum,na.rm=T)
stockTweetVolume <- as.data.frame(stockTweetVolume)
stockTweetVolume$ticker <- rownames(stockTweetVolume)
rownames(stockTweetVolume) <- NULL
colnames(stockTweetVolume) <- c("tweetVolume","ticker")

head(stockTweetVolume[order(stockTweetVolume$tweetVolume,decreasing=T),],n=10)
head(stockTweetVolume[order(stockTweetVolume$tweetVolume),],n=100)

### 10 Most Relevant Tweets
head(data[order(data$mostRelevantTweetScore,decreasing=T),],n=10)
dataMinusAmp <- data[!grepl("&",data$mostRelevantTweetText),]
dataMinusAmp <- dataMinusAmp[!is.na(dataMinusAmp$mostRelevantTweetScore),]
head(dataMinusAmp[order(dataMinusAmp$mostRelevantTweetScore,decreasing=T),],n=10)
  ### most relevant tweet with out a "&" has a score of 1.558 ...
  ### maybe we should cap at 2? (would remove about 5000 records)

max(dataMinusAmp$mostRelevantTweetScore, na.rm=T)
summary(dataMinusAmp$mostRelevantTweetScore, na.rm = T)

sum(is.na(data$priceShift))
dataWithPriceShift <- data[data$priceShift != 0,] ### Using data with price shifts as proxy for working hours

### 10-minute interval data
summary(dataWithPriceShift$tweetShift)
qplot(dataWithPriceShift$priceShift,
      dataWithPriceShift$tweetShift,
      xlab = "Price Shift",
      ylab = "Tweet Shift",
      xlim = c(-5,5),
      main = "Tweet Shift vs Price Shift");

cor.test(dataWithPriceShift$priceShift,dataWithPriceShift$tweetShift);


#### Hourly Data
head(dataWithPriceShift)
dataWithPriceShift$datetime2 <- as.character(dataWithPriceShift$datetime)
dataWithPriceShift$datetimeClean <- as.POSIXct(dataWithPriceShift$datetime2, tz="GMT")
dataWithPriceShift <- subset(dataWithPriceShift,select = -c(datetime2))
dataWithPriceShift$hour <- hour(dataWithPriceShift$datetimeClean)

hourPriceShift <- aggregate(dataWithPriceShift$priceShift ~ dataWithPriceShift$dateOnly + dataWithPriceShift$hour,
                            data = dataWithPriceShift,
                            sum)
class(hourPriceShift)
colnames(hourPriceShift) = c("dateOnly","hour","priceShift")
head(hourPriceShift)

hourTweetShift <- aggregate(dataWithPriceShift$tweetShift ~ dataWithPriceShift$dateOnly + dataWithPriceShift$hour,
                            data = dataWithPriceShift,
                            sum)
colnames(hourTweetShift) = c("dateOnly","hour","tweetShift")
head(hourTweetShift)

hourData <- merge(hourPriceShift,hourTweetShift,by=c("dateOnly","hour"))

qplot(hourData$priceShift,
      hourData$tweetShift,
      xlab = "Price Shift",
      ylab = "Tweet Shift",
      main = "Tweet Shift vs Price Shift");

cor.test(hourData$priceShift,hourData$tweetShift);


### Day-Level Data
dayPriceShift <- tapply(dataWithPriceShift$priceShift, dataWithPriceShift$dateOnly,sum, na.rm = T)
dayPriceShift <- as.data.frame(dayPriceShift)
dayPriceShift$dateOnly <- rownames(dayPriceShift)
rownames(dayPriceShift) <- NULL
dayPriceShift

dayTweetShift <- tapply(dataWithPriceShift$tweetShift,dataWithPriceShift$dateOnly,sum, na.rm = T)
dayTweetShift <- as.data.frame(dayTweetShift)
dayTweetShift$dateOnly <- rownames(dayTweetShift)
rownames(dayTweetShift) <- NULL
dayTweetShift

dayData <- merge(dayPriceShift,dayTweetShift,by="dateOnly")
head(dayData)

qplot(dayData$dayPriceShift,
      dayData$dayTweetShift,
      xlab = "Price Shift",
      ylab = "Tweet Shift",
      main = "Tweet Shift vs Price Shift");

cor.test(dayData$dayPriceShift,dayData$dayTweetShift);


### 10-minute shifted correlation
dataWithPriceShift$datetime10MinShift <- dataWithPriceShift$datetimeClean+600

help(merge)
colnames(dataWithPriceShift)
shiftedData <- merge(dataWithPriceShift,dataWithPriceShift,
                     by.x=c("datetimeClean","ticker"),
                     by.y = c("datetime10MinShift","ticker"))

head(shiftedData)

cor.test(shiftedData$priceShift.y, shiftedData$tweetShift.x)

qplot(shiftedData$priceShift.y,
      shiftedData$tweetShift.x,
      xlab = "Price Shift (after 10 min)",
      ylab = "Tweet Shift",
      xlim = c(-5,5),
      main = "Tweet Shift vs Price Shift w/ 10 min shift");

