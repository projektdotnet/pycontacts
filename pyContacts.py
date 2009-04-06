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
global contacts_array
contacts_array = [] #Used later to track all contacts
contacts_file = os.path.expanduser('~') + "/.pyContactsCSVTest"
running = True #Used for looping menu function instead of multiple re-calling

#=End Vars===

#=Classes===
class Contact:
    def __init__(self, id="", name="", phone="", email=""):
        self.contact_id = id
        self.contact_name = name
        self.phone = phone
        self.email = email
        # Create a pretty_phone that is easier on the user's eyes and keep self.phone for writing to CSV
        if len(self.phone) == 7:
            self.pretty_phone = self.phone[0:3] + '-' + self.phone[3:] #ex 555-1234
        elif len(self.phone) == 10:
            self.pretty_phone = '(' + self.phone[0:3] + ') ' + self.phone[3:6] + '-' + self.phone[6:] #ex (866) 555-1234
        else:
            self.pretty_phone = self.phone # If we don't know the correct output then don't attempt to format ex 815551234

    #listMe used to print a clean looking version with proper spacing
    def listMe(self, id=""):
        print str(self.contact_id).rjust(3) + ") " + self.contact_name.ljust(15) + "- " + self.pretty_phone

    #List output for other functions to use
    def writeMe(self):
        return [self.contact_id,self.contact_name,self.phone,self.email]

    #Return only a name, primarily used in remove function
    def sayName(self):
        return self.contact_name

    def reId(self, id):
        self.contact_id = id

#=End Classes===

#=Functions===
def perform_sorting():
    contact_id_count = 1
    global contacts_array
    if len(contacts_array) > 0:
        contacts_array.sort(key=operator.attrgetter('contact_name'))
        for row in contacts_array:
            row.reId(contact_id_count)
            contact_id_count += 1

def write_contacts(filename):
    perform_sorting()
    output_contacts_file = csv.writer(open(filename, 'w'))
    for row in contacts_array:
        output_contacts_file.writerow(row.writeMe())

def fetch_contacts(filename):
    contacts_contacts_file=csv.reader(open(filename))
    for row in contacts_contacts_file:
        contacts_array.append ( Contact(row[0],row[1],row[2],row[3]) ) #Split row into class attributes
    perform_sorting()

def print_contacts():
    contact_id=1
    for row in contacts_array:
        row.listMe(contact_id)
        contact_id += 1

def add_contact():
    add_loop = True
    while add_loop:
        print "Add a Contact: "
        name=str(raw_input("What is the contact's name?: "))
        number=str(raw_input("What is the contact's number?: "))
        print "Does this look right?"
        print "Name: " + name.capitalize()
        pretty_number = ""
        if len(number) == 7:
            pretty_number = number[0:3] + "-" + number[3:]
        elif len(number) == 10:
            pretty_number = "(" + number[0:3] + ") " + number[3:6] + "-"+ number[6:]
        print "Phone Number: " + pretty_number
        correct=str(raw_input("[y/n]"))
        if correct == "y":
            name = name.capitalize()
            contacts_array.append(Contact("",name,number,""))
        elif correct == "n":
            pass
        else:
            print "Not an option!"
        another=str(raw_input("Add another? [y/n]: "))
        if another == "y":
            pass
        elif another == "n":
            add_loop = False
        else:
            print "Not an option!"
    perform_sorting()


def remove_contact():
    remove_loop = True
    while remove_loop:
        if len(contacts_array) > 0:
            contact_id=1
            perform_sorting()
            for row in contacts_array:
                row.listMe(contact_id)
                contact_id += 1
            toremove=int(raw_input("Enter ID to remove: "))
            toremove -= 1
            if toremove < contact_id:
                print "Are you sure you want to remove " + contacts_array[toremove].sayName()
                last_chance=str(raw_input("[y/n]"))
                if (last_chance.lower() == "y"):
                    removed_name=contacts_array[toremove].sayName()
                    del contacts_array[toremove]
                    print "Removed " + removed_name
                else:
                    print "Did NOT delete "+contacts_array[toremove].sayName()
            else:
                print "Invalid contact id"
            another=str(raw_input("Remove another? [y/n]"))
            if another.lower() == "y":
                pass
            else:
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
    print "q. Save and Quit"
    print ""
    call_correct_function(raw_input("What to do?: "))

def call_correct_function(selection):
    if str(selection) == "q":
        global running
        running = False
    elif str(selection) == "1":
        print_contacts()
    elif str(selection) == "2":
        add_contact()
    elif str(selection) == "3":
        remove_contact()
    else:
        print "Error, not a valid item"

#=End Functions===

if os.path.exists(contacts_file):
    fetch_contacts(contacts_file)

while running:
    menu()

write_contacts(contacts_file)

