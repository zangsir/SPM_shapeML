#this script shows three ways of feature selection: redundant features; feature importance; Recursive Feature Elimination (rfe), via caret package.
#the documentation can be seen http://topepo.github.io/caret/recursive-feature-elimination.html#recursive-feature-elimination-via-caret
#the tutorial can be seen:http://machinelearningmastery.com/feature-selection-with-the-caret-r-package/


# ensure the results are repeatable
set.seed(7)
# load the library
library(mlbench)
library(caret)
# load the data
data(PimaIndiansDiabetes)
str(PimaIndianDiabetes)
# calculate correlation matrix
correlationMatrix <- cor(PimaIndiansDiabetes[,1:8])
# summarize the correlation matrix
print(correlationMatrix)
# find attributes that are highly corrected (ideally >0.75)
highlyCorrelated <- findCorrelation(correlationMatrix, cutoff=0.5)
# print indexes of highly correlated attributes
print(highlyCorrelated)


# ensure results are repeatable
set.seed(7)
# load the library
library(mlbench)
library(caret)
# load the dataset
data(PimaIndiansDiabetes)
# prepare training scheme
control <- trainControl(method="repeatedcv", number=10, repeats=3)
# train the model
model <- train(diabetes~., data=PimaIndiansDiabetes, method="lvq", preProcess="scale", trControl=control)
# estimate variable importance
importance <- varImp(model, scale=FALSE)
# summarize importance
print(importance)
# plot importance
plot(importance)



#######################################
#adapting to tone data
setwd('~/Desktop/cmn_mapping/')
tone134<-read.csv('downsample_syl_3_meta_200_134_.csv',header=TRUE)
head(tone134)
str(tone134)

#cast everything as factor as it should be
for (k in 10:38){
tone134[,k]<-as.factor(tone134[,k])
}

str(tone134)

#some variables are too sparse
table(tone134$pos1)
table(tone134$pos2)
table(tone134$pos3)
table(tone134$func1)
table(tone134$func2)
table(tone134$func3)
table(tone134$nuclear1)
table(tone134$nuclear2)
table(tone134$nuclear3)
table(tone134$prev_tone)
table(tone134$next_tone)

########################################clear some rare events
#get rid of near zero variance levels of factors
cleanZeroVar<- function(df,dfx,x){
	t<-table(dfx)
	small<-t[t<5]
	names<-dimnames(small)
	dfNew<-subset(df,!(dfx %in% names[[1]]))
	dfNew[x]<-droplevels(dfNew[x])
	return(dfNew)
	
}
#toneSub<-cleanZeroVar(tone134,tone134$nuclear2,'nuclear2')
#table(toneSub$nuclear2)
#toneSub<-cleanZeroVar(toneSub,toneSub$nuclear1,'nuclear1')
#table(toneSub$nuclear1)
#toneSub<-cleanZeroVar(toneSub,toneSub$nuclear3,'nuclear3')
#table(toneSub$nuclear3)
toneSub<-cleanZeroVar(tone134,tone134$pos2,'pos2')
table(toneSub$pos2)
toneSub<-cleanZeroVar(toneSub,toneSub$pos1,'pos1')
table(toneSub$pos1)
toneSub<-cleanZeroVar(toneSub,toneSub$pos3,'pos3')
table(toneSub$pos3)
toneSub<-cleanZeroVar(toneSub,toneSub$func2,'func2')
table(toneSub$func2)
toneSub<-cleanZeroVar(toneSub,toneSub$func1,'func1')
table(toneSub$func1)
toneSub<-cleanZeroVar(toneSub,toneSub$func3,'func3')
table(toneSub$func3)
#####################################################
str(toneSub)

#feature importance
control <- trainControl(method="repeatedcv", number=10, repeats=3)
# train the model
model <- train(label~., data=toneSub, method="lvq", preProcess="scale", trControl=control)
# estimate variable importance
importance <- varImp(model, scale=FALSE)
# summarize importance
print(importance)
# plot importance
plot(importance)



# ensure the results are repeatable
set.seed(7)
# load the library
library(mlbench)
library(caret)
# load the data
data(PimaIndiansDiabetes)
# define the control using a random forest selection function
control <- rfeControl(functions=rfFuncs, method="cv", number=10)
# run the RFE algorithm
results <- rfe(PimaIndiansDiabetes[,1:8], PimaIndiansDiabetes[,9], sizes=c(1:8), rfeControl=control)
# summarize the results
print(results)
# list the chosen features
predictors(results)
# plot the results
plot(results, type=c("g", "o"))


########################  randomForest
#http://trevorstephens.com/kaggle-titanic-tutorial/r-part-5-random-forests/
library('randomForest')
fit <- randomForest(label ~ .,data=tone134, importance=TRUE, ntree=2000)
fit
#accuracy is 56.21 with full feature set.
#accuracy is worse with toneSub1 best feature set. 
# Look at variable importance
varImpPlot(fit)



########################  S V M
#svm
library(e1071)
model<-svm(label ~ .,data=toneSub)

#create a subset of features

#feature set: without pos,func, prev,next,sent_pos 62.27, best so far
toneSub1<-toneSub[c(7,8,10:35,38)]
#removing rounding is not good:
#toneSub1<-toneSub[c(7,8,10:34,38)]
#include prev next tone:61.82
toneSub1<-toneSub[c(7,8,10:38)]

dosvm(toneSub1)
cf=confusionMatrix(toneSub$label, predict(model))
str(cf)
cf$overall[1]

#################utility function to do svm and output accuracy
str(toneSub1)
colnames(toneSub)

#function svm and accuracy
dosvm<-function(toneSub1){
model<-svm(label ~ .,data=toneSub1)
# alternatively the traditional interface:
#attach(toneSub)
x <- subset(toneSub1, select = -label)
y <- label
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
confusionMatrix(label, predict(model))
}


# it is now clear that all features without the pos and func features are giving the most performance. (sent position is also useless seems like, counter intuitive; after I removed prev and next tone, becomes better;)

