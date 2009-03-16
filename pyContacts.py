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
    contacts_file=csv.reader(open(filename))
    for name,phone in contacts_file:
        print name,phone

def input_contact(name,number):
    contacts_array

#=Start the program===
file=raw_input("Which file to read?: ")
fetch_contacts(file)

#=End===
