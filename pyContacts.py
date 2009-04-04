#!/usr/bin/env python
#
# pyContacts v0.2 - Copyright Shawn "prjktdtnt" Thompson 2008
# Simple contact manager for my own use
#
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Features: *Add, remove, store contact information
#           *Display easily readable and formatted info
#            to the user
#

#=Imports===
import csv
import os
import operator
#=End Imports===

#=Variables===
contacts_array = []
thefile = os.path.expanduser('~') + "/.pyContactsCSVTest"
running = True

#=End Vars===

#=Classes===
class Contact:
    def __init__(self, name="", phone=""):
        self.name = name
        self.phone = phone
        # Create a pretty_phone that is easier on the user's eyes and keep self.phone for writing to CSV
        if len(self.phone) == 7:
            self.pretty_phone = self.phone[0:3] + '-' + self.phone[3:] #ex 555-1234
        elif len(self.phone) == 10:
            self.pretty_phone = '(' + self.phone[0:3] + ') ' + self.phone[3:6] + '-' + self.phone[6:] #ex (866) 555-1234
        else:
            self.pretty_phone = self.phone # If we don't know the correct output then don't attempt to format ex 815551234

    def listMe(self, id=""):
        print str(id).rjust(3) + ") " + self.name.ljust(15) + "- " + self.pretty_phone

    def writeMe(self):
        return [self.name,self.phone]


#=End Classes===

#=Functions===
def perform_sorting():
    if len(contacts_array) > 0:
        contacts_array.sort(key=operator.attrgetter('name'))

def write_contacts(filename):
    perform_sorting()
    output_thefile = csv.writer(open(filename, 'w'))
    for row in contacts_array:
        output_thefile.writerow(row.writeMe())

def fetch_contacts(filename):
    contacts_thefile=csv.reader(open(filename))
    for row in contacts_thefile:
        contacts_array.append ( Contact(row[0],row[1]) )
    perform_sorting()

def print_contacts():
    contact_id=1
    perform_sorting()
    for row in contacts_array:
        row.listMe(contact_id)
        contact_id += 1

def add_contact():
    pass

def remove_contact():
    remove_loop = True
    while remove_loop:
        if len(contacts_array) > 0:
            contact_id=1
            perform_sorting()
            for row in contacts_array:
                row.listMe(contact_id)
                contact_id += 1
            remove_loop = False
        else:
            print "No Contacts!"
            remove_loop = False

def menu():
    print ""
    print "Menu:"
    print "1. List Contacts"
    print "2. Add a Contact"
    print "3. Remove a Contact"
    print "q. Quit"
    print ""
    call_correct_function(raw_input("What to do?: "))

def call_correct_function(selection):
    if str(selection) == "q":
        global running
        running = False
    elif str(selection) == "1":
        print_contacts()
    elif str(selection) == "2":
        pass
    elif str(selection) == "3":
        remove_contact()
    else:
        print "Error, not a valid item"

#=End Functions===

#if os.path.exists(thefile):
fetch_contacts(thefile)

while running:
    menu()

write_contacts(thefile)

