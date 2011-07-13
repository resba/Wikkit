#!/usr/bin/python
# Wikkity IRC Bot. Built for the #bukkitwiki channel for the Bukkit Community.
# Script by Resba
# Version: 0.7-development
# http://wiki.bukkit.org/IRC/Bots/Wikkity
# License: Do not remove this original copyright for fair use. 
# Give credit where credit is due!
# Requirements: Feedparser Python Library [http://www.feedparser.org/]
#
# NOTE: All commented lines of CODE are debug messages for when something goes wrong.

# Step 1: Import all the necessary libraries.
import socket, sys, string, time, feedparser

# Step 2: Enter your information for the bot. Incl Port of IRC Server, Nick that
# the Bot will take, host (IRC server), RealName, Channel that you want the bot
# to function in, and IDENT value.
port = 6667
nick = "Wikkity"
host = 'canis.esper.net'
name =  "Nothing Short of a Miracle"
channel = '#bukkitwiki'
ident = 'ilikeoctogons'

# Now we just initialize socket.socket and connect to the server, giving out
# the bot's info to the server.
woot = socket.socket()
woot.connect ( (host, port) )
woot.send ( 'NICK ' + nick + '\r\n' )
woot.send ( 'USER ' + ident + ' ' +  ident + ' ' + ident + ' :Wikkity\r\n' )
global nameslist
lastUsed = time.time()
# Beginning the Loop here.
while 1:
    data = woot.recv ( 1204 )
    print(data)
    globalnullvalue = ""
# Command Cooldown function. Basically checks to see if its been about 5 seconds
# before someone is allowed to use another one of Wikkity's commands.
    def commandCooldown():
#        woot.send ( 'PRIVMSG '+messageable+' :Loaded commandCooldown Function \r\n' )
        if(time.time() - lastUsed) > 10:
            global lastUsed
            lastUsed = time.time()
#            woot.send ("PRIVMSG "+messageable+" :lastUsed Check Passed, now returning to command %s\r\n" % globalnullvalue)
            return 0
        else:
#            woot.send ( 'PRIVMSG '+messageable+' :Command Cooldown Active. Ignoring Command \r\n' )
            return 1
#        woot.send ( 'PRIVMSG '+messageable+' :lastUsed Check Completed \r\n' )
    def readUser():
    	if data.find ( '^' ) != -1:
    	    lastmessage = data
            global readUserName
            readUserName = lastmessage[lastmessage.find(":")+1:lastmessage.find("!")]
            messageable = readUserName
        elif data.find( '!' ) != -1:
            readUserName = globalnullvalue

# Feelin' up the channel.
    if data.find ( '376' ) != -1:
        woot.send( 'JOIN '+channel+'\r\n' )
    if data.find ( '353' ) != -1:
        nameslist = data
#        woot.send( 'PRIVMSG '+messageable+' :Found new NAMES Listing: %s\r\n' %nameslist )
    if data.find ( 'PING' ) != -1:
        woot.send( 'PONG ' + data.split() [1] + '\r\n')        	

# Checks for operator status. If person has Op OR Voice, then the person
# completely bypasses the CommandCooldown function.
    def opCheck():
        lastmessage = data
        mySubString = lastmessage[lastmessage.find(":")+1:lastmessage.find("!")]
#        woot.send ( 'PRIVMSG '+messageable+' :Last Message: %s\r\n'%mySubString )
        atsymbol = "@"
        voicesymbol = "+"
        nameslist = data
        if nameslist.find(atsymbol+mySubString) != -1:
            readUser()
#            woot.send ( 'PRIVMSG '+messageable+' :You are an op \r\n' )
            return 0
# Note: If you don't want people with Voice to have Bypass privilages
# Then comment out the next two lines.
        elif nameslist.find(voicesymbol+mySubString) != -1:
            readUser()
            return 0
        else:
#            woot.send ( 'PRIVMSG '+messageable+' :You are not an op \r\n' )
            readUser()
            if commandCooldown() == 0:
                return 0
            if commandCooldown() == 1:
                return 1
# Beginning commands below. Parsed with feedparser.

