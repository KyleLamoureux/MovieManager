#!/usr/bin/env python3

import sys
import os
import json
import gspread

import config

from oauth2client.service_account import ServiceAccountCredentials

from autoformat_data import FormatMoviesToJSON
from gmail_handler import *

class Sheets(FormatMoviesToJSON):
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
   
    def add_new_movies(self, JSON_to_open):
        """
        movieList: JSON format
        Takes in a JSON dump and adds each movie to excel sheet
        """
        try:
            with open(JSON_to_open, 'r') as fp:
                movies = json.load(fp)
        except:
            sys.exit('Failed to open "temp.json"')
        for movie in range(len(movies.keys())):
            if not self.old_data(list(movies[str(movie)].values())):
                self.sheet.append_row(list(movies[str(movie)].values()))
    
    def reformat_data(self, output_filename, data):
        self.writeToJSON(os.getcwd(), output_filename, self.cvtMovie(data))

    def old_data(self, data):
        """ Check if data is identical """
        return data in self.sheet.get_all_values()

    def sort_data_by_col(self, col, descend=True):
        """ 
        Return a list of sorted movie list
        options = ['Title', 'Rating', 'Date', 'Location', 'Mood', 'Comment']
                      0,       1,       2,        3,         4,        5
        """
        movies = self.sheet.get_all_values()
        movies.pop(0)
        date_list = []
        for index, movie in enumerate(movies):
            if col == 1:
                rating = movie[col].split('/')
                date_list.append(float(rating[0]) + float(rating[1]))
            elif col == 2:
                date_list.append(int(movie[col].replace('-','')))
            else:
                date_list.append(movie[col])
        sorted_movies = [x for y, x in sorted(zip(date_list, movies), reverse=descend)]
        return sorted_movies
    
    def extract_data(self, search, col):
        """
        Takes in search word and returns every row with that key word in it
        options = ['Title', 'Rating', 'Date', 'Location', 'Mood', 'Comment']
                      0,       1,       2,        3,         4,        5
        """
        requested = []
        for row in self.sheet.get_all_values():
            if search.lower() in row[col].lower():
                requested.append(row)
        return requested


def main():
    manager = Sheets('client_secret.json') 
    email = GmailHandler(config.USERNAME, config.PASSWORD)
    movie_data = email.retrieve_email()
    if movie_data:
        manager.reformat_data('temp', movie_data)
        manager.add_new_movies('temp.json')
        if email.alert_email():
            #os.remove('temp.txt')
            os.remove('temp.json')
     
    #for x in manager.sort_data_by_col(1, descend=False): print(x)
    #print()
    #for y in manager.sort_data_by_col(1, descend=True): print(y)
    
    #for z in manager.extract_data("Avengers", 0): print(z)


if  __name__ == "__main__":
    main()
