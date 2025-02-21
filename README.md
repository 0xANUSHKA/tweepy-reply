# Marketing Twitter Bot

A Twitter bot that automatically responds to tweets about caffeine crashes with information about Quokka Brew coffee. Previously deployed during 2019-2020.

## Setup

1. Install dependencies:
   ```bash
   pip install tweepy
   ```

2. Add your Twitter API credentials to `config.py`

3. Run the bot:
   ```bash
   python twitter_auto_reply.py
   ```

## Features

- Monitors tweets for caffeine crash related keywords
- Auto-replies with randomized marketing messages
- Includes rate limiting and duplicate tweet prevention
- Logs all activities to `twitter_bot.log`

## Configuration

Edit `config.py` to customize:
- Twitter API credentials
- Marketing messages
- Search keywords

## History

This bot was actively used for Quokka Brew's social media marketing during 2019-2020. It is no longer in active deployment. 
