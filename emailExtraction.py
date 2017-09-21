#********************************************************
#
#  Program:      Project 2 -- Email Extraction
#
#  Author:       Caleb Myers
#  Email:        cm346613@ohio.edu
#
#  Description: This program reads through Ohio University's
#               engineering department people webpage
#               (https://ohio.edu/engineering/about/people)
#               and saves the listed names and emails to a
#               sqlite3 database. The name of the database
#               is taken as a command line argument.
#
#  Date:        Febuary 12, 2017
#
#********************************************************
import re
import sys
import urllib.request
import sqlite3



def main():
    SITE = 'https://www.ohio.edu/engineering/about/people'          # website to search through
    inputSite = urllib.request.urlopen(SITE)
    html = inputSite.read()                                         # html code read in from website
    inputSite.close()
    html = str(html)
    html = html.replace('\\xc2\\xa0','####')                        # replaces unicode
    html = html.replace('\\xcf\\x8d', 'u')                            # replaces unicode
    html = html.replace('\\xc3\\xa1','a')                           # replaces unicode

    EMAIL_RE = '>([\w,\s,\\-,\\.]*@ohio\\.edu)<'                     # regex to find emails
    emails = re.findall(EMAIL_RE, html)                              # list of emails

    NAME_RE = '"profiles.cfm\\?profile=[\w,-]*">([\w,\s,\\-,\\.]*)####([\w,\s,\\-,\\.]*)<'     # regex to find names
    names = re.findall(NAME_RE, html)                                                          # list of names
 
    try:
        con = sqlite3.connect(sys.argv[1])                              # creates database file
        cur = con.cursor()
        cur.execute('''create table engineeringProfessors
                       (id integer primary key,
                        firstName text,
                        lastName text,
                        email text)''')                                 # creates table in database file

        fillDatabase(names, emails, cur)                                # fills database
        con.commit()                                                    # saves changes in database
        con.close()                                                     # closes database
    except sqlite3.Error:
        
        print('Database Error')


#********************************************************
#
#  Function:   fillDatabase
#
#  Purpose:    saves names and emails to sqlite3 database
#
#  Parameters: names - list of names found on website
#              emails - list of emails found on website
#              cur - cursor used for database functions
#
#  Member/Global Variables: iterator - an iterator used as
#                                      the id of each entry
#
#  Preconditions:   all parameters have valid values
#
#  Postconditions:  database will contain all names and emails
#
#  Calls:  cur.execute() - sqlite3 execute function
#
#********************************************************
def fillDatabase(names, emails, cur):
    iterator = 0
    START = 'insert into engineeringProfessors values ('
    for name in names:
        insertion = START + str(iterator) + ', "'+ name[0] + '", "' + name[1] + '", "' + emails   [iterator] + '")'
        cur.execute(insertion)
        iterator += 1



if len(sys.argv) == 2:    # check for valid number of command line arguments
    main()
else:
    print('Error: Invalid number of command line arguments')
    print('Please try running the program agina with one command line argument')

