#!/usr/bin/env python3

import smtplib 
import imaplib
import sys
import email
import traceback

class GmailHandler():

    def __init__(self, username, password):
        """ Password must be an access code created in the security section of your account """
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
                        r  = (email.message_from_bytes(email_data[0][1]))
                        if r.is_multipart():
                            scraped_data.append(r.get_payload()[0].as_string()[42:])
                session.store('1:*', '+X-GM-LABELS', '\\Trash')
                session.expunge()
            session.logout()
            return scraped_data
        except Exception:
            traceback.print_exc()

    def alert_email(self):
        """ Will email yourself to alert that a new movie has been added """
        try:
            session = smtplib.SMTP('smtp.gmail.com:587')
            session.ehlo()
            session.starttls()
            session.login(self.username, self.password)
            session.sendmail(self.username, self.username, 'New Movie Has Been Added')
        except Exception:
            traceback.print_exc()
        return True
