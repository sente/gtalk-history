#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import re
import email
import email.parser
import dateutil.parser
import BeautifulSoup


from email.Iterators import typed_subpart_iterator
from email.header import decode_header


def getheader(header_text, default="ascii"):
    """Decode the specified header"""

    headers = decode_header(header_text)
    header_sections = [unicode(text, charset or default) for text, charset in headers]
    return u"".join(header_sections)


def get_charset(message, default="ascii"):
    """Get the message charset"""

    if message.get_content_charset():
        return message.get_content_charset()

    if message.get_charset():
        return message.get_charset()

    return default



def get_body(message,ctype='plain'):
    """Get the body of the email message which has a content_subtype of <ctype>"""

    if message.is_multipart():
        #get the plain text version only
        text_parts = [part for part in typed_subpart_iterator(message, 'text', ctype)]

        body = []
        for part in text_parts:
            charset = get_charset(part, get_charset(message))
            body.append(unicode(part.get_payload(decode=True), charset, "replace"))

        return u"\n".join(body).strip()

    else: # if it is not multipart, the payload will be a string
          # representing the message body
        body = unicode(message.get_payload(decode=True),
                       get_charset(message),
                       "replace")
        return body.strip()



def prettify(html):
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        return soup.prettify()
    except:
        return ""



def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def save_email(d):
    #ensure_dir(d['from'])
    fname = 'logs2/%s/%s.html' % (d['from'],d['date_format'])
    print fname
    ensure_dir(fname)
    f = open(fname,'w')
    f.write(d['html'].encode('utf-8','replace'))
    f.close()

    fname = 'logs2/%s/%s.xml' % (d['from'],d['date_format'])
    print fname
    ensure_dir(fname)
    f = open(fname,'w')
    f.write(d['xml'].encode('utf-8','replace'))
    f.close()

def process_email(filename):

    print filename
    msg = email.parser.Parser().parse(open(filename))

    d = {}
    d['to'] = getheader(msg.get('to'))
    d['to'] = email.utils.parseaddr(d['to'])[1]
    d['from'] = getheader(msg.get('from'))
    d['from'] = email.utils.parseaddr(d['from'])[1]

    d['date'] = getheader(msg.get('date'))
    d['msg_date'] = dateutil.parser.parse(d['date'])
    d['html'] = get_body(msg,ctype='html')
    d['xml'] = get_body(msg,ctype='xml')

    d['date_format'] = d['msg_date'].strftime('%F_%H-%M')

    save_email(d)

    return d

for f in sys.argv[1:]:
    try:
        process_email(f)
    except:
        sys.stderr.write("error with email %s\n" % f)

