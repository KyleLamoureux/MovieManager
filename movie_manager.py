#!usr/bin/env python

import sys
import os
import json
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from autoformat_data import formatMoviesToJSON

class Sheets(formatMoviesToJSON):
    """ Class to hold custom google sheet calls """
    
    def __init__(self, secret, sheet=None):
        """ 
        Initialize with the file name or path to the file with credentials
        The email in the credentials files must have been shared with the sheet
        """
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(secret, scope)
        gs = gspread.authorize(credentials)
        # print(gs.open('Movie List').sheet1.col_values(1))
        try:
            self.__sheet = gs.open('Movie List').sheet1
        except:
            sys.exit('Failed to load sheet named "Movie List"')
    
    def get_row(self):
        print(self.__sheet.row_values(1))
        print(self.__sheet.get_all_values())

    

def main():
    sheet = Sheets('client_secret.json')
    sheet.get_row()
    



if  __name__ == "__main__":
    main()
