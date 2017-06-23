library(mlbench)
library(caret)
library(e1071)
library(reshape)
setwd('~/Desktop/cmn_mapping/feature_files/')

#tone134<-read.csv('downsample_syl_3_meta_200_134_.csv',header=TRUE)
#head(tone134)
#str(tone134)

source('../cmn_map_rFiles/util_functions.r')
labels=c()
accuracies=c()
acc2<-c()
acc3<-c()
baseLines=c()
temp = list.files(pattern="*.csv")
#myfiles = lapply(temp, read.delim)
#currently we start from i=2 b/c i=1 is is 134 we've done that already
for (i in 1:length(temp)) {
  cat(temp[i])
  cat('\n')
  tones=read.csv(temp[i],header=TRUE)
  #str(toneData)
  if(ncol(tones)==28){
  tones<-preprocessToneBigram(tones)
  }
  else{tones<-preprocessToneTrigram(tones)}
  #base<-length(levels(tones$label))
  baseline<-1/(nlevels(tones$label))
  baseLines<-c(baseLines,baseline)
  cat('baseline:',1/base)
  ###########svm
  #no func/pos
  if(ncol(tones)==38){
  cat("============no fun/pos\n")
  toneSub1<-tones[c(7:38)]
  #dosvm(toneSub1)
  accuracy<-dosvm(toneSub1)
  
  cat("============no entity\n")
  toneSub1<-tones[c(7:9,11:38)]
  acc_noent<-dosvm(toneSub1)
  #dosvm(toneSub1)
  
  cat("============no singleton\n")
  toneSub1<-tones[c(7:13,15:38)]
  #dosvm(toneSub1)
  acc_nosing<-dosvm(toneSub1)
  }
  else{  cat("============no fun/pos\n")
    toneSub1<-tones[c(3:18)]
    #dosvm(toneSub1)
    accuracy<-dosvm(toneSub1)
    
    cat("============no entity\n")
    toneSub1<-tones[c(3:5,7:18)]
    #dosvm(toneSub1)
    acc_noent<-dosvm(toneSub1)
    
    cat("============no singleton\n")
    toneSub1<-tones[c(3:7,9:18)]
    #dosvm(toneSub1)
    acc_nosing<-dosvm(toneSub1)
    }
  label<-strsplit(temp[i],'_')[[1]][1]
  #label<-strsplit(prefix,'00_')[[1]][2]
  labels=c(labels,label)
  accuracies=c(accuracies,accuracy)
  acc2<-c(acc2,acc_noent)
  acc3<-c(acc3,acc_nosing)
  

  
  cat('************************************\n')
  
  
}

accuracy_noEntity<-acc2
accuracy_noSingleton<-acc3

data<-data.frame(labels,accuracies,accuracy_noEntity,accuracy_noSingleton,baseLines)
#plot(labels,accuracies, data=data)
#barplot(t(as.matrix(data)), beside=TRUE)
#library(ggplot2)
#geom_bar(aes(labels,accuracies))+geom_bar(data=data)


#barplot(data$accuracies, names = data$labels,xlab = "tone N-gram", ylab = "accuracy",main = "classification accuracy of tone Ngram shapes")
data.m <- melt(data, id.vars='labels')
ggplot(data.m, aes(labels, value)) +   
  geom_bar(aes(fill = variable), position = "dodge", stat="identity")
