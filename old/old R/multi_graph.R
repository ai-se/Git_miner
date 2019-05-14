library(plotly)

Project_Size <- c("Small", "Medium", "Large")
Hero_Developer <- c(151, 269, 569)
Non_Hero_Developer <- c(52, 60, 70)
dat <- data.frame(Project_Size, Hero_Developer, Non_Hero_Developer)

t <- list(size = 16)


p <- plot_ly(dat, x = ~Project_Size, 
             y = ~Hero_Developer, 
             type = 'bar', 
             #text = c('75.93%','83.20%','92.19%'),
             textposition = 'auto',
             name = 'Hero Developers',
             marker = list(color = c('rgba(250,112,112,1)'),line = list(color = 'rgb(0,0,0)',
                                                                        width = 1.5))) %>%
  add_trace(y = ~Non_Hero_Developer,
            name = 'Non-Hero Developer',
            #text = c('24.07%','16.80%','7.81%'), 
            textposition = 'auto', 
            marker = list(color = c('rgba(0,193,195,1)'))) %>%
  layout(yaxis = list(title = 'Count',showgrid = FALSE), barmode = 'group', font = t) 

#p <- ggplot(data=dat, aes(x=Project_Size, y=Hero_Developer, fill=Project_Size)) + 
#  geom_bar(colour="black",stat="identity",position = 'dodge',width = .5)


print(p)