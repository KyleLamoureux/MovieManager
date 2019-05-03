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
            self.sheet = gs.open('Movie List').sheet1
        except:
            sys.exit('Failed to load sheet named "Movie List"')
   
    def add_new_movies(self):
        """
        movieList: JSON format
        Takes in a JSON dump and adds each movie to excel sheet
        """
        try:
            with open('temp.json', 'r') as fp:
                movies = json.load(fp)
        except:
            sys.exit('Failed to open "temp.json"')
        for movie in range(len(movies.keys())):
            if not self.old_data(list(movies[str(movie)].values())):
                self.sheet.append_row(list(movies[str(movie)].values()))
    
    def reformat_text_file(self, filename):
        self.writeToJSON(os.getcwd(), 'temp', self.cvtMovie(filename))

    def get_row(self):
        print(self.sheet.row_values(1))
        print(self.sheet.get_all_values())

    def old_data(self, data):
        return data in self.sheet.get_all_values()

def main():
    manager = Sheets('client_secret.json') 
    
    manager.reformat_text_file('test.txt')
    manager.add_new_movies()

    



if  __name__ == "__main__":
    main()
