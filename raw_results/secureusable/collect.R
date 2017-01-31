# read all tables, group, and count NaN values
# NOTE: this seems tricky in Python + Pandas, so here's a solution in R
library(reshape)

# PARSEC BNDPRESERVE=0
df = read.table("parsec/raw.csv", header=T, sep=",")
df = aggregate(time ~ compiler + type, data=df, function(x) {sum(is.na(x))}, na.action = NULL)
df$bndpreserve=0
df$name="parsec"
write.table(df, "raw.csv", append=F, sep=",", col.names=T, row.names=F)

# PARSEC BNDPRESERVE=1
df = read.table("parsec_bndpreserve1/raw.csv", header=T, sep=",")
df = aggregate(time ~ compiler + type, data=df, function(x) {sum(is.na(x))}, na.action = NULL)
df$bndpreserve=1
df$name="parsec"
write.table(df, "raw.csv", append=T, sep=",", col.names=F, row.names=F)

# Phoenix BNDPRESERVE=0
df = read.table("phoenix/raw.csv", header=T, sep=",")
df = aggregate(time ~ compiler + type, data=df, function(x) {sum(is.na(x))}, na.action = NULL)
df$bndpreserve=0
df$name="phoenix"
write.table(df, "raw.csv", append=T, sep=",", col.names=F, row.names=F)

# Phoenix BNDPRESERVE=1
df = read.table("phoenix_bndpreserve1/raw.csv", header=T, sep=",")
df = aggregate(time ~ compiler + type, data=df, function(x) {sum(is.na(x))}, na.action = NULL)
df$bndpreserve=1
df$name="phoenix"
write.table(df, "raw.csv", append=T, sep=",", col.names=F, row.names=F)

# SPEC BNDPRESERVE=0
df = read.table("spec/raw.csv", header=T, sep=",")
df = aggregate(time ~ compiler + type, data=df, function(x) {sum(is.na(x))}, na.action = NULL)
df$bndpreserve=0
df$name="spec"
write.table(df, "raw.csv", append=T, sep=",", col.names=F, row.names=F)

# SPEC BNDPRESERVE=1
df = read.table("spec_bndpreserve1/raw.csv", header=T, sep=",")
df = aggregate(time ~ compiler + type, data=df, function(x) {sum(is.na(x))}, na.action = NULL)
df$bndpreserve=1
df$name="spec"
write.table(df, "raw.csv", append=T, sep=",", col.names=F, row.names=F)

# add security levels
df = read.table("raw.csv", header=T, sep=",")
df$securitylevel=-1
df$securitylevel[df$type =="native"] = 0
df$securitylevel[df$bndpreserve==0 & df$type =="mpx_no_narrow_bounds_only_write"] = 1
df$securitylevel[df$bndpreserve==0 & df$type =="mpx_no_narrow_bounds"] = 2
df$securitylevel[df$bndpreserve==0 & df$type =="mpx_only_write"] = 3
df$securitylevel[df$bndpreserve==0 & df$type =="mpx"] = 4
df$securitylevel[df$bndpreserve==0 & df$type =="mpx_first_field"] = 5
df$securitylevel[df$bndpreserve==1] = 6

wide = data.frame(cast(df, securitylevel + compiler + type + bndpreserve~name, value=c('time')))

wide$total = wide$parsec + wide$phoenix + wide$spec
wide = wide[order(wide$compiler,wide$securitylevel),]
write.table(wide, "raw2.csv", append=F, sep=",", col.names=T, row.names=F)
