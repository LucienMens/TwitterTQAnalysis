import tweepy
from datetime import datetime
from pprint import pprint
from pandas import DataFrame as df

def keys(name):
        """Return the API key from an API name."""
        keychain = {      'TwitKEY':'5EfKVV2SDVMULPE4yXXm4fQ1z',
                          'TwitSECRET':'x8lm81o6cgMlpXtNojjlY0o9Cd0wq1k2Ukrlv52De5uBCY',
                          'TwitTOKEN':'AAAAAAAAAAAAAAAAAAAAANz6LAEAAAAA0vf8%2FXo2OUFYzN1lVdfmlDQ%2Bdvl%3D5EBDkrCa5Tnl7FgaDgCq7WXZ83du6aAo1f0WjafvkVpfJS5k9',
                          'TwitTOKSEC':'yours_goes_here'}
        return keychain[name]
    
from myKeys import keys
import tweepy
# Get access to Twitter's API
auth = tweepy.OAuthHandler(keys('TwitKEY'), keys('TwitSECRET'))
auth.set_access_token(keys('TwitTOKEN'), keys('TwitTOKSEC'))
twitter = tweepy.API(auth)
# Test it on yourself
twitter.me().screen_name