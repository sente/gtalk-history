# coding: utf-8
import lxml
import lxml.etree
import sys
import datetime
import time
import os

def get_ms(element):
    ret = None
    for x in element.xpath(".//*"):
        if x.tag == '{google:timestamp}time':
            ret = x.get('ms')
    if ret:
        return int(ret)/1000
    else:
        return ''

def get_body(element):
    body = element.find('{jabber:client}body')
    if body is not None:
        return body.text
    else:
        return ''

def print_record(record):
    timestamp = datetime.datetime.fromtimestamp(record['ms']).isoformat()
    msg_to = record['to'].split("/")[0]
    msg_from = record['from'].split("/")[0]
    try:
        return '%s\t%s\t%s\t%s\t%s' % (record['filename'], timestamp, msg_from, msg_to, str(record['body']))
    except:
        return 'errorerrorerrorerrorerror'

def print_log(filename):

    try:
        root = lxml.etree.fromstring(open(filename).read())
    except Exception, e:
        sys.stderr.write(filename + '\n')
        sys.stderr.write(str(e))
        time.sleep(1)
        return

    for a in root.xpath('//*'):
        if a.tag == "{jabber:client}message":
            d = {}
            d['filename'] = filename
            d['from'] = a.get('from', '')
            d['to'] = a.get('to', '')
            d['ms'] = get_ms(a)
            d['body'] = get_body(a)

            print print_record(d)

    return a

if __name__ == '__main__':

    for filename in sys.argv[1:]:
        if len(open(filename).read()) == 0:
            continue
        print_log(filename)

