#!/usr/bin/env python
# encoding: utf-8
"""
    some ugly code which downloads all your chats from gmail.

    other scripts process the chats to create indexable /grepable
    chat histories
"""


import imaplib
import imaplib_connect
import datetime
import email
import email.header
import os

from imaplib_list_parse import parse_list_response

import time
import sys

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

try:
    search = sys.argv[1]
except:
    search = 'ALL'

def get_msg_body(id):

    if type(id) == type(3):
        idstr = '%s' %id
    else:
        idstr = id

    typ, msg_data = c.fetch('%s' %idstr, '(RFC822)')

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            for header in [ 'subject', 'to', 'from' ]:
                print '%-8s: %s' % (header.upper(), msg[header])

            date_tuple = email.utils.parsedate(msg.get('date'))
            timestamp = time.mktime(date_tuple)
            msgdate  = datetime.datetime.fromtimestamp(timestamp)

            msg_from = email.utils.parseaddr(msg.get('from'))[1]
            msg_to = email.utils.parseaddr(msg.get('to'))[1]
            msg_date = msgdate.strftime("%F_%H-%M-%S")

            myfile = 'chats/%s/%s.html' % (msg_from, msg_date)
            ensure_dir(myfile)
            print myfile
            open('chats/%s/%s.html' % (msg_from, msg_date) ,'w').write(response_part[1])

            #print type(msgdate), datetime.datetime.fromtuple(msgdate) #msgdate.strftime("%F_%H:%M:%S")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            return response_part[1]

c = imaplib_connect.open_connection(False, '~/.pymotw')

mailbox_name = 'wasachat'

try:
    c.select(mailbox_name, readonly=True)
    typ, msg_ids = c.search(None, search)
    print mailbox_name, typ, msg_ids

    for m in reversed([num for num in msg_ids[0].split(' ') if num]):
        try:
            print m
            open('mychats/%s.email' %m, 'w').write(get_msg_body(m))
            #print get_msg_body(m)
        except:
            print sys.exc_info()[2]
            print Exception("%r",e)
            time.sleep(5)

except:
    print 'trash'

