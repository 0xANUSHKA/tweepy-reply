import tweepy
import time
import random
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='twitter_bot.log'
)

# Twitter API credentials redacted
CONSUMER_KEY = "your_consumer_key"
CONSUMER_SECRET = "your_consumer_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Reply messages
REPLY_MESSAGES = [
    "Tired of the caffeine crash? Try Quokka Brew - smooth energy without the jitters! 🦘☕ #QuokkaBrew",
    "Say goodbye to caffeine crashes! Quokka Brew's unique formula keeps you energized all day long. 💪 #CoffeeInnovation",
    "Experience crash-free coffee with Quokka Brew! Our special blend keeps you focused without the afternoon slump. 🎯 #QuokkaCoffee",
]

# Keywords to monitor
KEYWORDS = [
    "caffeine crash",
    "coffee crash",
    "afternoon slump",
    "energy crash",
    "coffee jitters"
]

def setup_api():
    """Set up and return Twitter API client"""
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    return client

def get_search_query():
    """Create search query from keywords"""
    return " OR ".join(f'"{keyword}"' for keyword in KEYWORDS)

def should_reply_to_tweet(tweet):
    """Check if we should reply to this tweet"""
    # Don't reply to our own tweets
    if tweet.author_id == client.get_me().data.id:
        return False
    
    # Don't reply to retweets
    if hasattr(tweet, 'referenced_tweets') and tweet.referenced_tweets:
        return False
    
    return True

def reply_to_tweet(client, tweet):
    """Reply to a tweet with a random message"""
    try:
        reply_text = random.choice(REPLY_MESSAGES)
        client.create_tweet(
            text=reply_text,
            in_reply_to_tweet_id=tweet.id
        )
        logging.info(f"Replied to tweet {tweet.id}: {reply_text}")
        return True
    except Exception as e:
        logging.error(f"Error replying to tweet {tweet.id}: {str(e)}")
        return False

def main():
    client = setup_api()
    search_query = get_search_query()
    
    # Keep track of tweets we've replied to
    replied_tweets = set()
    
    while True:
        try:
            # Search for recent tweets containing our keywords
            tweets = client.search_recent_tweets(
                query=search_query,
                max_results=100,
                tweet_fields=['author_id', 'created_at', 'referenced_tweets']
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    if tweet.id not in replied_tweets and should_reply_to_tweet(tweet):
                        if reply_to_tweet(client, tweet):
                            replied_tweets.add(tweet.id)
                            # Wait 5 minutes between replies to avoid rate limits
                            time.sleep(300)
            
            # Clean up old tweet IDs from replied_tweets set (older than 24 hours)
            current_time = datetime.now()
            replied_tweets = {tweet_id for tweet_id in replied_tweets 
                            if (current_time - datetime.fromtimestamp(tweet_id >> 22 / 1000)).days < 1}
            
            # Wait 15 minutes before next search
            time.sleep(900)
            
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            time.sleep(900)  # Wait 15 minutes before retrying

if __name__ == "__main__":
    main() 