#!/usr/bin/python
import serial
import MySQLdb
import datetime
import sys
from datetime import timedelta
i=0
while 1:
	ser = serial.Serial(
        	port='/dev/ttyUSB0',
     		parity=serial.PARITY_NONE,
     		bytesize=serial.EIGHTBITS,
     		stopbits=serial.STOPBITS_ONE,
     		#timeout=3,
     		xonxoff=0,
     		rtscts=0,
     		baudrate=9600
   	)	

        g=ser.read(3)
	print g
	s=str(g)
	#d='249'
	#if s==d:
	print 'Trying to connect with MySQL'

	conn=MySQLdb.connect(host="localhost",
                        user="root",
                        passwd="vinay007",
                        db="final")
	x=conn.cursor()
	print 'Connected to MySQL'
        
	try:
		print 'in try...'
               	now=datetime.datetime.now()
               	datestr = now.strftime("%Y-%m-%d %H:%M:%s")
             	due=now + timedelta(days=15)
		dd=str(datestr)
               	duedate=str(due)
		loc='Hadapsar'
		fine='500'
               	#print dd
		x.execute('INSERT INTO ticket values("%s","%s","%s")'%(s,dd,loc))
		print 'Chassis number received'
		conn.commit()
		try:
			x.execute('INSERT INTO generated_ticket(chassisno,number_plate,name,address,contact_no,fine,issue_date,due_date) SELECT vehicaldata.chassisno,vehicaldata.number_plate,vehicaldata.name,vehicaldata.address,vehicaldata.contact_no,"%s","%s","%s" FROM vehicaldata WHERE vehicaldata.chassisno="%s"'%(fine,dd,duedate,s))
			#print x.fetchone()
			
		except MySQLdb.Error, e:
    			try:
        			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    			except IndexError:
        			print "MySQL Error: %s" % str(e)
	

		conn.commit()
		print 'Ticket generated against chassis number %s' %(s)
       		conn.close()
	except:
		print 'Exception occured while generating Ticket'
	        conn.rollback()

	ser.close()
