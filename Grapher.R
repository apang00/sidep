# library(reticulate)
# py_run_file("csvBuilder.py")
library(readr)
library(tidyr)
library(ggplot2)
library(ggthemes)
library(gganimate)

getwd()
setwd("C:/Users/alexp/Desktop/Side P")

data <- read.csv("data.csv", header = TRUE)
data$Player.Hand <- NULL
data$Dealer.Hand <- NULL
data[,2] <- cumsum(data[,2])

  
  

graph = data %>%
  ggplot(aes(x = Games.Played, y = Win.Loss....)) +
  geom_line(size = 2, alpha = 0.75) + theme_solarized_2(light = FALSE) + 
  labs(title = "Edit This", x="# of Games Played", y = "Cumulative Win/Loss ($)")

graph.animation = graph + transition_reveal(Games.Played)

  