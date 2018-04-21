# VADERSentiment Twitter Bot

This twitter bot uses Twitter API every 5 minutes to listen for "@Allenfp Analyze: <@namename>" where @namename is a different person's twitter handle. Once the Twitter call is detected, it performs VADER Sentiment analysis on the last 500 tweets from that account. It then produces a graph using Matplotlib that visualizes the compound sentiment score. The plot is then returned as an image attachement to a tweet.

