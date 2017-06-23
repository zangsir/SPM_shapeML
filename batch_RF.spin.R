library(mlbench)
library(caret)
library(e1071)
setwd('~/Desktop/cmn_mapping/')

#tone134<-read.csv('downsample_syl_3_meta_200_134_.csv',header=TRUE)
#head(tone134)
#str(tone134)

source('util_functions.r')

temp = list.files(pattern="*_.csv")
#myfiles = lapply(temp, read.delim)
#currently we start from i=2 b/c i=1 is is 134 we've done that already
for (i in 3:length(temp)) {
  print(temp[i])
  tones=read.csv(temp[i],header=TRUE)
  #str(toneData)
  tones<-preprocessTone(tones)
  ########################  randomForest
  #http://trevorstephens.com/kaggle-titanic-tutorial/r-part-5-random-forests/
  library('randomForest')
  fit <- randomForest(label ~ .,data=tones, importance=TRUE, ntree=2000)
  #fit
  #accuracy is 56.21 with full feature set.
  #accuracy is worse with toneSub1 best feature set. 
  # Look at variable importance
  print(varImpPlot(fit))
  



  ###########svm
  library(e1071)
  
  #create a subset of features
  dosvm(tones)
  #no pos
  toneSub1<-tones[c(4:38)]
  dosvm(toneSub1)
  #no func/pos
  toneSub1<-tones[c(7:38)]
  dosvm(toneSub1)
  #no sent position
  toneSub1<-tones[c(7,8,10:38)]
  dosvm(toneSub1)
  #feature set: without pos,func, prev,next,sent_pos 62.27, best so far
  toneSub1<-tones[c(7,8,10:35,38)]
  dosvm(toneSub1)
  #removing rounding is not good:
  #toneSub1<-toneSub[c(7,8,10:34,38)]
  #include prev next tone:61.82


  
}


