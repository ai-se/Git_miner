library(plotly)
library(scales)
library(reshape2)

social <- read.csv('/Users/suvodeepmajumder/Documents/AI4SE/Git_miner/new_results/Result_data_team_Social_line_graph.csv')
test_data <-
  data.frame(
    var1 = social['Hero_Developer'],
    var0 = social['Non_Hero_Developer'],
    team_number = social['team_number']
  )

test_data_long <- melt(test_data, id="team_number")
colnames(test_data_long)[colnames(test_data_long)=="value"] <- "Median_Bug_introduction_percentage"

p <- ggplot(data=test_data_long,
            aes(x=team_number, y=Median_Bug_introduction_percentage, colour=variable)) +
  geom_line() + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
                      panel.background = element_blank(), axis.line = element_line(colour = "black")) + 
  theme(text = element_text(size=15)) +  theme(legend.position="bottom") 

#+ labs(title="Buggy Commit")

p <- ggplotly(p)
print(p)
