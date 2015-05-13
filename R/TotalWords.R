write.csv(df %>% group_by(Year,ISSN) %>% summarise(TotalWords = sum(Length)),"TotalWords.csv")
