#!/usr/bin/env python
##
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
#
##

#==Imports==
import sys
import pygtk
if sys.platform !='win32':
    pygtk.require('2.0')
import gtk
import csv,os,operator,pango
from pyContacts import Contact

#==Main gtkPyContacts window and primary functions==
class gtkPyContacts:

    def delete_event(self, widget, data=None):
        return False

    def destroy(self, widget, data=None):
        self.write_contacts()
        gtk.main_quit()

    def __init__(self):
        self.storage_file = os.path.expanduser('~') + "/.pyContactsCSV"
        self.contactsArray = []
        self.version = "pyContacts GTK v0.4.0"

        #Start window, declare the callbacks to close the program
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title("pyContacts GTK")
        self.window.set_border_width(5)
        self.window.set_default_size(300, 400)
        
        #Contact List
        self.contactsArrayList = gtk.ListStore(str, str, str)
        self.contactsListView = gtk.TreeView(self.contactsArrayList)

        #Columns for list
        self.clvId = gtk.TreeViewColumn('id')
        self.clvfName = gtk.TreeViewColumn('First Name')
        self.clvlName = gtk.TreeViewColumn('Last Name')

        #Columns to correct order
        self.contactsListView.append_column(self.clvId)
        self.contactsListView.append_column(self.clvfName)
        self.contactsListView.append_column(self.clvlName)

        #Create the renderers, should always use CellRendererText here
        self.clvCellId = gtk.CellRendererText()
        self.clvCellfName = gtk.CellRendererText()
        self.clvCelllName = gtk.CellRendererText()

        #Cell Packing Renderers
        self.clvId.pack_start(self.clvCellId, True)
        self.clvfName.pack_start(self.clvCellfName, True)
        self.clvlName.pack_start(self.clvCelllName, True)

        #Packed renderers in cells, now pack those to columns
        self.clvId.set_attributes(self.clvCellId, text=0)
        self.clvfName.set_attributes(self.clvCellfName, text=1)
        self.clvlName.set_attributes(self.clvCelllName, text=2)

        #Wrap it in a scroll window
        self.clvScrollWrap = gtk.ScrolledWindow()
        self.clvScrollWrap.add(self.contactsListView)

        #Define buttons in this section
        btnQuit = gtk.Button(stock=gtk.STOCK_CLOSE)
        btnNew = gtk.Button(stock=gtk.STOCK_NEW)
        btnShow = gtk.Button(stock=gtk.STOCK_ZOOM_IN)
        btnShow.get_children()[0].get_children()[0].get_children()[1].set_label("Show Contact")
        btnEdit = gtk.Button(stock=gtk.STOCK_EDIT)
        btnRemove = gtk.Button(stock=gtk.STOCK_DELETE)
        btnSave = gtk.Button(stock=gtk.STOCK_SAVE)
        btnAbout = gtk.Button(stock=gtk.STOCK_ABOUT)

        #Connect callbacks here
        btnQuit.connect("clicked", self.destroy)
        btnNew.connect("clicked", self.add_contact)
        btnShow.connect("clicked", self.show_contact)
        btnEdit.connect("clicked", self.main_edit_button_clicked)
        btnRemove.connect("clicked", self.remove_contact)
        btnSave.connect("clicked", self.write_contacts)
        btnAbout.connect("clicked", self.displayAbout)

        #Main window layout, using table style
        layoutGrid = gtk.Table(9, 2, True)
        layoutGrid.set_row_spacings(5)
        layoutGrid.set_col_spacings(3)

        #Window add bits
        self.window.add(layoutGrid)

        #Table attachments
        layoutGrid.attach(btnAbout, 1, 2, 0, 1) 
        layoutGrid.attach(self.clvScrollWrap, 0, 2, 1, 6)
        layoutGrid.attach(btnNew, 0, 1, 6, 7) 
        layoutGrid.attach(btnEdit, 1, 2, 6, 7) 
        layoutGrid.attach(btnShow, 0, 1, 7, 8) 
        layoutGrid.attach(btnRemove, 1, 2, 7, 8)
        layoutGrid.attach(btnSave, 0, 1, 8, 9) 
        layoutGrid.attach(btnQuit, 1, 2, 8, 9) 

        #Widget show calls
        self.window.show_all()
        self.window.show()
        self.load_contacts()

    #Display Commands
    def reList(self):
        self.contactsArrayList.clear()
        for this_row in self.contactsArray:
            self.contactsArrayList.append([this_row.sayId(),this_row.sayfName(),this_row.saylName()])

    def displayAbout(self, widget, data=None):
        self.aboutWindow = gtk.Window()
        self.aboutWindow.set_default_size(300, 100)
        aboutVBox = gtk.VBox()
        self.aboutWindow.add(aboutVBox)
        self.aboutWindow.set_title("About pyContacts GTK")
        self.aboutWindow.set_modal(True)
        
        aboutHBlogo = gtk.HBox()
        aboutHBversion = gtk.HBox()
        aboutHBdesc = gtk.HBox()
        aboutHBbtns = gtk.HBox()

        imgLogo = gtk.Image()
        imgLogo.set_from_file('./logo_pycontacts_gtk_040.gif')
        lblVersion = gtk.Label(self.version)
        lblDesc = gtk.Label("Simple contacts manager to store \n Name, phone, email and addresses")
        lblVersion.modify_font(pango.FontDescription("normal 13"))
        lblDesc.modify_font(pango.FontDescription("normal 10"))
        lblVersion.set_alignment(0.5, 0.5)
        lblDesc.set_line_wrap(True)

        btnCloseAbout = gtk.Button(stock=gtk.STOCK_CLOSE)

        aboutHBlogo.pack_start(imgLogo, False, False, 5)
        aboutHBversion.pack_start(lblVersion, True, True, 5)
        aboutHBdesc.pack_start(lblDesc, True, True, 5)
        aboutHBbtns.pack_end(btnCloseAbout, False, False, 5)

        aboutVBox.pack_start(aboutHBlogo, False, False, 0)
        aboutVBox.pack_start(aboutHBversion, False, False, 0)
        aboutVBox.pack_start(aboutHBdesc, False, False, 0)
        aboutVBox.pack_start(aboutHBbtns, False, False, 0)

        btnCloseAbout.connect("clicked", self.about_close_btn_clicked)

        self.aboutWindow.show_all()
        self.aboutWindow.show()

    def about_close_btn_clicked(self, widget):
        self.aboutWindow.hide()

    #Primary Commands
    def perform_sorting(self):
        if len(self.contactsArray) > 0:
            contact_id_count = 1
            self.contactsArray.sort(key=operator.attrgetter('contact_fname'))
            for row in self.contactsArray:
                row.reId(contact_id_count)
                contact_id_count += 1
            self.reList()

    def load_contacts(self, data=None):
        load_from = csv.reader(open(self.storage_file))
        for row in load_from:
            self.contactsArray.append( Contact(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]) )
        for this_row in self.contactsArray:
            self.contactsArrayList.append([this_row.sayId(),this_row.sayfName(),this_row.saylName()])


    def write_contacts(self, widget=None, data=None):
        self.perform_sorting()
        save_to = csv.writer(open(self.storage_file, 'w'))
        for row in self.contactsArray:
            save_to.writerow(row.writeMe())

    def add_contact(self, widget, data=None):
        #Define add contact window, add a VBox to pack in HBoxes to
        self.addWindow = gtk.Window()
        addVBox1 = gtk.VBox(True, 2)
        self.addWindow.add(addVBox1)
        self.addWindow.set_title("New Contact")
        self.addWindow.set_modal(True)

        #HBoxes to pack into VBox1
        addHBFName = gtk.HBox()#First
        addHBLName = gtk.HBox()#Last
        addHBPhone = gtk.HBox()#Phone
        addHBEmail = gtk.HBox()#Email
        addHBAddress1 = gtk.HBox()#Address1
        addHBAddress2 = gtk.HBox()#Address2
        addHBCSZ = gtk.HBox()#City State Zip
        addHBbtns = gtk.HBox()#Buttons w00t!

        #Labels
        lblfName = gtk.Label("First Name: ")
        lbllName = gtk.Label("Last Name: ")
        lblPhone = gtk.Label("Phone Number: ")
        lblEmail = gtk.Label("Email: ")
        lblAddress1 = gtk.Label("Address 1: ")
        lblAddress2 = gtk.Label("Address 2: ")
        lblCity = gtk.Label("City: ")
        lblState = gtk.Label("State: ")
        lblZip = gtk.Label("Zip: ")

        #Self.Input Boxes
        self.inpfName = gtk.Entry()
        self.inplName = gtk.Entry()
        self.inpPhone = gtk.Entry()
        self.inpEmail = gtk.Entry()
        self.inpAddress1 = gtk.Entry()
        self.inpAddress2 = gtk.Entry()
        self.inpCity = gtk.Entry()
        self.inpState = gtk.Entry(2)
        self.inpZip = gtk.Entry(6)
        
        #Pretty layout mod
        self.inpEmail.set_width_chars(25)
        self.inpCity.set_width_chars(10)
        self.inpState.set_width_chars(2)
        self.inpZip.set_width_chars(5)

        #Buttons w00t!!
        btnOK = gtk.Button(None, gtk.STOCK_OK, False)
        btnCancel = gtk.Button(None, gtk.STOCK_CANCEL, False)

        #Pack lbl and self.inp's into HB's
        addHBFName.pack_start(lblfName, False, False, 2)
        addHBFName.pack_end(self.inpfName, False, False, 2)
        addHBLName.pack_start(lbllName, False, False, 2)
        addHBLName.pack_end(self.inplName, False, False, 2)
        addHBPhone.pack_start(lblPhone, False, False, 2)
        addHBPhone.pack_end(self.inpPhone, False, False, 2)
        addHBEmail.pack_start(lblEmail, False, False, 2)
        addHBEmail.pack_end(self.inpEmail, False, False, 2)
        addHBAddress1.pack_start(lblAddress1, False, False, 2)
        addHBAddress1.pack_end(self.inpAddress1, False, False, 2)
        addHBAddress2.pack_start(lblAddress2, False, False, 2)
        addHBAddress2.pack_end(self.inpAddress2, False, False, 2)
        addHBCSZ.pack_start(lblCity, False, False, 2)
        addHBCSZ.pack_start(self.inpCity, False, False, 2)
        addHBCSZ.pack_start(lblState, False, False, 2)
        addHBCSZ.pack_start(self.inpState, False, False, 2)
        addHBCSZ.pack_start(lblZip, False, False, 2)
        addHBCSZ.pack_start(self.inpZip, False, False, 2)
        addHBbtns.pack_end(btnOK, False, False, 2)
        addHBbtns.pack_end(btnCancel, False, False, 2)
        

        #Pack HB's into VBox
        addVBox1.pack_start(addHBFName, False, False, 2)
        addVBox1.pack_start(addHBLName, False, False, 2)
        addVBox1.pack_start(addHBPhone, False, False, 2)
        addVBox1.pack_start(addHBEmail, False, False, 2)
        addVBox1.pack_start(addHBAddress1, False, False, 2)
        addVBox1.pack_start(addHBAddress2, False, False, 2)
        addVBox1.pack_start(addHBCSZ, False, False, 2)
        addVBox1.pack_start(addHBbtns, False, False, 2)
        

        btnOK.connect("clicked", self.on_add_ok_clicked)
        btnCancel.connect("clicked", self.on_add_cancel_clicked)

        #Show completed UI
        self.addWindow.show_all()
        self.addWindow.show()

    def on_add_cancel_clicked(self, widget=None):
        self.addWindow.hide()

    def on_add_ok_clicked(self, widget=None):
        fName = self.inpfName.get_text()
        lName = self.inplName.get_text()
        phone = self.inpPhone.get_text()
        email = self.inpEmail.get_text()
        address1 = self.inpAddress1.get_text()
        address2 = self.inpAddress2.get_text()
        city = self.inpCity.get_text()
        state = self.inpState.get_text()
        zip = self.inpZip.get_text()
        self.contactsArray.append(Contact("",fName,lName,phone,email,address1,address2,city,state,zip))
        self.perform_sorting()
        self.addWindow.hide()

    def main_edit_button_clicked(self, widget, data=None):
        toEdit = self.get_selected()
        toEdit = int(toEdit[0]) - 1
        self.edit_contact(toEdit)

    def edit_contact(self, toEdit=None):
        #Define edit contact window, edit a VBox to pack in HBoxes to
        self.editWindow = gtk.Window()
        editVBox1 = gtk.VBox(True, 2)
        self.editWindow.add(editVBox1)
        self.editWindow.set_title("New Contact")
        self.curEditId = toEdit
        if toEdit > len(self.contactsArray):
            errorMessage = "No contact selected"
            errorBox = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, errorMessage)
            errorBox.run()
            errorBox.destroy()
        else:
            self.editWindow.set_modal(True)

        #HBoxes to pack into VBox1
            editHBFName = gtk.HBox()#First
            editHBLName = gtk.HBox()#Last
            editHBPhone = gtk.HBox()#Phone
            editHBEmail = gtk.HBox()#Email
            editHBaddress1 = gtk.HBox()#address1
            editHBaddress2 = gtk.HBox()#address2
            editHBCSZ = gtk.HBox()#City State Zip
            editHBbtns = gtk.HBox()#Buttons w00t!

        #Labels
            lblfName = gtk.Label("First Name: ")
            lbllName = gtk.Label("Last Name: ")
            lblPhone = gtk.Label("Phone Number: ")
            lblEmail = gtk.Label("Email: ")
            lbladdress1 = gtk.Label("address 1: ")
            lbladdress2 = gtk.Label("address 2: ")
            lblCity = gtk.Label("City: ")
            lblState = gtk.Label("State: ")
            lblZip = gtk.Label("Zip: ")

        #Self.Input Boxes
            self.inpfName = gtk.Entry()
            self.inplName = gtk.Entry()
            self.inpPhone = gtk.Entry()
            self.inpEmail = gtk.Entry()
            self.inpaddress1 = gtk.Entry()
            self.inpaddress2 = gtk.Entry()
            self.inpCity = gtk.Entry()
            self.inpState = gtk.Entry(2)
            self.inpZip = gtk.Entry(6)
            
        #Pretty layout mod
            self.inpEmail.set_width_chars(25)
            self.inpCity.set_width_chars(10)
            self.inpState.set_width_chars(2)
            self.inpZip.set_width_chars(5)

        #Load text into inp's
            self.inpfName.set_text(self.contactsArray[toEdit].sayfName())
            self.inplName.set_text(self.contactsArray[toEdit].saylName())
            self.inpPhone.set_text(self.contactsArray[toEdit].sayPhone())
            self.inpEmail.set_text(self.contactsArray[toEdit].sayEmail())
            editAddressList = self.contactsArray[toEdit].sayAddress()
            self.inpaddress1.set_text(editAddressList[0])
            self.inpaddress2.set_text(editAddressList[1])
            self.inpCity.set_text(editAddressList[2])
            self.inpState.set_text(editAddressList[3])
            self.inpZip.set_text(editAddressList[4])

        #Buttons w00t!!
            btnOK = gtk.Button(None, gtk.STOCK_OK, False)
            btnCancel = gtk.Button(None, gtk.STOCK_CANCEL, False)
            
        #Pack lbl and self.inp's into HB's
            editHBFName.pack_start(lblfName, False, False, 2)
            editHBFName.pack_end(self.inpfName, False, False, 2)
            editHBLName.pack_start(lbllName, False, False, 2)
            editHBLName.pack_end(self.inplName, False, False, 2)
            editHBPhone.pack_start(lblPhone, False, False, 2)
            editHBPhone.pack_end(self.inpPhone, False, False, 2)
            editHBEmail.pack_start(lblEmail, False, False, 2)
            editHBEmail.pack_end(self.inpEmail, False, False, 2)
            editHBaddress1.pack_start(lbladdress1, False, False, 2)
            editHBaddress1.pack_end(self.inpaddress1, False, False, 2)
            editHBaddress2.pack_start(lbladdress2, False, False, 2)
            editHBaddress2.pack_end(self.inpaddress2, False, False, 2)
            editHBCSZ.pack_start(lblCity, False, False, 2)
            editHBCSZ.pack_start(self.inpCity, False, False, 2)
            editHBCSZ.pack_start(lblState, False, False, 2)
            editHBCSZ.pack_start(self.inpState, False, False, 2)
            editHBCSZ.pack_start(lblZip, False, False, 2)
            editHBCSZ.pack_start(self.inpZip, False, False, 2)
            editHBbtns.pack_end(btnOK, False, False, 2)
            editHBbtns.pack_end(btnCancel, False, False, 2)

        #Pack HB's into VBox
            editVBox1.pack_start(editHBFName, False, False, 2)
            editVBox1.pack_start(editHBLName, False, False, 2)
            editVBox1.pack_start(editHBPhone, False, False, 2)
            editVBox1.pack_start(editHBEmail, False, False, 2)
            editVBox1.pack_start(editHBaddress1, False, False, 2)
            editVBox1.pack_start(editHBaddress2, False, False, 2)
            editVBox1.pack_start(editHBCSZ, False, False, 2)
            editVBox1.pack_start(editHBbtns, False, False, 2)
        
            btnOK.connect("clicked", self.on_edit_ok_clicked)
            btnCancel.connect("clicked", self.on_edit_cancel_clicked)

        #Show completed UI
            self.editWindow.show_all()
            self.editWindow.show()

    def on_edit_cancel_clicked(self, widget=None):
        self.editWindow.hide()

    def on_edit_ok_clicked(self, widget=None):
        cId = self.curEditId
        fName = self.inpfName.get_text()
        lName = self.inplName.get_text()
        phone = self.inpPhone.get_text()
        email = self.inpEmail.get_text()
        address1 = self.inpaddress1.get_text()
        address2 = self.inpaddress2.get_text()
        city = self.inpCity.get_text()
        state = self.inpState.get_text()
        zip = self.inpZip.get_text()
        newAddress=[address1,address2,city,state,zip]
        self.contactsArray[cId].reName(fName, lName)
        self.contactsArray[cId].rePhone(phone)
        self.contactsArray[cId].reEmail(email)
        self.contactsArray[cId].reAddress(newAddress)
        self.editWindow.hide()
        self.perform_sorting()
        

    def show_contact(self, widget, data=None):
        toShow = self.get_selected()
        toShow = int(toShow[0])-1
        self.showWindow = gtk.Window()
        self.showWindow.set_default_size(320, 150)
        showVBox = gtk.VBox()
        self.showWindow.add(showVBox)
        if toShow > len(self.contactsArray):
            errorMessage = "No contact selected"
            errorBox = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, errorMessage)
            errorBox.run()
            errorBox.destroy()
        else:
            title="Details for: %s" % self.contactsArray[toShow].sayFullName()
            self.showWindow.set_title(title)
            self.showWindow.set_modal(True)
        
        #HBoxes to pack  into VBoxes
            showHBNames = gtk.HBox()
            showHBPhone = gtk.HBox()
            showHBEmail = gtk.HBox()
            showHBAddress1 = gtk.HBox()
            showHBAddress2 = gtk.HBox()
            showHBcsz = gtk.HBox()
            showHBbtns = gtk.HBox()
            
        #Info for labels
            contactInfo = self.contactsArray[toShow].fullInfo()
            nameLabel = "Name:        %s" % contactInfo[0]
            phoneLabel = "Phone:       %s" % contactInfo[1]
            emailLabel = "Email:        %s" % contactInfo[2]
            addressLabel1 = "Address:    %s" % contactInfo[3]
            addressLabel2 = "                  %s" % contactInfo[4]
            cszString = contactInfo[5] + ", " + contactInfo[6] + " " + contactInfo[7]
            cszLabel = "                  %s" % cszString


        #Labels
            lblName = gtk.Label(nameLabel)
            lblPhone = gtk.Label(phoneLabel)
            lblEmail = gtk.Label(emailLabel)
            lblAddress1 = gtk.Label(addressLabel1)
            lblAddress2 = gtk.Label(addressLabel2)
            lblcsz = gtk.Label(cszLabel)

        #Button
            btnClose = gtk.Button(stock=gtk.STOCK_CLOSE)

        #Packing into HB
            showHBNames.pack_start(lblName, False, False, 2)
            showHBPhone.pack_start(lblPhone, False, False, 2)
            showHBEmail.pack_start(lblEmail, False, False, 2)
            showHBAddress1.pack_start(lblAddress1, False, False, 2)
            showHBAddress2.pack_start(lblAddress2, False, False, 2)
            showHBcsz.pack_start(lblcsz, False, False, 2)
            showHBbtns.pack_end(btnClose, False, False, 2)

        #Packing to VBox
            showVBox.pack_start(showHBNames, False, False, 2)
            showVBox.pack_start(showHBPhone, False, False, 2)
            showVBox.pack_start(showHBEmail, False, False, 2)
            showVBox.pack_start(showHBAddress1, False, False, 2)
            showVBox.pack_start(showHBAddress2, False, False, 2)
            showVBox.pack_start(showHBcsz, False, False, 2)
            showVBox.pack_start(showHBbtns, False, False, 2)
            
            btnClose.connect("clicked", self.show_close_button_clicked)
            
            self.showWindow.show_all()
            self.showWindow.show()

    def show_close_button_clicked(self, widget=None):
        self.showWindow.hide()

    def remove_contact(self, widget, data=None):
        toremoveList = self.get_selected()
        if toremoveList[0] > len(self.contactsArray):
            errorMessage = "No contact selected!"
            errorBox = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, errorMessage)
            errorBox.run()
            errorBox.destroy()
        else:
            toremoveId = int(toremoveList[0])-1
            toremovefName = toremoveList[1]
            toremovelName = toremoveList[2]
            toremoveFullName = self.contactsArray[toremoveId].sayFullName()
            confirm_message = "Are you sure you want to remove " + toremoveFullName
            confirmRemove = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, confirm_message)
            confirmRemove.set_modal(True)
            resp = confirmRemove.run()
            if resp == gtk.RESPONSE_YES:
                del self.contactsArray[toremoveId]
                self.perform_sorting()
            elif resp == gtk.RESPONSE_NO:
                pass
            else:
                baderror=gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "SOMETHING WENT TERRIBLY WRONG")
                baderror.run()
                baderror.destroy()
                confirmRemove.destroy()

    def get_selected(self):
        liststore, treeiter = self.contactsListView.get_selection().get_selected()
        if treeiter is not None:
            self.selected = [liststore.get(treeiter, 0)[0], liststore.get(treeiter,1)[0], liststore.get(treeiter, 2)[0]]
            return self.selected
        else:
            errorID = len(self.contactsArray) + 10
            return [errorID]

    def main(self):
        gtk.main()

    #Internal Workings
    def _add_edit_save(self, widget, data=None):
        print "Data received: "
        print "Data: " + data
        

if __name__ == "__main__":
    gtkPyContacts = gtkPyContacts()
    gtkPyContacts.main()
    gtkPyContacts.write_contacts()
