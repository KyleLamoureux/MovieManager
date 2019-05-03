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

    def old_data(self, data):
        return data in self.sheet.get_all_values()

    def sort_data_by_date(self, descend=True):
        movies = self.sheet.get_all_values()
        movies.pop(0)
        date_list = []
        for index, movie in enumerate(movies):
            date_list.append(movie[2].replace('-',''))
        sorted_movies = [x for y, x in sorted(zip(date_list, movies), reverse=descend)]
        return sorted_movies


def main():
    manager = Sheets('client_secret.json') 
    
    manager.reformat_text_file('test.txt')
    manager.add_new_movies()

    print(manager.sort_data_by_date(descend=False))



if  __name__ == "__main__":
    main()
