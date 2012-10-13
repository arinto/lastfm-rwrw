#! /usr/bin/env python

import urllib2
import re
import random

#init some variables
command_limit_one= \
"http://ws.audioscrobbler.com/2.0/?method=user.getfriends"\
"&user={0}&limit=1&page={1}&api_key={2}"

command_user_info = \
"http://ws.audioscrobbler.com/2.0/?method=user.getinfo"\
"&user={0}&api_key={1}"

command_user_shouts = \
"http://ws.audioscrobbler.com/2.0/?method=user.getshouts"\
"&user={0}&limit={1}&api_key={2}"

api_key = 'cda9140cf81af12206d411e1d420af18' #team_amz's API Key
user = "rj"
num_users = 100
x = 0

#banned_user = "RomanRy" #or "robolover"
#user = banned_user
#command = command_user_info.format(banned_user, api_key)
#data = urllib2.urlopen(command).read()
#print data

#command = command_user_shouts.format(banned_user, 5, api_key)
#data = urllib2.urlopen(command).read()
#print data

#command = command_user_info.format(user, api_key)
#data = urllib2.urlopen(command).read()
#print data

#team_amz = "team_amz"
#command = command_user_info.format(team_amz, api_key)
#data = urllib2.urlopen(command).read()
#print data


#crawl num_users Lastfm users
while (x < num_users):

    command = command_limit_one.format(user, 1, api_key)
    data = urllib2.urlopen(command).read() # data is in XML format
    
    #learn the degree
    degree = int(re.search('total="(\d+)"', data).group(1)) 
    id = random.randint(0, degree-1)
	
    #get the data for random user
    command = command_limit_one.format(user, id, api_key)
    data = urllib2.urlopen(command).read()

    #print data

    #useful data : number of friends, age, playcount, playlists, id
    friends = re.findall("<name>(.*)</name>", data)	
    ages = re.findall("<age>(.*)</age>",data)		
    playcounts = re.findall("<playcount>(.*)</playcount>", data)
    playlists = re.findall("<playlists>(.*)</playlists>", data)
    friend_ids = re.findall("<id>(.*)</id>", data)

    print "I am", user, "and from",degree,"friends, I picked",friends[0],\
    "index", id, "friend_id", friend_ids[0],"age", ages[0], "playcount", \
    playcounts[0], "playlists", playlists[0]

    user = friends[0]
    x+=1
