data <- read.csv("recommendation_results.csv")


for (i in 1:3) {
    sample_data <- data[sample(nrow(data), 200), ]
    svg(paste(paste("plot", i), "svg"))
    plot(sample_data$RealRating, sample_data$PredictedRating, main = "Real Rating vs Predicted Rating", xlab = "Real Rating", ylab = "Predicted Rating")
    abline(0, 1, col = "red")
    legend("topleft", legend = paste("MAE =", round(mae, 2)), bty = "n")
    dev.off()
}
