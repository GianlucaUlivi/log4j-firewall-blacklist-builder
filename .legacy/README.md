# Legacy scripts

### cisco_ASA_format_CriticalPathSecurity.py and cisco_ASA_format_gnremy.py
Will download a public IP List and format it to be used on a Cisco ASA.  
This will create a txt file with the configuration ready to be copy-pasted into a Cisco ASA, it will create a Network Group named "Log4j_Blacklist_IP" with all IP as hosts inside of it.  
Deleting the Netwrok Group will also delete all hosts.  


### extract_CriticalPathSecurity_list.py and extract_gnremy_list.py
Will download a public IP List and create a list with IP only, one per line in a txt file. 