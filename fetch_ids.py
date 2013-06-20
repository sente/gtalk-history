import sys
import os
import imaplib
import imaplib_connect
import email


def fetch_ids_from_query(con, query):

    status, email_ids = con.search(None, query)
    if status != 'OK':
        raise Exception("Error running imap search for spinvox messages: "
                        "%s" % status)

    fetch_ids = ','.join(email_ids[0].split())
    status, data = con.fetch(fetch_ids, '(RFC822.HEADER BODY.PEEK[1])')
    if status != 'OK':
        raise Exception("Error running imap fetch for spinvox message: "
                        "%s" % status)

    for i in range(len(email_ids[0].split())):
        header_msg = email.message_from_string(data[i * 3 + 0][1])
        subject = header_msg['Subject'],
        date = header_msg['Date'],
        body = data[i * 3 + 1][1] # includes some mime multipart junk

        print i, date, subject, header_msg
        print body



def main():

    c = imaplib_connect.open_connection(False,'')

    c.select('[Gmail]/All Mail', readonly=True)
    query = '(FROM "tessello@gmail.com")'

    fetch_ids_from_query(c, query)


if __name__ == '__main__':
    main()
