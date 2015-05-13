library(dplyr)
library(tau)
data_size <- 33595
tmpa <- as.data.frame(read.csv("data/nlf_0371-6635.csv"))
tmpb <- as.data.frame(read.csv("data/nlf_1458-6711.csv"))
tmpc <- as.data.frame(read.csv("data/nlf_1458-8625.csv"))
tmp <- rbind(tmpa,tmpb,tmpc)
df <- tbl_df(data.frame(list(row.index = 1:data_size)))
df$Path <- paste0("data/",tmp$ISSN,"/",tmp$Filename)
df$ISSN <- tmp$ISSN
df$Lang <- substr(tmp$Filename,1,3)
df$Year <- gsub("(....)-..-..","\\1",tmp$Date.YYYY.MM.DD.)
df$Month <- gsub("....-(..)-..","\\1",tmp$Date.YYYY.MM.DD.)
df$Day <- gsub("....-..-(..)","\\1",tmp$Date.YYYY.MM.DD.)
df$IssueNo <- tmp$Issue.No
df$PageNbr <- tmp$PageNbr
df$BindingId <- tmp$BindingId
findText <- function(x) {
	scan(x,what=character(),encoding="UTF-8",quiet=TRUE,quote=NULL)
}
df$Text <- sapply(df$Path,findText)
df$Text <- lapply(df$Text,fixEncoding,latin1=TRUE)
df$Text <- lapply(df$Text,tolower)
df$Text <- lapply(df$Text,gsub,pattern="[.:,;&*-=()/~|'+%]",replacement="")
df$Text <- lapply(df$Text,gsub,pattern="[0-9]",replacement="")
df$Length <- sapply(df$Text,length)
