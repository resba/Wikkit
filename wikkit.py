#!/usr/bin/python
# Wikkit IRC Bot. Built for the #bukkitwiki channel for the Bukkit Community.
# Script by resba
# Version: 1.4
# http://wiki.bukkit.org/IRC/Bots/Wikkit
# License: Do not remove this original copyright for fair use. 
# Give credit where credit is due!
# Requirements: Feedparser Python Library [http://www.feedparser.org/]
# For a base version of this bot, check out Sprokkit [https://www.github.com/resba/Sprokkit]
#
# NOTE: All commented lines of CODE are debug messages for when something goes wrong.

# Step 1: Import all the necessary libraries.
import socket, sys, string, time, feedparser

# Step 2: Enter your information for the bot. Incl Port of IRC Server, Nick that
# the Bot will take, host (IRC server), RealName, Channel that you want the bot
# to function in, and IDENT value.
port = 6667
nick = "Wikkit"
host = 'optical.esper.net'
name =  "WikkitBot"
channel = '#bukkitwiki'
ident = 'Loveitwhenweletloose'
#Nickpasscheck: 1 - The nick requires a pass. 0 - The nick does NOT require a pass.
nickpasscheck = 1
#Nickpass: Password for Nick (If required.)
nickpass = 'changeme'

#botadmin: your nick is inputted for access to debug commands such as graceful shutdown and debug messages
botadmin = 'resba'
botadmin2 = 'chrisward'

#DebugSwitch: For use when debug is needed.
debug = 0

# Now we just initialize socket.socket and connect to the server, giving out
# the bot's info to the server.
woot = socket.socket()
woot.connect ( (host, port) )
woot.send ( 'NICK ' + nick + '\r\n' )
woot.send ( 'USER ' + ident + ' 0 * :BukkitBot\r\n' )
global nameslist
global sentmessage
global messageable
messageable = ''
lastUsed = time.time()

# Beginning the Loop here.
while 1:
    data = woot.recv ( 1204 )
    print(data)
    globalnullvalue = ""

