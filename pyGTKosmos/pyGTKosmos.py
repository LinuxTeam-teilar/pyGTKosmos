#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PyCosmos version 0.5 fork by forfolias
 
import urllib
import httplib2
import pygtk
import sys
if not sys.platform == 'win32': 
    pygtk.require('2.0')
import gtk
import os.path
import encodings.idna
import encodings.ascii
import re

VER="0.5"
NAME="PyGTKosmos"
 
class PyCosmos:
                def on_change(self, widget, label):
                        label.set_text(str(140-buffer.get_char_count()) + " left")
                        if buffer.get_char_count() > 140:
                                iter = buffer.get_end_iter()
                                buffer.backspace(iter, True, True)
                def about_on_clicked(self, widget):
                        about = gtk.AboutDialog()
                        about.set_program_name(NAME)
                        about.set_version(VER)
                        about.set_copyright("(c) George Vasilakos")
                        about.set_comments("This script allows sending SMS using\nthe MyCosmos portal of COSMOTE in\nGreece. This script is a fork of\nPyCosmos 0.4 authored by Sakis Kanaris.")
                        about.set_website("http://pycosmos.sourceforge.net/")
                        about.run()
                        about.destroy()
                def options(self, widget, window):
                        opt_win= gtk.Dialog(NAME + " options", window, gtk.DIALOG_MODAL, None)
                        opt_win.add_button("Cancel", 0)
                        opt_win.add_button("Save", 1)
                        usr_label = gtk.Label("Username : ")
                        usr_entry = gtk.Entry(max=10)
                        hbox = gtk.HBox(True, 2)
                        hbox.pack_start(usr_label, False, False, 2)
                        hbox.pack_start(usr_entry, False, False, 2)
                        opt_win.vbox.pack_start(hbox, False, False, 2)
                        hbox1 = gtk.HBox(True, 2)
                        pass_label = gtk.Label("Password : ")
                        pass_entry = gtk.Entry()
                        pass_entry.set_visibility(False)
                        hbox1.pack_start(pass_label, False, False, 2)
                        hbox1.pack_start(pass_entry, False, False, 2)
                        opt_win.vbox.pack_start(hbox1, False, False, 2)
                        try:
                                f = open(conf_file, 'r')
                                temp = f.readline()
                                temp = temp[0:-1]
                                usr_entry.set_text(temp)
                                temp = f.readline()
                                temp = temp[0:-1]
                                pass_entry.set_text(temp)
                                f.close()
                        except:
                                usr_entry.set_text("")
                                pass_entry.set_text("")
                        opt_win.show_all()
                        response_id = opt_win.run()
                        if response_id   == 1:
                                f = open(conf_file, 'w')
                                f.write(usr_entry.get_text() + '\n')
                                f.write(pass_entry.get_text() + '\n')
                                f.close()
                        opt_win.destroy()
                def on_button_clicked(self, widget):
                        try:
                                f = open(conf_file, 'r')
                                tel = f.readline()
                                tel = tel[0:-1]
                                pas = f.readline()
                                pas = pas[0:-1]
                                f.close()
                        except:
                                tel = ""
                                pas = ""
