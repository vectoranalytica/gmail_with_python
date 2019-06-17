# import smtplib
# import time
# import imaplib
# import email


# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

# SMTP_SERVER = 'imap.gmail.com'
# FROM_EMAIL = 'vectoranalytica2016@gmail.com'
# FROM_PWD = 'aAch71340*@Q'


# def getMsgs(servername="myimapserverfqdn"):
#   usernm = getpass.getuser()
#   passwd = getpass.getpass()
#   subject = 'Your SSL Certificate'
#   conn = imaplib.IMAP4_SSL(servername)
#   conn.login(usernm,passwd)
#   conn.select('Inbox')
#   typ, data = conn.search(None,'(UNSEEN SUBJECT "%s")' % subject)
#   for num in data[0].split():
#     typ, data = conn.fetch(num,'(RFC822)')
#     msg = email.message_from_string(data[0][1])
#     typ, data = conn.store(num,'-FLAGS','\\Seen')
#     yield msg

#
# def read_email_from_gmail():
#     try:
#         mail = imaplib.IMAP4_SSL(SMTP_SERVER)
#         mail.login(FROM_EMAIL, FROM_PWD)
#         mail.select('inbox')
#
#         type, data = mail.search(None, 'ALL')
#         mail_ids = data[0]
#
#         id_list = [str(v) for v in mail_ids.split()]
#
#         print(id_list)
#
#         for m in mail_ids[:4]:
#             typ, data = mail.fetch(m,'(RFC822)')
#             print(data[0][1])
#             # for response_part in data:
#             #     if isinstance(response_part, tuple):
#             #         msg = email.message_from_string(response_part[1])
#             #         email_subject = msg['subject']
#             #         email_from = msg['from']
#             #         print('From : ' + email_from + '\n')
#             #         print('Subject : ' + email_subject + '\n')
#
#     except:
#         raise

# https://stackoverflow.com/questions/2230037/how-to-fetch-an-email-body-using-imaplib-in-python
import datetime
import email
import imaplib
import mailbox

EMAIL_ACCOUNT = "vectoranalytica2016@gmail.com"
PASSWORD = "aAch71340*@Q"

def main():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "UNSEEN")  # (ALL/UNSEEN)
    i = len(data[0].split())

    for x in range(i):
        mail_dict = {}
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # result, email_data = conn.store(num,'-FLAGS','\\Seen')
        # this might work to set flag to seen, if it doesn't already
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        # fill dict
        mail_dict['from'] = str(email_from)
        mail_dict['to'] = str(email_to)
        mail_dict['date'] = str(local_message_date)
        mail_dict['subject'] = str(subject)

        # Body details
        for part in email_message.walk():

            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                file_name = "email_" + str(x) + ".txt"
                output_file = open(file_name, 'w')
                output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" % (
                email_from, email_to, local_message_date, subject, body.decode('utf-8')))
                output_file.close()

                mail_dict['body'] = "%s" % (body.decode('utf-8'))
            else:
                continue

            print(mail_dict)


# class ReadGmail():
#
#     def __init__(self,
#                  host='imap.gmail.com',
#                  account=EMAIL_ACCOUNT,
#                  passwd=PASSWORD,
#                  mail_type="UNSEEN",  # (ALL/UNSEEN)
#                  encode='utf-8'
#                  ):
#         self.host=host
#         self.account=account
#         self.passwd=passwd
#         self.mail_type=mail_type
#         self.encode=encode
#
#     def get_mails(self):
#         mail = imaplib.IMAP4_SSL(self.host)
#         mail.login(self.account, self.passwd)
#         mail.list()
#         mail.select('inbox')
#         result, data = mail.uid('search', None, self.mail_type)
#         i = len(data[0].split())
#         list_mails_info = []
#         for x in range(i):
#             latest_email_uid = data[0].split()[x]
#             result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
#             # result, email_data = conn.store(num,'-FLAGS','\\Seen')
#             # this might work to set flag to seen, if it doesn't already
#             raw_email = email_data[0][1]
#             raw_email_string = raw_email.decode(self.encode)
#             email_message = email.message_from_string(raw_email_string)
#
#             # Header Details
#             date_tuple = email.utils.parsedate_tz(email_message['Date'])
#             if date_tuple:
#                 local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
#                 local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
#             email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
#             email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
#             subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
#
#             # Body details
#             for part in email_message.walk():
#                 mail_dict = {}
#                 if part.get_content_type() == "text/plain":
#                     body = part.get_payload(decode=True)
#                     mail_dict['from'] = email_from
#                     mail_dict['to'] = email_to
#                     mail_dict['date'] = local_message_date
#                     mail_dict['subject'] = subject
#                     mail_dict['body']=body.decode(self.encode)
#                     print(mail_dict)
#                     list_mails_info.append(mail_dict)
#                 else:
#                     continue
#
#         return list_mails_info
#
# def main():
#     lst_mails = ReadGmail()
#     print(lst_mails.get_mails())

if __name__ == '__main__':
    main()
