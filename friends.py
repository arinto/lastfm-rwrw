#! /usr/bin/env python

import urllib2
import re
import random
import signal
import sys
import datetime
import time
from sys import stdout
from datetime import datetime

def robustRead(command_to_send):
    data = ''
    while True:
        success_read = True
        try:
            data = urllib2.urlopen(command_to_send).read() # data is in XML format
        except:
            success_read = False
        
        if success_read == True and data != None and data != '':
            break
        else:
            init_strings = "\n\n" + str(datetime.now()) + " RETRY"
            printStats(init_strings)
            time.sleep(3)
    
    return data

def printStats(total_strings):
    total_strings += "\ntotal samples = " + str(counter_total)
    total_strings += "\ntotal age samples = " + str(counter_age)
   
    if counter_total == 0 or counter_age == 0:
        return

    total_strings += "\nage avg = " + str(float(total_age) / counter_age)
    total_strings += "\nage rwrw avg = " + str(total_rwrw_num_age \
    / total_rwrw_denum_age)

    total_strings += "\nplaylist avg = " + str(float(total_playlists)\
    / counter_total)
    total_strings += "\nplaylist rwrw avg = " + str(total_rwrw_num_playlists\
    / total_rwrw_denum)

    total_strings += "\nplaycount avg = " + str(float(total_playcounts)\
    / counter_total)
    total_strings += "\nplaycount rwrw avg = " + str(total_rwrw_num_playcounts\
    / total_rwrw_denum)

    total_strings += "\nid avg = " + str(float(total_id) / counter_total)
    total_strings += "\nid rwrw avg = " + str(total_rwrw_num_id\
    / total_rwrw_denum)

    total_strings += "\ndegree avg = " + str(float(total_friends) \
    / counter_total)
    total_strings += "\ndegree rwrw avg = " + str(total_rwrw_num_friends \
    / total_rwrw_denum)

    #separate IO for accumulated information
    try:
        total_file = open("total.log", "a")
        try:
            total_file.write(total_strings)
        finally:
            total_file.close()
    except IOError:
        pass

def printTempStats():
    init_strings = "\n\n" + str(datetime.now()) + " TEMP"
    printStats(init_strings)

def sigquitHandler(signum, frame):
    init_strings = "\n\n" + str(datetime.now()) + " END"
    printStats(init_strings)
    stdout.write("\n")
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
new_user = user = "rj"
degree = 0

#init some files
try:
    log_file = open("counter.log", "a")
    user_select_log_file = open("select.log", "a")
    total_file = open("total.log", "a")
    try:
        start_str = "\n\n" + str(datetime.now()) + " START"
        log_file.write(start_str)
        user_select_log_file.write(start_str)
        total_file.write(start_str)
    finally:
        log_file.close()
        user_select_log_file.close()
        total_file.close()
except IOError:
    pass

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

#init string
print_string = ''
print_user_choose_string = ''

#while (1):
while (counter_total < 100000):
    #DEGREE COMMAND
    data = '' #flush
    command = command_limit_one.format(new_user, 1, api_key)
    data = robustRead(command)
    
    #add degree__________________________________________________
    new_degree = int(re.search('total="(\d+)"', data).group(1))
    if new_degree > 0: #only process new_user when new_ degree > 0
        degree = new_degree
        user = new_user

        #INFO COMMAND________________________________________________
        data = '' #flush
        command = command_user_info.format(user, api_key)
        data = robustRead(command)

        ages = re.findall("<age>(.*)</age>",data)		
        playcounts = re.findall("<playcount>(.*)</playcount>", data)
        playlists = re.findall("<playlists>(.*)</playlists>", data)
        friend_ids = re.findall("<id>(.*)</id>", data)

        #update totals_______________________________________________
        total_playcounts += int(playcounts[0])
        total_playlists += int(playlists[0])
        total_id += int(friend_ids[0])

        #update counters_____________________________________________
        counter_total += 1
        if ages[0] is not '':
            counter_age += 1
            total_age += int(ages[0])

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
        
        #log activity_____________________________________________
        print_one = "[counter_total, counter_age] = ["+str(counter_total)+","\
        +str(counter_age)+"] : [playcount,playlist,friend_id,degree,age] = ["\
        +str(total_playcounts)+","+str(total_playlists)+","\
        +str(total_id)+","+str(total_friends)+","+str(total_age)+"]\n"
        #print print_one
        print_string += print_one
    else:
        print_degree_zero =  '\n' + new_user + ' has degree 0!, '\
         + user + ' will choose another random friend'
        print_user_choose_string += print_degree_zero

    #friend id
    friend_id = random.randint(1, degree)

    #FRIENDS COMMAND_____________________________________________
    #get random friend from 'user' for next iteration
    #note that 'user' is only updated when selected friend has degree > 0
    data = ''
    command = command_limit_one.format(user, friend_id, api_key)
    data = robustRead(command)
    
    friends = re.findall("<name>(.*)</name>", data)	

    print_user_choose = "\n{0:24} --> {1:24}".format(user, friends[0])
    print_user_choose_string += print_user_choose
    
    new_user = friends[0]

    #write log according to IO interrupt quantity
    #(how many terminal or disk writes interrupts)
    if counter_total % 5 == 0:
        #stdout.write("%d samples\n" % counter_total)
        stdout.write("\r%d samples" % counter_total)
        stdout.flush()
    if counter_total%100 == 0:
        try:
            log_file = open("counter.log", "a")
            user_select_log_file = open("select.log", "a")
            printTempStats()
            try:
                 log_file.write(print_string)
                 user_select_log_file.write(print_user_choose_string)
            finally:
                 log_file.close()
                 user_select_log_file.close()
        except IOError:
            pass
        print_string = ''
        print_user_choose_string = ''

sigquitHandler(1,1);
