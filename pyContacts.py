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

#=Major Variables===
contacts_array = []
file=""
#=End Variables===


#=Functions===

#Ugly first attempt at fetch and print on an existing file
def fetch_contacts(filename):
    contacts_file=csv.reader(open(filename))
    for row in contacts_file:
        contacts_array.append( row )

#add a contact to the array
def append_contact(input):
    contacts_array.append(input)

#The write and exit function
#def kill_func():

#def write_to_contacts(filename)

def menu():
    print "Contacts Management"
    print "1. List Contacts"
    print "2. Add a contact"
    print "q. quit"
    
def write_contacts(filename):
    output_file = csv.writer(open(file, 'w'))
    output_file.writerows(contacts_array)
    
#=Start the program===
file="/home/trash/.contacts.csv"
#append_name="someone"
#append_number="555-555-5555"
#input=[append_name,append_number]
#input_contact(input)
#menu()
fetch_contacts(file)
contacts_array.sort()
print contacts_array
write_contacts(file)
#=End===
