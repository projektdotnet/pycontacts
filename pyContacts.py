#
# pyContacts - Copyright Shawn "prjktdtnt" Thompson
# Simple contact manager for my own use
# This program is distributed under the GNU GPLv3 license
#
# Features: *Add, remove, store contact information
#           *Display easily readable and formatted info
#            to the user
#
#=Imports===
import csv

#=End Imports===

#=Functions===

#Ugly first attempt at fetch and print on an existing file
def fetch_contacts(filename):
    contacts_array=csv.reader(open(filename))
    for name,phone in contacts_array:
        print name,phone

file=raw_input("File to use?: ")
fetch_contacts(file)
