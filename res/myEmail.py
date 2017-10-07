import imaplib
import email
from email.parser import HeaderParser

#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
#https://github.com/awangga/outlook






#mail = imaplib.IMAP4_SSL('imap.mdycontactcenter.com')
#mail = imaplib.IMAP4('mail.mdycontactcenter.com')
#mail.login('richar.samaniego@mdycontactcenter.com','umTGdEPS')

""""""
mail = imaplib.IMAP4_SSL('mail.globalltell.com')
mail.login('gerencia@globalltell.com','@g.gt.com')
#"""

"""
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('granlinux@gmail.com','password')
"""

mail.list()

mail.select('inbox')

"""
result, data = mail.search(None, 'ALL')
ids = data[0]
id_list = ids.split()
latest_email_id = id_list[-1]
result, data = mail.fetch(latest_email_id, "(RFC822)")
"""

result, data = mail.uid('search', None, "ALL") # search and return uids instead
latest_email_uid = data[0].split()[-5]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')

raw_email = data[0][1].decode('utf-8')

email_message = email.message_from_string(raw_email)

for d in email_message:
    #print(d)
    print(d," - ",email_message[d])
"""
print("From: %s" % (email_message["From"]))
print("TO: %s\n" % (email_message["To"]))

print("FROM: Alias: %s - Email: %s" % email.utils.parseaddr(email_message['From']))
print("TO: Alias: %s - Email: %s\n" % email.utils.parseaddr(email_message['To']))


print("%s" % email.utils.parseaddr(email_message['From'])[1])
print("%s\n" % email.utils.parseaddr(email_message['To'])[1])


print("%s" % str(email.utils.parseaddr(email_message['From'])))
print(email_message["To"])
#"""



data = mail.fetch('1', '(BODY[HEADER])')
header_data = data[1][0][1].decode('utf-8')
parser = HeaderParser()
msg = parser.parsestr(header_data)
print(msg)

#print(email_message.items())


#print(raw_email)
#print(email_message)
