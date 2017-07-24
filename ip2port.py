#!/usr/bin/python

import commands
import cgi
import string
import requests
import sys

#INIT ERROR CONDITION
ERROR="NO"

#GRAB INPUT FROM HTML FORM
form = cgi.FieldStorage()
ip = form.getvalue('ip')

#FORMAT DAT CRAP
splitip = ip.split('.')
tgtip = splitip[0]+"."+splitip[1]+"."+splitip[2]+"."+"1"


#BASED ON INPUT, DECIPHER VLAN- THIS IS BASED ON MY ADDRESS SCHEME.  PART OF THE CAVEAT THAT THIS IS TAILORED FOR MY DESIGN.  THIS IS PART OF MY TEMPLATE
if int(splitip[2]) < 100:
	vlan = "2000"

if (int(splitip[2]) > 99 and int(splitip[2]) < 200):
        vlan = "2001"

if int(splitip[2]) > 199:
        vlan = "2002"

#SNMP CALL TO GRAB ARP INFO
GETARP = commands.getstatusoutput('snmpwalk -v2c -c SNMPKEY@'+vlan+' '+tgtip+' .1.3.6.1.2.1.3.1.1.2 | grep "'+ip+' "')

#ERROR CONDITIONS
if (tgtip == ip):
	ERROR="ERROR"

if str(GETARP[0])=="256":
	ERROR="ERROR"
else:
	GETARP=GETARP[1] 


#IF NO ERROR< PROCEED 
if (ERROR <> "ERROR"):
	#GRAB SWITCHNAME
	SWITCHNAME = commands.getstatusoutput('snmpwalk -v2c -c SNMPKEY '+tgtip+' SNMPv2-MIB::sysName.0')
	SWITCHNAME = SWITCHNAME[1].split('STRING: ')
	SWITCHNAME = SWITCHNAME[1]
	
	STRIPMAC = GETARP.split('STRING:')
	STRIPMAC = STRIPMAC[1]

	#PULL MAC FORM SWITCH BASED ON ARP
	GETMAC = commands.getstatusoutput('snmpwalk -v2c -c SNMPKEY@'+vlan+' '+tgtip+' .1.3.6.1.2.1.17.4.3.1.1 | grep "'+STRIPMAC+'"')
	GETMAC = GETMAC[1]
	
	STRIPID = GETMAC.split('= Hex-STRING: ')
	GETMAC = STRIPID[1]
	GETMAC = GETMAC.replace(' ',':')
	GETMAC = GETMAC[:-1]
	STRIPID = STRIPID[0].split('4.3.1.1')
	STRIPID = STRIPID[1].strip(' ')
	#FIND INTERFACE CONNECTED TO MAC BASED ON PREVIOUS
	GETINTERFACE = commands.getstatusoutput('snmpwalk -v2c -c SNMPKEY@'+vlan+' '+tgtip+' .1.3.6.1.2.1.17.4.3.1.2 | grep "'+STRIPID+'"')
	GETINTERFACE = GETINTERFACE[1]
	GETINTERFACE = GETINTERFACE.split('INTEGER: ')
	GETINTERFACE = GETINTERFACE[1]
	#FIND INTERFACE INDEX
	GETINDEX = commands.getstatusoutput('snmpwalk -v2c -c SNMPKEY@'+vlan+' '+tgtip+' .1.3.6.1.2.1.17.1.4.1.2 | grep "2.'+GETINTERFACE+' "')
	GETINDEX = GETINDEX[1].split('INTEGER: ')
	GETINDEX = GETINDEX[1]
	#CORRELATE INTERFACE NAME
	GETIFNAME = commands.getstatusoutput('snmpwalk -v2c -c SNMPKEY@'+vlan+' '+tgtip+' IF-MIB::ifName.'+GETINDEX)
	GETIFNAME = GETIFNAME[1].split('STRING: ')
	GETIFNAME = GETIFNAME[1]

	print "Content-type: text/html\n"
	print "\n\n"
	print "<HTML>"
	print "<HEAD>"
	print "<TITLE>Port Locator Tool</TITLE>"
	print "</HEAD>"
	print "<CENTER>"
	print "<BODY bgcolor='#07BF1A'>"
	print "<BR>"
	print "<BR>"
	print '<h1>Device Locator Tool</h1>'
	print '<TABLE bgcolor="white" border="1" cellpadding="10"> '
	print '<TR><TD><p>SWITCH: </TD><TD>'+SWITCHNAME+'</TD></TR>'
	print '<TR><TD><p>HOST IP: </TD><TD>'+ip+'</TD></TR>'
	print '<TR><TD><p>MAC: </TD><TD>'+GETMAC+'</TD></TD>'
	print '<TR><TD><p>VLAN: </TD><TD>'+vlan+'</TD></TR>'
	print '<TR><TD><p>INTERFACE: </TD><TD>'+GETIFNAME+'</TD></TR>'
	print '</TABLE>'
	print "<br><hr>"
	print "<CENTER>"
else:
	print "Content-type: text/html\n"
        print "\n\n"
        print "<HTML>"
        print "<HEAD>"
        print "<TITLE>Port Locator Tool</TITLE>"
        print "</HEAD>"
        print "<CENTER>"
        print "<BODY bgcolor='#07BF1A'>"
        print "<BR>"
        print "<BR>"
	if (ip == tgtip):
		print "<H1>You have entered in a gateway address, try again."
	else:
		print "<H1>ERROR, NO ARP ENTRY FOUND FOR "+ip+"</H1>"
		print "<p>Please try again!</p>"
print '<form action="/ip/ip2port.py" method="post">'
print '<input autofocus title="Please enter the host IP appropriately!!" required type="text" name="ip" pattern="\\b(10)\\.(14[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\b">'
print '<input type="submit" value="Submit">'

