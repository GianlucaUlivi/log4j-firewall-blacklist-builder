# Log4j-Firewall-Blacklist-Builder

# Requirements:  
 - Python3  
 - Python3 requests module  


# Usage and details:
## log4j_blacklist_builder.py
All in one script.
Run "python3 log4j_blacklist_builder.py -h" for help.
Multiple input source:
- gnremy git
- Critical Path Security (CPS) gits
- Custom URL (must be a raw IP list)
- Local File (must be a raw IP list)
Multiple Output formats:
 - Cisco ASA
 - Fortinet Fortigate
 - Plain List

Other scripts have been moved to legacy.

### IP List Sources
Critical Path Security gits: https://raw.githubusercontent.com/CriticalPathSecurity/Public-Intelligence-Feeds/master/log4j.txt  
gnremy gits: https://gist.githubusercontent.com/gnremy/c546c7911d5f876f263309d7161a7217
