#! /usr/bin/env python

import urllib2
import re
import random
import signal
import sys

def sigquitHandler(signum, frame):
    print "\nage avg = " + str(total_age / counter_age)
    print "age rwrw avg = " + str(total_rwrw_num_age / total_rwrw_denum_age)
    
    print "playlist avg = " + str(total_playlists / counter_total)
    print "playlist rwrw avg = " + str(total_rwrw_num_playlists / total_rwrw_denum)
    
    print "playcount avg = " + str(total_playcounts / counter_total)
    print "playcount rwrw avg = " + str(total_rwrw_num_playcounts / total_rwrw_denum)
    
    print "id avg = " + str(total_id / counter_total)
    print "id rwrw avg = " + str(total_rwrw_num_id / total_rwrw_denum)
    
    print "degree avg = " + str(total_friends / counter_total)
    print "degree rwrw avg = " + str(total_rwrw_num_friends/ total_rwrw_denum)
    sys.exit(0)
	
signal.signal(signal.SIGINT, sigquitHandler)
signal.siginterrupt(signal.SIGINT, True)

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

#app counters
total_age = 0
counter_age = 0
total_friends = 0
total_playcounts = 0
total_playlists = 0
total_id = 0
counter_total = 0

total_rwrw_num_age = 0.0
total_rwrw_num_friends = 0.0
total_rwrw_num_playcounts = 0.0
total_rwrw_num_playlists = 0.0
total_rwrw_num_id = 0.0
total_rwrw_denum_age = 0.0
total_rwrw_denum = 0.0

while (1):
	#INFO COMMAND________________________________________________
    data = ''
    command = command_user_info.format(user, api_key)
    data = urllib2.urlopen(command).read() # data is in XML format

    ages = re.findall("<age>(.*)</age>",data)		
    playcounts = re.findall("<playcount>(.*)</playcount>", data)
    playlists = re.findall("<playlists>(.*)</playlists>", data)
    friend_ids = re.findall("<id>(.*)</id>", data)
    
    #update totals________________________________________________
    total_playcounts += int(playcounts[0])
    total_playlists += int(playlists[0])
    total_id += int(friend_ids[0])
    
    #update counters______________________________________________
    counter_total += 1
    if ages[0] is not '':
        counter_age += 1
        total_age += int(ages[0])

	#DEGREE COMMAND_______________________________________________
    data = ''	
    command = command_limit_one.format(user, 1, api_key)
    data = urllib2.urlopen(command).read() # data is in XML format
    
    #add degree
    degree = int(re.search('total="(\d+)"', data).group(1)) 
    total_friends += degree

    #update rwrw_________________________________________________
    total_rwrw_num_friends += (degree/degree)
    total_rwrw_num_playcounts += float(playcounts[0])/degree 
    total_rwrw_num_playlists += float(playlists[0])/degree
    total_rwrw_num_id += float(friend_ids[0])/degree

    total_rwrw_denum += 1.0/degree

    if ages[0] is not '':
        total_rwrw_num_age += float(ages[0])/degree
        total_rwrw_denum_age += 1.0/degree

    #friend id
    id = random.randint(1, degree)
	

    #FRIENDS COMMAND_____________________________________________
    
    #get the data for random user
    data = ''
    command = command_limit_one.format(user, id, api_key)
    data = urllib2.urlopen(command).read()

    #useful data : number of friends, age, playcount, playlists, id
    friends = re.findall("<name>(.*)</name>", data)	

    #log activity______________________________________________
    if counter_age > 0 :
        print "[counter_total, counter_age] = ["+str(counter_total)+","\
        +str(counter_age)+"] : [playcount,playlist,id,degree,age] = ["\
        +str(total_playcounts)+","+str(total_playlists)+","\
        +str(total_id)+","+str(total_friends)+","+str(total_age)+"]"

    user = friends[0]
