library(mlbench)
library(caret)
library(e1071)
setwd('~/Desktop/cmn_mapping/')

#tone134<-read.csv('downsample_syl_3_meta_200_134_.csv',header=TRUE)
#head(tone134)
#str(tone134)

#source('util_functions.r')

temp = list.files(pattern="*_.csv")
#myfiles = lapply(temp, read.delim)
#currently we start from i=2 b/c i=1 is is 134 we've done that already
for (i in 3:length(temp)) {
  print(temp[i])
  tones=read.csv(temp[i],header=TRUE)
  #str(toneData)
  
  #preprocess and classification
  toneSub<-preprocessTone(tones)
  str(toneSub)
  #featImp(toneSubdata)
  #feature importance
  control <- trainControl(method="repeatedcv", number=19, repeats=3)
  # train the model
  model <- train(label~., data=toneSub, method="lvq", preProcess="scale", trControl=control)
  # estimate variable importance
  importance <- varImp(model, scale=FALSE)
  # summarize importance
  print(importance)
  # plot importance
  print(plot(importance))
}


