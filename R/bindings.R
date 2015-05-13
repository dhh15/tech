library(dplyr)
library(tau)
bin <- df %>% group_by(BindingId) %>% tally(sort=TRUE)
binn <- rapply(bin[1],c)
n_vol <- length(binn)
vol <- tbl_df(data.frame(list(row.index = 1:n_vol)))
vol$Year <- rep(NA,n_vol)
vol$Month <- rep(NA,n_vol)
vol$Day <- rep(NA,n_vol)
vol$Lang <- rep(NA,n_vol)
vol$Text <- rep(NA,n_vol)
for (i in 1:n_vol) {
	id <- binn[i]
	vol$BindingId[i] <- id
	vol$Year[i] <- (df %>% filter(BindingId == id))$Year[1]
	vol$Month[i] <- (df %>% filter(BindingId == id))$Month[1]
	vol$Day[i] <- (df %>% filter(BindingId == id))$Day[1]
	vol$Lang[i] <- (df %>% filter(BindingId == id))$Lang[1]
	vol$Text[i] <- toString(rapply((df %>% filter(BindingId == id))$Text,c))
}
saveRDS(vol,"vol.Rds")
