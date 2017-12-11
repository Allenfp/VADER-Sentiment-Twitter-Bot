import time
import matplotlib.pyplot as plt
import pandas as pd
import tweepy
import seaborn as sns
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

#Twitter API Key
consumer_key = ""
consumer_secret = ""
access_token = 	""
access_token_secret = ""

#Twitter Credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

user_history = []

# Create sentiment_function
while True:
    
    # Target Term
    search_term = "@Allenfp Analyze: "
    sentiments = []
    now = datetime.datetime.now()

    # Search for all tweets
    public_tweets = api.search(search_term, count=3, result_type="recent")

    # Loop through all tweets
    for tweet in public_tweets["statuses"]:

        # Get ID and author of most recent tweet directed to me
        target_user = tweet['text'].split(": ")[1]
        
        if target_user in user_history:

            print("Analysis Incomplete: User already exists.")

        else:

            user_history.append(target_user)
            print(user_history)
            print(target_user)

            for x in range(5):

                # Get all tweets from home feed
                target_tweets = api.user_timeline(target_user, count=100, result_type="recent", page=x+1)

                # Loop through all tweets
                for target in target_tweets:

                    text = target['text']

                    # Run Vader Analysis on each tweet
                    scores = analyzer.polarity_scores(text)

                    # Add dictionary of scores to the `sentiments` list
                    sentiments.append(scores)

            sns.set()

            sentiments_df = pd.DataFrame(sentiments)
            print(sentiments_df.head())
            print(len(sentiments_df))

            # Plot compound sentiment
            sentiments_df['compound'].plot(marker='o', linewidth=1, label=target_user)
            plt.xlabel('Tweet Number')
            plt.ylabel('Compound Score (higher is more positive')

            # Plot line for average compound score
            avg = sentiments_df['compound'].mean()
            plt.hlines(avg, 0, len(sentiments), linewidth=1, linestyle='dotted', color='red')

            plt.title(f'VADER sentiment analysis on {target_user} as of {now.strftime("%Y-%m-%d")}')
            plt.legend(title="Tweets", loc='center left', bbox_to_anchor=(1, .5), fancybox=True, shadow=True,)

            # Save graphic & post to twitter
            plt.savefig('analysis.png', bbox_inches='tight')
            plt.gcf().clear()
            api.update_with_media('analysis.png',
                      f'Behold! VADER Sentiment analysis of {target_user}')

    print("Sleeping for 5 minutes.")
    time.sleep(300)