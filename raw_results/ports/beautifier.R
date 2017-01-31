df = read.table('raw.csv',header=T,sep=",")
df = subset(df, select=-c(threads,input,mpxerrors,mpxbtnum))
d = df

d$PORT_0 = d$PORT_0*100/d$UOPS_EXECUTED.CORE
d$PORT_1 = d$PORT_1*100/d$UOPS_EXECUTED.CORE
d$PORT_2 = d$PORT_2*100/d$UOPS_EXECUTED.CORE
d$PORT_3 = d$PORT_3*100/d$UOPS_EXECUTED.CORE
d$PORT_4 = d$PORT_4*100/d$UOPS_EXECUTED.CORE
d$PORT_5 = d$PORT_5*100/d$UOPS_EXECUTED.CORE
d$PORT_6 = d$PORT_6*100/d$UOPS_EXECUTED.CORE
d$PORT_7 = d$PORT_7*100/d$UOPS_EXECUTED.CORE

d = d[, c("name","compiler","type","PORT_0","PORT_1","PORT_2","PORT_3","PORT_4","PORT_5","PORT_6","PORT_7")]
write.csv(format(d, digits=2), 'beauty.csv',row.names=F)
