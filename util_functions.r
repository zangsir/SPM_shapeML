##################### utility functions
preprocessTone<-function(toneData){
  #cast everything as factor as it should be
  for (k in 10:38){
    toneData[,k]<-as.factor(toneData[,k])
  }
  toneSub<-cleanZeroVar(toneData,toneData$pos2,'pos2')
  #table(toneSub$pos2)
  toneSub<-cleanZeroVar(toneSub,toneSub$pos1,'pos1')
  #table(toneSub$pos1)
  toneSub<-cleanZeroVar(toneSub,toneSub$pos3,'pos3')
  #table(toneSub$pos3)
  toneSub<-cleanZeroVar(toneSub,toneSub$func2,'func2')
  #table(toneSub$func2)
  toneSub<-cleanZeroVar(toneSub,toneSub$func1,'func1')
  #table(toneSub$func1)
  toneSub<-cleanZeroVar(toneSub,toneSub$func3,'func3')
  #table(toneSub$func3)
  #try<-cleanRare(toneData,toneData$next_tone,'next_tone')
  
  toneSub<-cleanZeroVar(toneSub,toneSub$next_tone,'next_tone')
  toneSub<-cleanZeroVar(toneSub,toneSub$prev_tone,'prev_tone')
  
  #toneSub[toneSub$next_tone=='6',]$next_tone='-1'
  #toneSub$next_tone<-droplevels(toneSub$next_tone)
  #toneSub[toneSub$prev_tone=='6',]$prev_tone='-1'
  #toneSub$prev_tone<-droplevels(toneSub$prev_tone)
  return(toneSub)
}


featImp<-function(toneSub){
  
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






cleanZeroVar<-function(df,factor,name){
  df.new<-df
  for (i in 1:length(levels(factor))){
    if(table(factor)[i] < 5){
      df.new <- df[factor != names(table(factor))[i],] 
    }
  }
  df.new[name]<-droplevels(df.new[name])
  return(df.new)
}

#function svm and accuracy
dosvm<-function(toneSub1){
  model<-svm(label ~ .,data=toneSub1)
  # alternatively the traditional interface:
  #attach(toneSub)
  x <- subset(toneSub1, select = -label)
  y <- toneSub1$label
  #model <- svm(x, y) 
  
  #print(model)
  #summary(model)
  
  # test with train data
  pred <- predict(model, x)
  # (same as:)
  pred <- fitted(model)
  # Check confusion table:
  #table(pred, y)
  #accuracy report
  cf=confusionMatrix(toneSub1$label, predict(model))
  cat('\n')
  
  cat('accuracy:',as.character(cf$overall[1]))
  cat('\n')
  
  cat('lower:',as.character(cf$overall[3]))
  cat('\n')
  
  cat('upper:',as.character(cf$overall[4]))
  cat('\n')
}
