library(reticulate)
library(readr)
library(tidyr)
library(ggplot2)
library(ggthemes)
library(gganimate)
library(dplyr)
library(gapminder)
library(patchwork)

getwd()
setwd("C:/Users/alexp/Desktop/Side P")

py_run_file("csvBuilder.py")

data <- read.csv("data3.csv", header = TRUE)

bet_amount <- tail(names(sort(table(data$Win.Loss....))), 1)
bet <- as.character(abs(as.numeric(bet_amount)))
plays <- as.character(nrow(data))

# create new column to track number of wins/losses
data$Win_Count <- data$Win.Loss....
data$Win_Count[data$Win_Count<0] <- -1
data$Win_Count[data$Win_Count>0] <- 1


# delete player and dealer hand amounts, those columns are irrelevant
data$Player.Hand <- NULL
data$Dealer.Hand <- NULL

#take cumulative data for win amount and win count
data[,2] <- cumsum(data[,2])
data[,4] <- cumsum(data[,4])

moneyColor <- "#009900"
winColor <- "#0099FF"

money <- paste("$",bet, sep ="")
g1_title <- paste(money, "Bets Played Through", plays, "Hands")
g2_title <- paste("Wins and Losses Through", plays, "Hands")

graph = data %>%
  ggplot(aes(x = Games.Played, y = Win.Loss....)) +
  geom_line(size = 1, alpha = 0.75, color = moneyColor) + 
  theme_solarized_2(light = FALSE) +
  labs(title = g1_title, bet, "ok", x="# of Games Played", y = "Cumulative Win/Loss ($)")


graph2 = data %>%
  ggplot(aes(x = Games.Played, y = Win_Count)) +
  geom_line(size = 1, alpha = 0.75, color = winColor) +
  theme_solarized_2(light = FALSE) +
  labs(title = g2_title, x="# of Games Played", y = "Win/Loss Count")

 
