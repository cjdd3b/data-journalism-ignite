library(ggplot2)

googledata = read.csv("report_modified.csv")
p <- ggplot(googledata, aes(x=week, y=count, group=type))
p + geom_line(aes(color=type)) + opts(title="Google Trends: data journalism vs. data science")