

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from bs4 import BeautifulSoup
from urllib.request import Request,urlopen 

import requests
import json

def find(r):

  best=[]
  magnet=[]
  d={}
  mov={}
  #r=input()
  x=r.replace(" ","+")
  for i in range(1,4):
     url=f"https://kickass.onl/usearch/{x}/{i}"

     headers = {"User-Agent":"Mozilla/5.0"}

     page_req=Request(url,headers=headers)
     page=urlopen(page_req)

     soup=BeautifulSoup(page,'html.parser')
     l=soup.find_all('td',attrs={'class':'green center'})
     link=soup.find_all('tr',attrs={'id':'torrent_latest_torrents'})
     #print (link)
     #m=soup.find('a',attrs={'data-nop':''}).get('href')
     for i,j in zip(l,link):
        print (i.text)
        try:
           b=int(i.text)
        except:
           print("error")
        best.append(b)
        #print (j.text)
        m=j.find('a',attrs={'data-nop':True}).get('href')
        #m=j.find('a',attrs={'class':'icon16', 'data-nop':True}).get('href')
        magnet.append(m[23:])

  for i in range(0,len(magnet)):
      print(magnet[i])
      print(best[i])
      d[best[i]]=magnet[i]
      print("\n")
  print(d)

  for i in sorted(d,reverse=True):
    print(i,d[i])
    mov[i]=d[i]
  movies=list(mov.values())[0:5]

  text = '\n\n'.join(map(str, movies))


  payload = {'sections':[{'name':'Section1','contents':text}]}
  headers = {'X-Auth-Token': 'abx2yzCx7vw8RuFENtUeZTnrFVA6z57q4AzhViegP'}
  post_response = requests.post(url='https://api.paste.ee/v1/pastes', json=payload, headers=headers)
  print(post_response.text)
  i=post_response.text
  print (type(i))
  id=i[7:12]
  print(f"https://paste.ee/p/{id}")

  url=f"https://paste.ee/p/{id}"

  #response = requests.put("https://api.shorte.st/v1/data/url", {"urlToShorten":url}, headers={"public-api-token": "6ecac39ce3355cfdec48dea0220b6d4e"})
  #print(response.content)
  # {"status":"ok","shortenedUrl":"http:\\/\\/sh.st\\/ryHyU"}

 # decoded_response=json.loads(response.content)
 # print(decoded_response)
 # print(list(mov.keys())[0]) 
 # f=response
 # print(type(f))
  return(url)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('''Hi! I am best link giving bot. You can download movies,anime,books,games,apps etc...
    Now type what you want🧑‍💻''')
    


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    


def echo(update, context):
   """Echo the user message."""
   #update.message.send_gif('https://giphy.com/gifs/bredenkids-construction-breden-kids-W2dHV7C4eOlvWLmpdv')
   update.message.reply_text("Working on it just wait for 1-2 mins")
   p=find(update.message.text)
   print(p)
   update.message.reply_text(p)
   update.message.reply_text('''If trying each 1-5 magnets on uTorrent doesn't maches your requirement ,then try to specify your requirement more clearly
   like adding year etc. 
   If the problem persists type /help to get help''')
           


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1455027954:AAFJntPcemEJFZmMOyZXGKfZGGA748foTGA", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
