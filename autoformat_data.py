#!/usr/bin/env python3

import json
import os

class FormatMoviesToJSON():

    def clean_string(self, line):
        return line.rstrip().lstrip().replace('\n','')

    def cvtMovie(self, data=None, filename=None):
        """ 
        Given either a file or list to parse movie data from it will return
        a newly formated data list
        """
        lines = []
        if filename:
            readf = open(filename, 'r')
            lines = readf.readlines()
        elif data:
            lines = data
        return_data = {}
        for key, line in enumerate(lines):
            splt_line = line.split('!')
            temp_dict = {}
            temp_dict['Title'] = self.clean_string(splt_line[0])
            temp_dict['Rating'] = self.clean_string(splt_line[1])
            temp_dict['Date'] = self.clean_string(splt_line[2])
            temp_dict['Location'] = self.clean_string(splt_line[3])
            temp_dict['Mood'] = self.clean_string(splt_line[4])
            temp_dict['Comment'] = self.clean_string(splt_line[5])
            return_data[key] = temp_dict
        if filename: readf.close()
        return return_data

    def writeToJSON(self, path, fileName, data):
        filePathDense = path + '/' + fileName + '.json'
        with open(filePathDense, 'w') as fp:
            json.dump(data, fp)
    
    def makeReadableJSON(path, cvntFile, readableFileName):
        filePathReadable = path + '/' + readableFileName + '.json'
        read = open(filePathReadable, 'w')
        read.write(json.dumps(json.load(open(path + '/' + cvntFile)), indent=4))
        read.close()

def main():
    m = formatMoviesToJSON()
    #c = m.cvtMovie(data=['gfs!10/10!51-12-532!sdfsdf!fgdfgdf!dfgdfg'])
    #print(c)
    #m.writeToJSON(os.getcwd(), 'movies', m.cvtMovie('curr_list.txt'))
    #m.makeReadableJSON(os.getcwd(), 'movies.json', 'movies_readable')

if __name__ == "__main__":
    main()
