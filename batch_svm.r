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
for (i in 1:length(temp)) {
  cat(temp[i])
  tones=read.csv(temp[i],header=TRUE)
  #str(toneData)
  tones<-preprocessTone(tones)
  
  
  ###########svm
  #create a subset of features
  dosvm(tones)
  #no pos
  cat("============no pos\n")
  toneSub1<-tones[c(4:38)]
  dosvm(toneSub1)
  #no func/pos
  cat("============no fun/pos\n")
  toneSub1<-tones[c(7:38)]
  dosvm(toneSub1)
  
  cat("============no entity/singleton\n")
  toneSub1<-tones[c(7:9,11:13,15:38)]
  dosvm(toneSub1)
  
  cat("============no entity\n")
  toneSub1<-tones[c(7:9,11:38)]
  dosvm(toneSub1)
  
  cat("============no singleton\n")
  toneSub1<-tones[c(7:13,15:38)]
  dosvm(toneSub1)
  
  cat("============no tok-bound\n")
  toneSub1<-tones[c(7:10,14:38)]
  dosvm(toneSub1)
  
  cat("============no phons\n")
  toneSub1<-tones[c(7:14,35:38)]
  dosvm(toneSub1)
  
  #no sent position
  cat("============no sent position\n")
  toneSub1<-tones[c(7,8,10:38)]
  dosvm(toneSub1)
  #feature set: without pos,func, prev,next,sent_pos 62.27, best so far
  cat("============no prev, next tone\n")
  toneSub1<-tones[c(7,8,10:35,38)]
  dosvm(toneSub1)
  #removing rounding is not good:
  #toneSub1<-toneSub[c(7,8,10:34,38)]
  #include prev next tone:61.82
  
  cat('************************************\n')
  
  
}


