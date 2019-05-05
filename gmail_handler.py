#!usr/bin/env python

import smtplib 
import imaplib
import sys
import email
import traceback

class gmail_handler():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def retrieve_email(self):
        """ 
        Will retrieve all the unseen emails with the tag Movies scrape out the data
        and return the data as a list ready to be parsed
        """
        try:
            scraped_data = []
            session = imaplib.IMAP4_SSL("imap.gmail.com")
            session.login(self.username, self.password)
            session.select('Movies')
            retcode, new_movies = session.search(None, '(UNSEEN)')
            ids = new_movies[0].split()
            if retcode == 'OK' and ids:
                for index in str(email.message_from_bytes((new_movies[0]))).replace('\n','').split(' '):
                    retcode, email_data = session.fetch(index, '(RFC822)')
                    if retcode == 'OK':
                        scraped_data.append(email.message_from_bytes(email_data[0][1]).as_string().split('\n')[11])
                session.store('1:*', '+X-GM-LABELS', '\\Trash')
                session.expunge()
            session.logout()
            return scraped_data
        except Exception:
            traceback.print_exc()

    def send_email(self):
        """ Will email yourself to alert that a new movie has been added """
        try:
            session = smtplib.SMTP('smtp.gmail.com:587')
            session.ehlo()
            session.starttls()
            session.login(self.username, self.password)
            session.sendmail(self.username, self.password, 'New Movie Has Been Added')
        except Exception:
            traceback.print_exc()
