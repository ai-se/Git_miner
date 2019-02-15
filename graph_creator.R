library(plotly)
library(scales)
dat <- data.frame(
  Developer_Type = factor(c("Heroes","Non-Heroes"), levels=c("Heroes","Non-Heroes")),
  Number_Of_Projects = c(1146, 188)
)
p <- ggplot(data=dat, aes(x=Developer_Type, y=Number_Of_Projects, fill=Developer_Type)) +
  geom_bar(colour="black",stat="identity",position = 'dodge',width = .5) + 
  geom_text(aes(label=c(paste(formatC((c(1146, 188)/1334)*100, digits = 2, format = "f"), "%", sep=""))), 
                                                                          position = position_nudge(x = 0, y = 20.5)) + 
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(), axis.line = element_line(colour = "black")) + 
  theme(text = element_text(size=15)) +  theme(legend.position="bottom")

p <- ggplotly(p)
print(p)