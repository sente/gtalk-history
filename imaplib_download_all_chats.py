#!/usr/bin/env python
# encoding: utf-8

import imaplib
import imaplib_connect
import datetime
import email
import email.header
import os
import time
import sys

from imaplib_list_parse import parse_list_response


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def get_msg_body(c, id):

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




def main():

    try:
        search = sys.argv[1]
    except:
        search = 'ALL'

    c = imaplib_connect.open_connection(False, './.pymotw')

    mailbox_name = '[Gmail]/Chats'

    try:
        #num = c.select(mailbox_name, readonly=True)
        typ, msg_ids = c.select(mailbox_name, readonly=True)
        print mailbox_name, typ, msg_ids

        print msg_ids[0]

        for i in range(int(msg_ids[0])):
            print i

        arraynum = list(reversed([num for num in range(int(msg_ids[0]) ) if isinstance(num, int)]))
        for m in arraynum:
            try:
                print m
                open('mychats/%s.email' %m, 'w').write(get_msg_body(c, m))
            except Exception, e:
                sys.stderr.write(str(e))

    except Exception, e:
        sys.stderr.write(str(e))
        print 'trash'


if __name__ == '__main__':
    main()

