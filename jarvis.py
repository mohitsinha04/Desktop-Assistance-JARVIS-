import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import urllib2
import json
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
import wikipedia
import random
from time import strftime


def JarvisResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def assistant(command):
    "if statements for executing commands"

    #open subreddit Reddit
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        JarvisResponse('The Reddit content has been opened for you Sir.')

    elif 'shutdown' in command:
        JarvisResponse('Bye bye Sir. Have a nice day')
        sys.exit()

    #open website
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            JarvisResponse('The website you have requested has been opened for you Sir.')
        else:
            pass

    #greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            JarvisResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            JarvisResponse('Hello Sir. Good afternoon')
        else:
            JarvisResponse('Hello Sir. Good evening')

    elif 'help me' in command:
        JarvisResponse("""
        You can use these commands and I'll help you out:
        1. Open reddit subreddit : Opens the subreddit in default browser.
        2. Open xyz.com : replace xyz with any website name
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
        4. Tell a joke/another joke : Says a random dad joke.
        5. Current weather in {cityname} : Tells you the current condition and temperature
        7. Greetings
        8. play me a video : Plays song in your VLC media player
        9. change wallpaper : Change desktop wallpaper
        10. news for today : reads top news of today
        11. time : Current system time
        12. top stories from google news (RSS feeds)
        13. tell me about xyz : tells you about xyz
        """)


    #top stories from google news
    elif 'news for today' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:15]:
                JarvisResponse(news.title.text.encode('utf-8'))
        except Exception as e:
                print(e)

    #current weather
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='f719fc3c1496996fba0c33440cc8baea')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            JarvisResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

    #time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        JarvisResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    #send email
    elif 'email' in command:
        JarvisResponse('Who is the recipient?')
        recipient = myCommand()
        if 'david' in recipient:
            JarvisResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('mohitsinha1108@gmail.com', '*************')
            mail.sendmail('mohitsinha1108@gmail.com', 'carsvally40@gmail.com' , content)
            mail.close()
            JarvisResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            JarvisResponse('I don\'t know what you mean!')

    #launch any application
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)

        JarvisResponse('I have launched the desired application')

    #play youtube song
    elif 'play me a song' in command:
        path = '/Users/mohitsinha04/Documents/videos/'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        JarvisResponse('What song shall I play Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urllib2.urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)

            url = url_list[0]
            ydl_opts = {}

            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            vlc.play(path)

            if flag == 0:
                JarvisResponse('I have not found anything in Youtube ')

    #change wallpaper
    elif 'change wallpaper' in command:
        folder = '/Users/mohitsinha04/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = ''
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #pic from unspalsh.com
        f = urllib2.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.urlretrieve(photo, "/Users/mohitsinha04/Documents/wallpaper/a") # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        JarvisResponse('wallpaper changed successfully')

    #ask me anything
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                JarvisResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
                print(e)
                JarvisResponse(e)

JarvisResponse('Hi User, I am JARVIS and I am your desktop voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
