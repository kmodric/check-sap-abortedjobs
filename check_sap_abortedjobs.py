#!/usr/bin/python

import os
os.chdir('/tmp')
#sapnwrfc - A Python interface to SAP NetWeaver R/3 systems using the RFC protocol
#SAP RFC Connector using the SAP NW RFC SDK for Python http://www.piersharding.com/blog/
#https://github.com/piersharding/python-sapnwrfc
import sapnwrfc
import sys

if len(sys.argv) <> 4:
        print "Usage:" + sys.argv[0] +" <SID> <warning shortdumps> <critical shortdumps>"
        sys.exit(3)

if os.path.exists("/etc/sapmon/"+sys.argv[1]+".yml"):
        sapnwrfc.base.config_location = "/etc/sapmon/"+sys.argv[1]+".yml"
else:
        print "File not found:" +"/etc/sapmon/"+sys.argv[1]+".yml"
        sys.exit(3)

sapnwrfc.base.load_config()

from datetime import date, timedelta
today = date.today()
yesterday = date.today() - timedelta(1)


w = " STATUS = 'A' AND ( SDLSTRTDT = '" + today.strftime('%Y%m%d') + "' OR SDLSTRTDT = '" + yesterday.strftime('%Y%m%d') + "' )"
#print w

di = { 'TEXT': w }

#print "making a new connection:"
try:
        conn = sapnwrfc.base.rfc_connect()
        fd = conn.discover("RFC_READ_TABLE")
        f = fd.create_function_call()
        f.QUERY_TABLE("TBTCO")
        f.DELIMITER(";")
        f.ROWCOUNT(10000)
        f.OPTIONS( [ di ] )
        f.FIELDS( [ {'FIELDNAME' : 'JOBNAME'},{'FIELDNAME' : 'STATUS'},{'FIELDNAME' : 'SDLSTRTDT'} ] )
        f.invoke()

        d = f.DATA.value
        todo = {'results': d}
        #print d

        number=0
        for i in d:
                        number += 1


#        print number
        abortedjobs = str(number)
        if number  >= int(sys.argv[3]):
                print "CRITICAL: Aborted jobs in 2 days -w "+sys.argv[2] +" -c "+sys.argv[3]+": "+ abortedjobs +" AbortedJobs | AbortedJobs="+abortedjobs
                sys.exit(2)
        elif number  >= int(sys.argv[2]):
                print "WARNING: Aborted jobs in 2 days  -w "+sys.argv[2] +" -c "+sys.argv[3]+": "+ abortedjobs +" AbortedJobs | AbortedJobs="+abortedjobs
                sys.exit(1)
        else:
                print "OK: Aborted jobs in 2 days -w "+sys.argv[2] +" -c "+sys.argv[3]+": "+abortedjobs+" AbortedJobs | AbortedJobs="+abortedjobs
                sys.exit(0)

        conn.close()

except sapnwrfc.RFCCommunicationError:
        print "bang!"
        if 'NO_DATA_FOUND' in e[0]:
                print "OK: Aborted jobs in 2 days -w "+sys.argv[2] +" -c "+sys.argv[3]+": 0 Aborted Jobs | AbortedJobs=0"
        else:
                print "UKNOWN:" + e[0]
                sys.exit(3)