# Feelin' up the channel.
    if data.find ( '376' ) != -1:
        woot.send( 'JOIN '+channel+'\r\n' )
    if data.find ( '353' ) != -1:
        nameslist = data
        if (debug == 1):
            woot.send( 'PRIVMSG '+channel+' :Found new NAMES Listing: %s\r\n' %nameslist )
    if data.find ( 'PING' ) != -1:
        woot.send( 'PONG ' + data.split() [1] + '\r\n');
    if (nickpasscheck == 1):
        if data.find ( 'NickServ!' ) != -1:
            woot.send ( 'PRIVMSG NickServ :IDENTIFY '+nick+' '+nickpass+'\r\n' )
            nickpasscheck = 0
    def filterResponse():
        sentmessage = data
        if (debug == 1):
            woot.send ( 'PRIVMSG '+channel+' :Loaded filterResponse Function with '+sentmessage+' as the trigger. \r\n' )
        #The command has been called. First check to see what type of command was called.
        if data.find ( ':!' ) != -1:
            global messageable 
            messageable = channel
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :The command was an announement ! \r\n' )
            #The command was an announcement. now we check for privilages.
            mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            if (debug == 1):
                woot.send ( 'PRIVMSG '+channel+' :Last Message: %s\r\n'%mySubString )
            atsymbol = "@"
            voicesymbol = "+"
            #If the nameslist variable contains the user with some sort of privilage. The check ends and returns to the command.
            if nameslist.find(atsymbol+mySubString) != -1:           
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are an op \r\n' )
                #because this is a global filter, the messageable is named the channel because its an announcement.
                return 0
            elif nameslist.find(voicesymbol+mySubString) != -1:
                if (debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are voiced \r\n' )
                return 0
            else:
                #If the user is NOT privilidged, then they need to jump through a few more hoops.
                if(debug == 1):
                    woot.send ( 'PRIVMSG '+channel+' :You are not a privilidged user \r\n' )
                if(time.time() - lastUsed) > 10:
                    global lastUsed
                    lastUsed = time.time()
                    if (debug == 1):
                        woot.send ('PRIVMSG '+channel+' :lastUsed Check Passed, now returning to command \r\n' )
                    return 0
                else:
                    if (debug == 1):
                        woot.send ( 'PRIVMSG '+channel+' :Command Cooldown Active. Ignoring Command \r\n' )
                    return 1
        elif data.find ( ':^' ) != -1:
            #The Command was a Privmsg, so we send the privmsg.
            global readUserName
            readUserName = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
            global messageable 
            messageable = readUserName
            return 0
# Beginning commands below. Parsed with feedparser.

# !wiki: Checks the recent changes RSS feed at wiki.bukkit.org
    if data.find ( 'bwiki' ) != -1:
        if (filterResponse() == 0):
            feedurl = feedparser.parse("http://wiki.bukkit.org/index.php?title=Special:RecentChanges&feed=atom")
            newest = feedurl['items'][0]
            e = feedurl.entries[0]
            threadurl = e.link
            title = e.title
            author = e.author
            timestamp = e.updated
            summary = e.summary
            summarya = summary.replace('<p>','')
            summaryb = summarya.replace('</p>','')
            woot.send ( 'PRIVMSG '+messageable+' :-- BukkitWiki Most Recent Edit [ http://wiki.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Most Recent Change: %s\r\n" % title)
            woot.send ("PRIVMSG "+messageable+" :Author: %s\r\n" % author)
            woot.send ("PRIVMSG "+messageable+" :Summary: %s\r\n" % summaryb)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % threadurl)
            woot.send ("PRIVMSG "+messageable+" :Timestamp: %s\r\n" % timestamp)

# !build: Checks the most recent RECCOMENDED build of Craftbukkit from ci.bukkit.org
    if data.find ( 'build' ) != -1:
        if (filterResponse() == 0):
            feedurlsophos = feedparser.parse("http://ci.bukkit.org/other/latest_recommended.rss")
            newestsophos = feedurlsophos['items'][0].title
            d = feedurlsophos.entries[0]
            sophosurl = d.link
            woot.send ( 'PRIVMSG '+messageable+' :-- Latest Recommended Craftbukkit Build [ http://ci.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" : %s\r\n" % newestsophos)
            woot.send ("PRIVMSG "+messageable+" :Download URL: %s\r\n" % sophosurl)

    if data.find ( 'cbtweet' ) != -1:
        if (filterResponse() == 0):
            cbrss = feedparser.parse("http://www.twitter.com/statuses/user_timeline/craftbukkit.rss")
            n = cbrss['items'][0]
            #e = cbrss.entries[0]
            t = n.title
            #d = n.published
            l = n.link
            woot.send ( 'PRIVMSG '+messageable+' :-- Craftbukkit Twitter [ http://www.twitter.com/Craftbukkit ] -- \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' : %s\r\n' % t)
            woot.send ( 'PRIVMSG '+messageable+' : %s\r\n' % l)
            #woot.send ( 'PRIVMSG '+messageable+' : Time Published: %s\r\n' % d)            

# !latest: Checks the most latest build of Craftbukkit  from ci.bukkit.org
    if data.find ( 'latest' ) != -1:
        if (filterResponse() == 0):
            feedurlsophos = feedparser.parse("http://ci.bukkit.org/job/dev-CraftBukkit/rssAll")
            newestsophos = feedurlsophos['items'][0].title
            d = feedurlsophos.entries[0]
            sophosurl = d.link
            woot.send ( 'PRIVMSG '+messageable+' :-- Latest Craftbukkit Build [ http://ci.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Latest Build: %s\r\n" % newestsophos)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % sophosurl)

# !news: displays most recent news from a topic at forums.bukkit.org
    if data.find ( 'news' ) != -1:
        if (filterResponse() == 0):
            feedurlex = feedparser.parse("http://forums.bukkit.org/forums/bukkit-news.2/index.rss")
            newestex = feedurlex['items'][0].title
            newestlink = feedurlex['items'][0].link
            woot.send ( 'PRIVMSG '+messageable+' :-- Latest Bukkit News [ http://www.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Latest News: %s\r\n" % newestex)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % newestlink)
# !notch: Displays the most recent blog post from notch.tumblr.com
    if data.find ( 'notch' ) != -1:
        if (filterResponse() == 0):
            feedurlex = feedparser.parse("http://notch.tumblr.com/rss")
            newestex = feedurlex['items'][0].title
            newestlink = feedurlex['items'][0].link
            woot.send ( 'PRIVMSG '+messageable+' :-- Most Recent Minecraft News from Notch [ http://notch.tumblr.com ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Last Blog Post: %s\r\n" % newestex)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % newestlink)
# !help: Displays the help menu that explains all commands.
    if data.find ( 'help' ) != -1:
        if (filterResponse() == 0):
            thenull = ""
            woot.send ( 'PRIVMSG '+messageable+' :-- Wikkit Help -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :!bwiki: Displays Last Wiki Edit %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!build: Displays Recommended Craftbukkit Build %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!latest: Displays Latest Craftbukkit Build %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!news: Displays Current News Displayed on the HomePage of Bukkit.org %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!notch: Displays Latest Blog Post From Notch's Tumblr Account %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!rules: Displays Link to Rules %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!cbtweet: Displays Link to Rules %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!rule<number>: Displays IRC Rule for that Number [1-16] %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :You can replace ! with ^ to have the command send in a Private Message! %s\r\n" % thenull )
# !version: Displays Wikkity Version
    if data.find ( 'version' ) != -1:
        if (filterResponse() == 0):
            thenull = ""
            woot.send ( 'PRIVMSG '+messageable+' :-- Wikkit Version -- \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Wikkit v1.4 b17 \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Built By resba \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :http://wiki.bukkit.org/IRC/Bots/Wikkit \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :http://dev.resbah.com:8080/job/Wikkit \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Receives feeds from sources and displays them after a certain command is run \r\n' )
# !rules: Displays rules linkout.
    if data.find ( 'rule' ) != -1:
        if (filterResponse() == 0):
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-1] == 'e'):
                woot.send ( 'PRIVMSG '+messageable+' :IRC Rules can be found on: http://wiki.bukkit.org/IRC \r\n' )
                woot.send ( 'PRIVMSG '+messageable+' :To display a rule, type !rule<number> \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 1'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #1 - ALWAYS READ THE TOPIC - http://wiki.bukkit.org/IRC#rule1 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 2'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #2 - We are volunteers! - http://wiki.bukkit.org/IRC#rule2 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 3'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #3 - This is not designed as a support channel! - http://wiki.bukkit.org/IRC#rule3 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 4'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #4 - Ignorance is not a valid defense. - http://wiki.bukkit.org/IRC#rule4 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 5'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #5 - No excessive usage of profanity - http://wiki.bukkit.org/IRC#rule5 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 6'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #6 - No racism, discrimination, threats, harassment or personal attacks of any kind are permitted. - http://wiki.bukkit.org/ \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 7'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #7 - No vulgarity or obscenity. - http://wiki.bukkit.org/IRC#rule7 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 8'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #8 - No spamming is permitted, whatsoever. - http://wiki.bukkit.org/IRC#rule8 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == ' 9'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #9 - No flaming, inciting hatred or instigating flame bait is permitted. - http://wiki.bukkit.org/IRC#rule9 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == '10'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #10 - No selling of products or services, unless approved by a member of the channel staff. - http://wiki.bukkit.org/IRC#rule10 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == '11'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #11 - Do not ask for a position on staff. - http://wiki.bukkit.org/IRC#rule11 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == '12'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #12 - No advertising. - http://wiki.bukkit.org/IRC#rule12 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == '13'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #13 - Disrespect and intolerance towards other people is NOT acceptable. - http://wiki.bukkit.org/IRC#rule13 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == '14'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #14 - BE PATIENT and no excessive repeating - http://wiki.bukkit.org/IRC#rule14 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == '15'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #15 - Pastebin logs, code snippets, anything longer than 3 lines! - http://wiki.bukkit.org/IRC#rule15 \r\n' )
            if (sentmessage[sentmessage.find(':')+len(sentmessage)-2]+sentmessage[sentmessage.find(':')+len(sentmessage)-1] == '16'):
            	woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #16 - This is an English only channel - http://wiki.bukkit.org/IRC#rule16 \r\n' )
    if data.find ( 'MODE' ) != -1:
        if (debug == 1):
            woot.send ( 'PRIVMSG '+channel+' :MODE Command Was Sent. \r\n' )
        woot.send ( 'NAMES ' + channel + ' \r\n' )
        
    # debugGrace Checking Command
    def debugGrace():
        global messageable
        if (messageable == ''):
            messageable = channel
        if (debug == 1):
            woot.send('PRIVMSG '+messageable+' :debugGrace() has been loaded \r\n' )
        sentmessage = data
        mySubString = sentmessage[sentmessage.find(":")+1:sentmessage.find("!")]
        if (mySubString == botadmin or mySubString == botadmin2):
            if(debug == 1):
                woot.send('PRIVMSG '+messageable+' :You are one of the predefined users who can use this command. debugGrace() returns 1 \r\n' )
            return 1
        else:
            if(debug == 1):
                woot.send('PRIVMSG '+messageable+' :You are one of the predefined users who can use this command. debugGrace() returns 0 \r\n' )
            return 0
# Command to gracefully close Wikkit and disconnect it from the
# Server.
    if data.find ( '!debug.timetogo') != -1:
        thenull = ""
        if (debugGrace() == 1):
            woot.send ("QUIT :I have been Deadeded. %s\r\n" % thenull )
            woot.close()
            sys.exit()
#Toggles Debug
    if data.find ( '!debug.debug') != -1:
        if (debugGrace()==1):
            if (debug == 0):
                debug = 1
                woot.send ('PRIVMSG '+messageable+' :Debug is ON \r\n')
            elif (debug == 1):
                debug = 0
                woot.send ('PRIVMSG '+messageable+' :Debug is OFF \r\n')
#Fun debug commands
    if data.find ( '!debug.reloader' ) != -1:
        if (debugGrace()==1):
            woot.send ( 'NAMES '+messageable+' \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Boom! \r\n')
    if data.find ( '!debug.lastUsed') != -1:
        if (debugGrace()==1):
            woot.send ('PRIVMSG '+messageable+' :%s\r\n' % lastUsed )
    if data.find ( '!debug.join') != -1:
        if (debugGrace()==1):
       	    channelist = sentmessage[sentmessage.find("#")+1:sentmessage.find(".")
            woot.send ('JOIN '+channelist+' \r\n' )
    if data.find ( '!debug.time.time' ) != -1:
        if (debugGrace()==1):
            woot.send ('PRIVMSG '+messageable+' :%s\r\n' % time.time() )

