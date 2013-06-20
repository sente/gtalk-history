# coding: utf-8
import email
import quopri
import os
import lxml
import lxml.etree
import sys



def prettify_xml(email_file):

    try:
        txt = open(email_file).read()
    except Exception, e:
        sys.stderr.write(email_file + '\n' +  str(e))
        return ''

    msg = email.message_from_string(txt)
    walks = list(msg.walk())

    res = []
    for w in walks:
        if w.get_content_type() == 'text/xml':
            if 'quoted-printable' in w.values():
                payload = quopri.decodestring(w.get_payload())
            else:
                payload = w.get_payload()
            root = lxml.etree.fromstring(payload)
            res.append(lxml.etree.tostring(root, pretty_print=True))

    if len(res) == 1:
        return res[0]
    else:
        return ''


def process_files(files):
    for i, filename in enumerate(files):
        basefilename = os.path.basename(filename)
        ofile = os.path.join('xmls/%s' % basefilename.replace('.email','.xml'))
        try:
            ar = prettify_xml(filename)
            open(ofile, 'w').write(ar)
            sys.stdout.write('%d\t%s\t%s\t%d\n' % (i, filename, ofile, len(ar)))
        except Exception, e:
            sys.stderr.write(filename + '\n')
            sys.stderr.write(str(e) + '\n')
            #raise Exception(e)



if __name__ == '__main__':

    process_files(sys.argv[1:])