#                        dst = "0030" + dst_entry.get_text()
                        dst = dst_entry.get_text()
                        msg = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)

                        # regular expression:
                        # start with maybe 00 or '+' for any number
                        # for Greece    : (3069 OR 69 ) + 8 digits.
                        # for not Greece: + 1 digit nonzero + digits.
                        patternOFnumber='(00|[\+])?((((30)?69[0-9]{8})|(?!3069)(?!69)[1-9][0-9]{1,3}[0-9]{7,12}))'

                        # up to 10 numbers separated with comma
                        pattern = "^" + patternOFnumber + "(,"  +  patternOFnumber + "){0,9}" +"$"
                        if not re.search(pattern,dst):
                            text= "Destination number is not valid!"
                            statusbar.push(0, text)
                            return 1
                        h0 = httplib2.Http()
                        location0 = "http://mail.mycosmos.gr/mycosmos/login.aspx"
                        resp0, content0 = h0.request(location0, "GET")
                        cookie = resp0['set-cookie']
                        aspsessid = cookie.split()[0].split(';')[0]
                        viewstate = content0.split('VIEWSTATE')[1].split('"')[2]
                        mybody1=urllib.urlencode({
                                "__VIEWSTATE": viewstate,
                                "tbUsername": tel,
                                "tbPassword": pas,
                                "btLogin": "Σύνδεση",
                                "rbSecurityPub": "rbSecurityPub"
                        })                  
                        length1=len(mybody1)
                        myheaders1={
                                "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
                                "Referer": location0,
                                "Accept-Language": "el",
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Accept-Encoding": "gzip, deflate",
                                "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 3.51; SV1; .NET CLR 2.0.50727)",
                                "Host": "mail.mycosmos.gr",
                                "Connection": "Keep-Alive",
                                "Content-Length": str(length1),
                                "Cache-Control": "no-cache",
                                "Cookie": aspsessid
                        }
                        h1 = httplib2.Http()
                        resp1, content1 = h1.request(location0, "POST",  headers=myheaders1, body=mybody1)
                        cookie1 = resp1['set-cookie']
                        sessionid = cookie1.split()[0]
                        cadata = cookie1.split()[2].split(';')[0]
                        location = "http://mail.mycosmos.gr/mycosmos/SMS_Send.aspx?Theme=0"
                        myheaders={
                                "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
                                "Accept-Language": "el",
                                "Accept-Encoding": "gzip, deflate",
                                "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 3.51; SV1; .NET CLR 2.0.50727)",
                                "Host": "mail.mycosmos.gr",
                                "Connection": "Keep-Alive",
                                "Cookie": aspsessid+"; "+sessionid+" "+cadata
                        }
                        mybody=urllib.urlencode({ })
                        h = httplib2.Http()
                        resp, content = h.request(location, "GET", body=mybody, headers=myheaders)
                        viewstate = content.split('VIEWSTATE')[1].split('"')[2]
                        location2 = "http://mail.mycosmos.gr/mycosmos/SMS_Send.aspx?Theme=0"
                        mybody2=urllib.urlencode({
                                "__VIEWSTATE": viewstate,
                                "txtMobile": dst,
                                "txtMessage": msg,
                                "btnSend": "Αποστολή"
                        })
                        length=len(mybody2)
                        myheaders2={
                                "Accept": "image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*",
                                "Referer": location,
                                "Accept-Language": "el",
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Accept-Encoding": "gzip, deflate",
                                "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 3.51; SV1; .NET CLR 2.0.50727)",
                                "Host": "mail.mycosmos.gr",
                                "Content-Length": str(length),
                                "Connection": "Keep-Alive",
                                "Cache-Control": "no-cache",
                                "Cookie": aspsessid+"; "+sessionid+" "+cadata
                        }
                        resp2, content2 = h.request(
                                location2,
                                "POST",
                                body=mybody2,
                                headers=myheaders2
                                )
                        location3 = resp2['location']
                        try:
                            status=location3.split('Success=')[1].split('&')[0]
                            if status == "True":
                                statusbar.push(0, "Message sent successfully!")
                                return 0
                            if status == "False":
                                statusbar.push(0, "Message was not sent successfully. Maybe message limit is reached.")
                                return 1
                        except:
                            statusbar.push(0, "An unknown error occured. Maybe the source number is not registered in Mycosmos.")
                            return 1
 
                def __init__(self):
                        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                        window.set_title(NAME + " " + VER)
                        window.set_size_request(300, 178)
                        window.set_position(gtk.WIN_POS_CENTER)
                        window.connect("delete_event", lambda w,e: gtk.main_quit())
                        global dst_entry
                        global buffer
                        global statusbar
                        global conf_file
                        if sys.platform == 'win32': 
                                conf_file = os.path.expanduser("~") + '/pycosmos.conf'
                        else:
                                conf_file = os.path.expanduser("~") + '/.pycosmos.conf'
                        vbox = gtk.VBox(False, 2)
                        window.add(vbox)
                        window.set_resizable(False)
                        vbox.show()
                        hbox = gtk.HBox(False, 2)
                        dst_label = gtk.Label("Send to : ")
                        hbox.pack_start(dst_label, False, False, 2)
                        dst_entry = gtk.Entry(max=109) # 10 numbers * 10 free sms + 9 seperators
                        dst_entry.set_text("69")
                        hbox.pack_start(dst_entry, False, False, 2)
                        button = gtk.Button("  Send  ")
                        button.connect("clicked", self.on_button_clicked)
                        hbox.pack_start(button, False, False, 2)
                        vbox.pack_start(hbox, False, False, 2)
 
                        hbox1 = gtk.HBox(False, 2)
                        vbox1 = gtk.VBox(False, 2)
                        msg_label = gtk.Label("Message : ")
                        vbox1.pack_start(msg_label, False, False, 2)
                        char_label = gtk.Label("140 left")
                        vbox1.pack_start(char_label, False, False, 2)
                        opt_button = gtk.Button("Options")
                        opt_button.connect("clicked", self.options, window)
                        vbox1.pack_start(opt_button, False, False, 2)
                        about_button = gtk.Button("About")
                        about_button.connect("clicked", self.about_on_clicked)
                        vbox1.pack_start(about_button, False, False, 2)
                        hbox1.pack_start(vbox1, False, False, 2)
                        textview = gtk.TextView()
                        textview.set_size_request(220, 90)
                        textview.set_wrap_mode(gtk.WRAP_WORD)
                        buffer = textview.get_buffer()
                        buffer.connect("changed", self.on_change, char_label)
                        textview.set_accepts_tab(False)
                        hbox1.pack_start(textview, False, False, 0)
                        vbox.pack_start(hbox1, False, False, 2)
                        statusbar = gtk.Statusbar()
                        vbox.pack_start(statusbar, False, False, 0)
                        window.show_all()
 
def main():     
                        gtk.threads_init()
                        gtk.threads_enter()
                        gtk.main()
                        gtk.threads_leave()
                        return 0
 
if __name__ == "__main__":
                        PyCosmos()
                        main()

