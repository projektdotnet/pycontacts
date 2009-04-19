#!/usr/bin/env python
#
# pyContacts v0.4.0 - Copyright Shawn "prjktdtnt" Thompson 2008
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
class Contact:
    def __init__(self, id="", fname="", lname="", phone="", email="", address1="", address2="", city="", state="", zip=""):
        self.contact_id = id
        #Capitalize fname and lname (for newly added contacts)
        self.contact_fname = fname.capitalize()
        self.contact_lname = lname.capitalize()
        #Receive the phone info
        self.phone = phone
        self.makePhonePretty()
        self.email = email
        self.address1 = address1.capitalize()
        self.address2 = address2
        self.city = city.capitalize()
        if len(state) == 2:
            self.state = state.upper()
        else:
            self.state = state.capitalize()
        self.zip = zip

    #listMe used to print a clean looking version with proper spacing
    def listMe(self):
        return [str(self.contact_id),self.sayFullName()]

    #List output for other functions to use
    def writeMe(self):
        return [self.contact_id,self.contact_fname,self.contact_lname,self.phone,self.email,self.address1,self.address2,self.city,self.state,self.zip]

    #Return only first name
    def sayfName(self):
        return self.contact_fname

    #Return only last name 
    def saylName(self):
        return self.contact_lname
    
    #Return the full name of a user
    def sayFullName(self):
        myFullName = self.contact_fname + " " + self.contact_lname
        return myFullName

    #Return the User ID
    def sayId(self):
        return self.contact_id
    
    def sayPhone(self):
        return self.phone

    def sayEmail(self):
        return self.email

    def sayAddress(self):
        return [self.address1,self.address2,self.city,self.state,self.zip]
        

    #Create a user readable phone
    def makePhonePretty(self):
        if len(self.phone) == 7:
            self.pretty_phone = self.phone[0:3] + '-' + self.phone[3:] #ex 555-1234
        elif len(self.phone) == 10:
            self.pretty_phone = '(' + self.phone[0:3] + ') ' + self.phone[3:6] + '-' + self.phone[6:] #ex (866) 555-1234
        else:
            self.pretty_phone = self.phone # If we don't know the correct output then don't attempt to format ex 815551234

    #Print full information in an easy to read manor
    def fullInfo(self):
        return [self.sayFullName(),self.pretty_phone,self.email,self.address1,self.address2,self.city,self.state,self.zip]

    #Below here is where the reFunctions begin, this is for updating user information easily
    def reId(self, id):
        self.contact_id=id

    def reName(self, fname, lname):
        self.contact_fname=fname.capitalize()
        self.contact_lname=lname.capitalize()

    def rePhone(self, phone):
        self.phone=phone
        self.makePhonePretty()

    def reEmail(self, email):
        self.email=email

    def reAddress(self, newaddress):
        self.address1=newaddress[0]
        self.address2=newaddress[1]
        self.city=newaddress[2].capitalize()
        if len(newaddress[3]) == 2:
            self.state=newaddress[3].upper()
        else:
            self.state=newaddress[3].capitalize()
        self.zip=newaddress[4]



#=END Contact Class===

#=END Classes===


if __name__ == "__main__":
    print "Pleanse run cmd_pycontacts.py or gtk_pycontacts.py, "
    print "this file has no direct use to the user."
    print
#=END===
