
library(tidyverse)

dt <- read_csv("ar1.csv")

arima_model <- arima(dt$ar1, order = c(1, 0, 0))
arima_model

-0.2086 * (1 - 0.8204)

mean(dt$ar1)