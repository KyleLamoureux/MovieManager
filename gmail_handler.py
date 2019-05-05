#!usr/bin/env python

import smtplib 
import imaplib
import sys
import config
import email

def main():
    try:
        #session = smtplib.SMTP('smtp.gmail.com:587')
        #session.ehlo()
        #session.starttls()
        #session.login(config.USERNAME, config.PASSWORD)
        
        session = imaplib.IMAP4_SSL("imap.gmail.com")
        session.login(config.USERNAME, config.PASSWORD)
        session.select('Movies')
        outfile = open('uploaded_movies.txt', 'w')
        retcode, new_movies = session.search(None, '(UNSEEN)')
        ids = new_movies[0].split()
        if retcode == 'OK' and ids:
            for index in str(email.message_from_bytes((new_movies[0]))).replace('\n','').split(' '):
                retcode, email_data = session.fetch(index, '(RFC822)')
                if retcode == 'OK':
                    outfile.write(email.message_from_bytes(email_data[0][1]).as_string().split('\n')[11])
            session.store('1:*', '+X-GM-LABELS', '\\Trash')
            session.expunge()
        session.logout()
        outfile.close()
    except Exception:
        sys.exit("Error in gmail_handler fetch: " + Exception)

if __name__ == '__main__':
    main()

"""
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json')
service = build('gmail', 'v1', credentials=credentials)
print(dir(service))
"""
