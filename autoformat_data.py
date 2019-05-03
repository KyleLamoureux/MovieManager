#!usr/bin/env python

import json
import os

class formatMoviesToJSON():

    def clean_string(self, line):
        return line.rstrip().lstrip().replace('\n','')

    def cvtMovie(self, fileName):
        readf = open(fileName, 'r')
        data = {}
        for key, line in enumerate(readf.readlines()):
            splt_line = line.split('!')
            temp_dict = {}
            temp_dict['Title'] = self.clean_string(splt_line[0])
            temp_dict['Rating'] = self.clean_string(splt_line[1])
            temp_dict['Date'] = self.clean_string(splt_line[2])
            temp_dict['Location'] = self.clean_string(splt_line[3])
            temp_dict['Genre'] = self.clean_string(splt_line[4]).split(',')
            temp_dict['Comment'] = self.clean_string(splt_line[5])
            data[key] = temp_dict
        readf.close()
        return data

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
    m.writeToJSON(os.getcwd(), 'movies', m.cvtMovie('curr_list.txt'))
    m.makeReadableJSON(os.getcwd(), 'movies.json', 'movies_readable')

if __name__ == "__main__":
    main()
