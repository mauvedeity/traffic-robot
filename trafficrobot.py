#!/usr/bin/python3

##############################################################################
#  _              __  __ _                _           _                 
# | |_ _ __ __ _ / _|/ _(_) ___ _ __ ___ | |__   ___ | |_   _ __  _   _ 
# | __| '__/ _` | |_| |_| |/ __| '__/ _ \| '_ \ / _ \| __| | '_ \| | | |
# | |_| | | (_| |  _|  _| | (__| | | (_) | |_) | (_) | |_ _| |_) | |_| |
#  \__|_|  \__,_|_| |_| |_|\___|_|  \___/|_.__/ \___/ \__(_) .__/ \__, |
#                                                          |_|    |___/ 
##############################################################################

import os.path
import xml.etree.ElementTree as etree
import urllib
import urllib.request
import urllib.parse
#
from chump import Application

##############################################################################

def global_datasource():
  return("http://m.highwaysengland.co.uk/feeds/rss/UnplannedEvents/West%20Midlands.xml")

# get current location so that we can look for files in our folder 
# TODO: fix it so we can use an arbitary r/w path for the guid and download
# files, r/o path for users (from POV of app we're running as)
# users, lastguid, download file name
#
def get_fileloc(pfile):
  # return(os.path.dirname(os.path.realpath(__file__)) + '/')
  ourpath = (os.path.dirname(os.path.realpath(__file__)) + '/')
  if(pfile == 'USERS'):
    rv = ourpath + "trafficrobot-users.txt"
  elif(pfile == 'LGUID'):
    rv = ourpath + "lastguid.txt"
  elif(pfile == 'DLOAD'):
    rv = ourpath + "web-traffic-data.xml"
  elif(pfile == 'APIKF'):
    rv = ourpath + "app-api-key.txt"
  elif(pfile == ''):
    rv = ourpath
  else:
    raise ValueError('Invalid entry in call to get_fileloc', pfile)
  return(rv)

# Get Application API key from external file
def get_appapikey():
  apikf = open(get_fileloc('APIKF'),mode='r',encoding='utf-8')
  appapikey = apikf.read()
  apikf.close()
  appapikey = appapikey.rstrip()
  print(']' + appapikey + '[')
  return(appapikey)

# check a GUID against the last seen GUIDs
def guidcheck(cguid):
  guidfile = open(get_fileloc('LGUID'),mode='r',encoding='utf-8')
  fileguid = guidfile.read()
  guidfile.close()
  return(cguid > fileguid)

# update last seen from latest GUID in the file
def guidupdate(pguid):
  guidfile = open(get_fileloc('LGUID'),mode='w',encoding='utf-8')
  fileguid = guidfile.write(pguid)
  guidfile.close()

def listusers():
  """list users present in the system. eventually should filter by road"""
  users = []
  devs = []
  names = []
  userf = open(get_fileloc("USERS"), 'r')
  lines = userf.readlines()
  for userl in lines:
    if(userl[0] != '#'):
      userl = userl[:-1]
      u,d,n = userl.split(',')
      users += [u]
      devs += [d]
      names += [n]
  userf.close()
  return(users,devs, names)

def notifyusers(title, msgtext, msgpriority):
  idx = 0;
  app = Application(get_appapikey())
  print ('Application authenticated OK: ',(app.is_authenticated))
  if(app.is_authenticated):
    usertokens, devices, friendname = listusers()
    for usertoken in usertokens:
      user = app.get_user(usertoken)
      if(user.is_authenticated):
        print(user, 'authenticated OK')
        message = user.create_message(msgtext,
          # sound = 'incoming', # uncomment for alternate sound, leave for default
          title = title,
          device = devices[idx],
          priority = msgpriority,
          html = False
        );
        message.send()
        print('Sent: ', message.is_sent, ' ID: ',message.id, ' User: ', friendname[idx]);
      else:
        print('fail: ', user, '/', friendname[idx])
      idx += 1
    print('Users notified: ', idx)
    print('Quota: ', app.remaining, '/', app.limit)
  else:
    print('App could not authenticate')

def processitem(anitem):
  road = anitem.findall('road')[0].text
  guid = anitem.findall('guid')[0].text
  priority = 0 	                                # normal priority
  if((road in ['M6']) and (guidcheck(guid))):
    cat1 = 'Incident type: ' + anitem.findall('category')[0].text
    cat2 = 'Delay category: ' + anitem.findall('category')[1].text
    description = anitem.findall('description')[0].text
    # msg = cat1 + '\n' + cat2 + '\n' + description + 'GUID: ' + guid + '\n'
    msg = description + cat1 + '\n' + cat2 + '\n' + 'GUID: ' + guid + '\n'
    # print(msg)
    # check delay and adjust priority as appropriate
    # if cat2 = 'No Delay' or 'Minor Disruption' then leave priority else priority = 1
    if(not(('No Delay' in cat2) or ('Minor Disruption' in cat2))):
      priority = 1
    if('Lane Closures' in description):	# if lane closures, then likely major delay - priority 2 # pri 2 under review
      priority = 1
    notifyusers(cat1, msg, priority)
    # 
    print(guid + ' processed')
  else:
    print('Skipping GUID ' + guid)
  return(guid)

def trafficrobot():
  # download and parse XML 
  urllib.request.urlretrieve (global_datasource(), get_fileloc('DLOAD'))
  tree = etree.parse(get_fileloc('DLOAD'))  # slurp XML into parser
  root = tree.getroot()       # get root element
  channel = root[0]           # get channel - children of this include item
  items = channel.findall('item')
  lastguid = ''
  itemscount = 0
  for pitem in items:
    thisguid = (processitem(pitem))
    if(thisguid > lastguid):
      lastguid = thisguid
    itemscount += 1
  if(itemscount > 0):
    guidupdate(lastguid)
    print("Updating GUID " + lastguid)

def test():
  notifyusers("Test", "This is a test message to check that we are working OK", 0)

if __name__ == '__main__':
  # test()
  trafficrobot()

