library(plotly)
library(scales)
library(reshape2)

social <- read.csv('/Users/suvodeepmajumder/Documents/AI4SE/Git_miner/Project_meta.csv')

dat <- data.frame(social['name'],social['releases'])

p <- ggplot(social, aes(x=name, y=releases)) + geom_boxplot(outlier.shape = NA) + 
  scale_y_continuous(limits = quantile(dat$releases, c(0.1, 0.9)))

print(p)
