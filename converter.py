#!/usr/bin/env python
"""
Convert pyContacts v0.2 and older CSV's to new python v0.3 CVS format
 This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import csv
import os
import operator

old_contacts_array = []
old_contacts_file = os.path.expanduser('~') + "/.pyContactsCSV"
new_contacts_array = []

#load file to array
contacts_thefile=csv.reader(open(old_contacts_file))
for row in contacts_thefile:
    old_contacts_array.append ( row )

#sort alphabetically
old_contacts_array.sort()

#Count each line and assign the ID number and empty space for future e-mail option
counter = 0
for row in old_contacts_array:
    name = old_contacts_array[counter][0]
    number = old_contacts_array[counter][1]
    new_contact = [counter,name,number,""]
    new_contacts_array.append(new_contact)
    counter += 1

new_counter = 0
for row in new_contacts_array:
    print new_contacts_array[new_counter]
    new_counter += 1

output_thefile = csv.writer(open(old_contacts_file, 'w'))
output_thefile.writerows(new_contacts_array)

