##horizontally flips 2D digitized points for 2 camera planes##

library(dplyr) #we need this for the select() function, to search through column names and grab only those that contain the string "_X" 

fname<-file.choose() #file browser prompt, loads up the path of the target file as a string
fname_new<-paste(substr(basename(fname), 1, nchar(basename(fname))-4),"H12flip.csv",sep="") #appends a suffix to the base filename for later saving
setwd(substr(fname,1,nchar(fname)-nchar(basename(fname)))) #sets the working directory to wherever the target file lives

run<-read.csv(fname, header=TRUE) #reads in the target file, with column names
runbackup<-run #makes a copy of the original data so we can check to see if stuff worked
width<-1024 #sets the sensor width variable (1024px for CFS c-arms)
cam12Xcols<-colnames(select(run, contains("_X"))) #grabs the columns with X data and stores their names as a vector of strings

for(i in cam12Xcols){
  x_old<-run[[i]]
  x_new<-width-x_old
  run[[i]]<-x_new
} #loops through the "_X" columns containing and subtracts each x value from 1024 to flip horizontally. The original value is then replaced. [[]] is used instead of $

write.csv(run, file=fname_new, row.names=FALSE) #writes a .csv to the working directory. "row.names=FALSE" gets rid of the row index
rm(list=ls()) #optional, clears environment