# check-sap-abortedjobs
Nagios plugin for checking SAP Aborted jobs in last two days

![](/images/check_sap_abortedjobs2.png)

![](/images/check_sap_abortedjobs.png)


Usage:./check_sap_abortedjobs.py \<SID\> \<warning shortdumps\> \<critical shortdumps\>

### Example:
root@:~/github# ./check_sap_abortedjobs.py SBX 10 20

OK: Aborted jobs in 2 days -w 10 -c 20: 0 AbortedJobs | AbortedJobs=0

                                                                      
### Prerequisite:
Installation of sapnwrfc for python on Linux and Unix
https://wiki.scn.sap.com/wiki/display/EmTech/Installation+of+sapnwrfc+for+python+on+Linux+and+Unix





To prepare a script, you'll need a 'yml' file similar to the 'sap.yml' file included with the sapnwrfc download. The file looks 

like this:
#### Example of SID.yml file

ashost: gecko.local.net

sysnr: "01"

client: "001"

user: developer

passwd: developer

lang: EN

trace: 3

loglevel: warn
