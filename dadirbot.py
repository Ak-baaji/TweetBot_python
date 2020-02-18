#Autor Abdulkadir M.Hassen Baaji
# 10/23/19
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import tweepy as dadir
# TwitterBot to login automaticlly and like tweets
class TwitterBot:
    def __init__(self, email , password):
        self.email = email
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get("https://twitter.com/")
        email = bot.find_elements_by_class_name('email-input')
        password = bot.find_elements_by_class_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.email)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)
    def like_tweet(self,hashtag):
        bot = self.bot
        bot.get('https:twitter.com/search?q='+hashtag+'&src=typd')
        time.sleep(3)
        for i in range(1,3):
            bot.execute_script('windows.scrollTo(0,document.body.scrollHeight)')
            time.sleep(3)
            tweets = bot.find_elements_by_class_name('tweet')
            links = [elem.get_attribut('data-permalink-path')for elem in tweets]
            print(links)
        for link in links:
            bot.get('https://twitter.com' + link)
            try:
                bot.find_element_by_class_name('HeartAnimation').click()
                time(10)
            except Exception as ex:
                time.sleep(60)

baaji = TwitterBot('email','password')
baaji.login()
baaji.like_tweet('webdevelopment')
# TwitterBot for to reply tweet and store last seen id then response it back !
CONSUMER_KEY =  ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = dadir.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = dadir.API(auth)
try:
    api.verify_credentials()
    print('Authentication OK')
except:
    print('Error during authentication!')

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#helloworld' in mention.full_text.lower():
            print('found #helloworld!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    '#HelloWorld back to you!', mention.id)
while True:
    reply_to_tweets()
    time.sleep(15)