# !wiki: Checks the recent changes RSS feed at wiki.bukkit.org
    if data.find ( 'wiki' ) != -1:
        if (opCheck() == 0):
            feedurl = feedparser.parse("http://wiki.bukkit.org/index.php?title=Special:RecentChanges&feed=atom")
            newest = feedurl['items'][0]
            e = feedurl.entries[0]
            threadurl = e.link
            title = e.title
            author = e.author
            timestamp = e.updated
            summary = e.summary
            woot.send ( 'PRIVMSG '+messageable+' :-- BukkitWiki Most Recent Edit [ http://wiki.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Most Recent Change: %s\r\n" % title)
            woot.send ("PRIVMSG "+messageable+" :Author: %s\r\n" % author)
            woot.send ("PRIVMSG "+messageable+" :Summary: %s\r\n" % summary)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % threadurl)
            woot.send ("PRIVMSG "+messageable+" :Timestamp: %s\r\n" % timestamp)

# !build: Checks the most recent RECCOMENDED build of Craftbukkit from ci.bukkit.org
    if data.find ( 'build' ) != -1:
        if (opCheck() == 0):
            feedurlsophos = feedparser.parse("http://ci.bukkit.org/other/latest_recommended.rss")
            newestsophos = feedurlsophos['items'][0].title
            d = feedurlsophos.entries[0]
            sophosurl = d.link
            woot.send ( 'PRIVMSG '+messageable+' :-- Latest Recommended Craftbukkit Build [ http://ci.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" : %s\r\n" % newestsophos)
            woot.send ("PRIVMSG "+messageable+" :Download URL: %s\r\n" % sophosurl)

# !latest: Checks the most latest build of Craftbukkit  from ci.bukkit.org
    if data.find ( 'latest' ) != -1:
        if (opCheck() == 0):
            feedurlsophos = feedparser.parse("http://ci.bukkit.org/job/dev-CraftBukkit/rssAll")
            newestsophos = feedurlsophos['items'][0].title
            d = feedurlsophos.entries[0]
            sophosurl = d.link
            woot.send ( 'PRIVMSG '+messageable+' :-- Latest Craftbukkit Build [ http://ci.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Latest Build: %s\r\n" % newestsophos)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % sophosurl)

# !news: displays most recent news from a topic at forums.bukkit.org
    if data.find ( 'news' ) != -1:
        if (opCheck() == 0):
            feedurlex = feedparser.parse("http://forums.bukkit.org/forums/bukkit-news.2/index.rss")
            newestex = feedurlex['items'][0].title
            newestlink = feedurlex['items'][0].link
            woot.send ( 'PRIVMSG '+messageable+' :-- Latest Bukkit News [ http://www.bukkit.org ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Latest News: %s\r\n" % newestex)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % newestlink)
# !notch: Displays the most recent blog post from notch.tumblr.com
    if data.find ( 'notch' ) != -1:
        if (opCheck() == 0):
            feedurlex = feedparser.parse("http://notch.tumblr.com/rss")
            newestex = feedurlex['items'][0].title
            newestlink = feedurlex['items'][0].link
            woot.send ( 'PRIVMSG '+messageable+' :-- Most Recent Minecraft News from Notch [ http://notch.tumblr.com ] -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :Last Blog Post: %s\r\n" % newestex)
            woot.send ("PRIVMSG "+messageable+" :URL: %s\r\n" % newestlink)
# !help: Displays the help menu that explains all commands.
    if data.find ( 'help' ) != -1:
        if (opCheck() == 0):
            thenull = ""
            woot.send ( 'PRIVMSG '+messageable+' :-- Wikkity Help -- \r\n' )
            woot.send ("PRIVMSG "+messageable+" :!wiki: Displays Last Wiki Edit %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!build: Displays Recommended Craftbukkit Build %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!latest: Displays Latest Craftbukkit Build %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!news: Displays Current News Displayed on the HomePage of Bukkit.org %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!notch: Displays Latest Blog Post From Notch's Tumblr Account %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!rules: Displays Link to Rules %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :!rule<number>: Displays IRC Rule for that Number [1-16] %s\r\n" % thenull )
            woot.send ("PRIVMSG "+messageable+" :You can replace ! with ^ to have the command send in a Private Message! %s\r\n" % thenull )

# Command to gracefully close Wikkity and disconnect it from the
# Server. Only OPs can use this command due to opCheck
    if data.find ( 'debug.timetogo') != -1:
        thenull = ""
        if (opCheck() == 0):
            woot.send ("QUIT death to us all %s\r\n" % thenull )
            woot.close()
            sys.exit()

# !version: Displays Wikkity Version
    if data.find ( 'version' ) != -1:
        if (opCheck() == 0):
            thenull = ""
            woot.send ( 'PRIVMSG '+messageable+' :-- Wikkity Version -- \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :WikkityBot V0.7-development \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Built By resba \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :http://wiki.bukkit.org/Wikkity \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Receives feeds from sources and displays them after a certain command is run \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :Last Updated: 7/10/11 at 23:13 ET \r\n' )
# !rules: Displays rules linkout.
    if data.find ( 'rules' ) != -1:
        if (opCheck() == 0):
            thenull = ""
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rules can be found on: http://wiki.bukkit.org/IRC \r\n' )
            woot.send ( 'PRIVMSG '+messageable+' :To display a rule, type !rule<number> \r\n' )
    if data.find ( 'MODE' ) != -1:
#        woot.send ( 'PRIVMSG '+messageable+' :MODE Command Was Sent. \r\n' )
        woot.send ( 'NAMES ' + channel + ' \r\n' )

# !rule1 ~ !rule16: Displays rules for Bukkit Community IRC Channels.
    if data.find ( 'rule1' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #1 - ALWAYS READ THE TOPIC - http://wiki.bukkit.org/IRC#rule1 \r\n' )
    if data.find ( 'rule2' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #2 - We are volunteers! - http://wiki.bukkit.org/IRC#rule2 \r\n' )
    if data.find ( 'rule3' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #3 - This is not designed as a support channel! - http://wiki.bukkit.org/IRC#rule3 \r\n' )
    if data.find ( 'rule4' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #4 - Ignorance is not a valid defense. - http://wiki.bukkit.org/IRC#rule4 \r\n' )
    if data.find ( 'rule5' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #5 - No excessive usage of profanity - http://wiki.bukkit.org/IRC#rule5 \r\n' )
    if data.find ( 'rule6' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #6 - No racism, discrimination, threats, harassment or personal attacks of any kind are permitted. - http://wiki.bukkit.org/ \r\n' )
    if data.find ( 'rule7' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #7 - No vulgarity or obscenity. - http://wiki.bukkit.org/IRC#rule7 \r\n' )
    if data.find ( 'rule8' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #8 - No spamming is permitted, whatsoever. - http://wiki.bukkit.org/IRC#rule8 \r\n' )
    if data.find ( 'rule9' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #9 - No flaming, inciting hatred or instigating flame bait is permitted. - http://wiki.bukkit.org/IRC#rule9 \r\n' )
    if data.find ( 'rule10' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #10 - No selling of products or services, unless approved by a member of the channel staff. - http://wiki.bukkit.org/IRC#rule10 \r\n' )
    if data.find ( 'rule11' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #11 - Do not ask for a position on staff. - http://wiki.bukkit.org/IRC#rule11 \r\n' )
    if data.find ( 'rule12' ) != -1:
        if (opCheck() == 0):
		            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #12 - No advertising. - http://wiki.bukkit.org/IRC#rule12 \r\n' )
    if data.find ( 'rule13' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #13 - Disrespect and intolerance towards other people is NOT acceptable. - http://wiki.bukkit.org/IRC#rule13 \r\n' )
    if data.find ( 'rule14' ) != -1:
        if (opCheck() == 0):
            woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #14 - BE PATIENT and no excessive repeating - http://wiki.bukkit.org/IRC#rule14 \r\n' )		
    if data.find ( 'rule15' ) != -1:
        if (opCheck() == 0):
		    woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #15 - Pastebin logs, code snippets, anything longer than 3 lines! - http://wiki.bukkit.org/IRC#rule15 \r\n' )
    if data.find ( 'rule16' ) != -1:
        if (opCheck() == 0):
			woot.send ( 'PRIVMSG '+messageable+' :IRC Rule #16 - This is an English only channel - http://wiki.bukkit.org/IRC#rule16 \r\n' )
    

"""
#Private Messages Commands. Same documentation as above.#
    if data.find ( '^wiki' ) != -1:
        readUser()
        feedurl = feedparser.parse("http://wiki.bukkit.org/index.php?title=Special:RecentChanges&feed=atom")
#        newest = feedurl['items'][0].items
        e = feedurl.entries[0]
        threadurl = e.link
        title = e.title
        author = e.author
        timestamp = e.updated
        summary = e.summary
        woot.send ( 'PRIVMSG '+readUserName+' :-- BukkitWiki Most Recent Edit [ http://wiki.bukkit.org ] -- \r\n' )
        woot.send ('PRIVMSG '+readUserName+' :Most Recent Change: %s\r\n' % title)
        woot.send ('PRIVMSG '+readUserName+' :Author: %s\r\n' % author)
        woot.send ('PRIVMSG '+readUserName+' :Summary: %s\r\n' % summary)
        woot.send ('PRIVMSG '+readUserName+' :URL: %s\r\n' % threadurl)
        woot.send ('PRIVMSG '+readUserName+' :Timestamp: %s\r\n' % timestamp)
    if data.find ( '^latestrb' ) != -1:
        readUser()
        feedurlsophos = feedparser.parse("http://ci.bukkit.org/other/latest_recommended.rss")
        newestsophos = feedurlsophos['items'][0].title
        d = feedurlsophos.entries[0]
        sophosurl = d.link
        woot.send ( 'PRIVMSG '+readUserName+' :-- Latest Recommended Craftbukkit Build [ http://ci.bukkit.org ] -- \r\n' )
        woot.send ('PRIVMSG '+readUserName+' : %s\r\n' % newestsophos)
        woot.send ('PRIVMSG '+readUserName+' :Download URL: %s\r\n' % sophosurl)
    if data.find ( '^latest' ) != -1:
        readUser()
        feedurlsophos = feedparser.parse("http://ci.bukkit.org/job/dev-CraftBukkit/rssAll")
        newestsophos = feedurlsophos['items'][0].title
        d = feedurlsophos.entries[0]
        sophosurl = d.link
        woot.send ( 'PRIVMSG '+readUserName+' :-- Latest Craftbukkit Build [ http://ci.bukkit.org ] -- \r\n' )
        woot.send ('PRIVMSG '+readUserName+' :Latest Build: %s\r\n' % newestsophos)
        woot.send ('PRIVMSG '+readUserName+' :URL: %s\r\n' % sophosurl)
    if data.find ( '^news' ) != -1:
        readUser()
        feedurlex = feedparser.parse("http://forums.bukkit.org/forums/bukkit-news.2/index.rss")
        newestex = feedurlex['items'][0].title
        newestlink = feedurlex['items'][0].link
        woot.send ( 'PRIVMSG '+readUserName+' :-- Latest Bukkit News [ http://www.bukkit.org ] -- \r\n' )
        woot.send ('PRIVMSG '+readUserName+' :Latest News: %s\r\n' % newestex)
        woot.send ('PRIVMSG '+readUserName+' :URL: %s\r\n' % newestlink)
    if data.find ( '^notch' ) != -1:
        readUser()
        feedurlex = feedparser.parse("http://notch.tumblr.com/rss")
        newestex = feedurlex['items'][0].title
        newestlink = feedurlex['items'][0].link
        woot.send ( 'PRIVMSG '+readUserName+' :-- Most Recent Minecraft News from Notch [ http://notch.tumblr.com ] -- \r\n' )
        woot.send ('PRIVMSG '+readUserName+' :Last Blog Post: %s\r\n' % newestex)
        woot.send ('PRIVMSG '+readUserName+' :URL: %s\r\n' % newestlink)
    if data.find ( '^help' ) != -1:
        readUser()
        thenull = ""
        woot.send ( 'PRIVMSG '+readUserName+' :-- Wikkity Help -- \r\n' )
        woot.send ('PRIVMSG '+readUserName+' :!wiki: Displays Last Wiki Edit %s\r\n' % thenull )
        woot.send ('PRIVMSG '+readUserName+' :!latestrb: Displays Recommended Craftbukkit Build %s\r\n' % thenull )
        woot.send ('PRIVMSG '+readUserName+' :!latest: Displays Latest Craftbukkit Build %s\r\n' % thenull )
        woot.send ('PRIVMSG '+readUserName+' :!news: Displays Current News Displayed on the HomePage of Bukkit.org %s\r\n' % thenull )
        woot.send ('PRIVMSG '+readUserName+' :!notch: Displays Latest Blog Post From The Notch Tumblr Account %s\r\n' % thenull )
        woot.send ('PRIVMSG '+readUserName+' :!rules: Displays Link to Rules %s\r\n' % thenull )
        woot.send ('PRIVMSG '+readUserName+' :!rule<number>: Displays IRC Rule for that Number [1-16] %s\r\n' % thenull )
        woot.send ('PRIVMSG '+readUserName+' :You can replace ! with ^ to have the command send in a Private Message! %s\r\n' % thenull )
    if data.find ( '^version' ) != -1:
        readUser()
        thenull = ""
        woot.send ( 'PRIVMSG '+readUserName+' :-- Wikkity Version -- \r\n' )
        woot.send ( 'PRIVMSG '+readUserName+' :WikkityBot V0.7-development \r\n' )
        woot.send ( 'PRIVMSG '+readUserName+' :Built By resba \r\n' )
        woot.send ( 'PRIVMSG '+readUserName+' :http://wiki.bukkit.org/Wikkity \r\n' )
        woot.send ( 'PRIVMSG '+readUserName+' :Receives feeds from sources and displays them after a certain command is run \r\n' )
        woot.send ( 'PRIVMSG '+readUserName+' :Last Updated: 6/27/11 at 16:10 EST \r\n' )
    if data.find ( '^rules' ) != -1:
        readUser()
        thenull = ""
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rules can be found on: http://wiki.bukkit.org/IRC \r\n' )
        woot.send ( 'PRIVMSG '+readUserName+' :To display a rule, type !rule<number> \r\n' )
    if data.find ( '^rule1' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #1 - ALWAYS READ THE TOPIC - http://wiki.bukkit.org/IRC#rule1 \r\n' )
    if data.find ( '^rule2' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #2 - We are volunteers! - http://wiki.bukkit.org/IRC#rule2 \r\n' )
    if data.find ( '^rule3' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #3 - This is not designed as a support channel! - http://wiki.bukkit.org/IRC#rule3 \r\n' )
    if data.find ( '^rule4' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #4 - Ignorance is not a valid defense. - http://wiki.bukkit.org/IRC#rule4 \r\n' )
    if data.find ( '^rule5' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #5 - No excessive usage of profanity - http://wiki.bukkit.org/IRC#rule5 \r\n' )
    if data.find ( '^rule6' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #6 - No racism, discrimination, threats, harassment or personal attacks of any kind are permitted. - http://wiki.bukkit.org/IRC#rule6 \r\n' )
    if data.find ( '^rule7' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #7 - No vulgarity or obscenity. - http://wiki.bukkit.org/IRC#rule7 \r\n' )
    if data.find ( '^rule8' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #8 - No spamming is permitted, whatsoever. - http://wiki.bukkit.org/IRC#rule8 \r\n' )
    if data.find ( '^rule9' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #9 - No flaming, inciting hatred or instigating flame bait is permitted. - http://wiki.bukkit.org/IRC#rule9 \r\n' )
    if data.find ( '^rule10' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #10 - No selling of products or services, unless approved by a member of the channel staff. - http://wiki.bukkit.org/IRC#rule10 \r\n' )
    if data.find ( '^rule11' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #11 - Do not ask for a position on staff. - http://wiki.bukkit.org/IRC#rule11 \r\n' )
    if data.find ( '^rule12' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #12 - No advertising. - http://wiki.bukkit.org/IRC#rule12 \r\n' )
    if data.find ( '^rule13' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #13 - Disrespect and intolerance towards other people is NOT acceptable. - http://wiki.bukkit.org/IRC#rule13 \r\n' )
    if data.find ( '^rule14' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #14 - BE PATIENT and no excessive repeating - http://wiki.bukkit.org/IRC#rule14 \r\n' )
    if data.find ( '^rule15' ) != -1:
        readUser()
        woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #15 - Pastebin logs, code snippets, anything longer than 3 lines! - http://wiki.bukkit.org/IRC#rule15 \r\n' )
    if data.find ( '^rule16' ) != -1:
        readUser()
	    woot.send ( 'PRIVMSG '+readUserName+' :IRC Rule #16 - This is an English only channel - http://wiki.bukkit.org/IRC#rule16 \r\n' )

# Debug commands to help with Wikkity Development.
    if data.find ( '!debug:say' ) != -1:
        lastMessage = data
        parsedMessage = lastMessage[lastMessage.find("!debug:say")+1:lastMessage.find("~.")]
        woot.send ( 'PRIVMSG '+messageable+' :%s\r\n' % parsedMessage )
    if data.find ( '!debug:reloader' ) != -1:
        woot.send ( 'NAMES '+messageable+' \r\n' )
    if data.find ( 'MODE' ) != -1:
        woot.send ( 'PRIVMSG '+messageable+' :MODE Command Was Sent. \r\n' )
        woot.send ( 'NAMES '+messageable+' \r\n' )
    if data.find ( '!debug:lastUsed') != -1:
        woot.send ("PRIVMSG "+messageable+" :%s\r\n" % lastUsed )
    if data.find ( '!debug:time.time' ) != -1:
        woot.send ("PRIVMSG "+messageable+" :%s\r\n" % time.time() )
"""
