from typing import Counter
import requests
import csv
import datetime
import os.path
import argparse

#Override SmartFormatter from argparse to allow multiline help
class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

#Variable definitions
url_gnremy = 'https://gist.githubusercontent.com/gnremy/c546c7911d5f876f263309d7161a7217'
url_CPS = 'https://raw.githubusercontent.com/CriticalPathSecurity/Public-Intelligence-Feeds/master/log4j.txt'
current_time = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M")
IP_count = 0
IP_list = []
source_is_local_file = False

#Argument Parser and help
parser = argparse.ArgumentParser(formatter_class=SmartFormatter)
parser.add_argument('source', type=str, 
    help='R|Source to gather IP List\n'
        'gnremy:     ' + url_gnremy + '\n'
        'CPS:        ' + url_CPS + '\n'
        'Custom URL: Insert your custom URL to gather IP List, must be a raw IP list \n'
        'Local File: Path to your custom IP List File, must be a raw IP list'
        )
parser.add_argument('format', type=str,
    help='R|Firewall Format to generate the configuration \n'
        'ASA:       Format the output to be used as command line configuration on Cisco ASA Firewalls.\n'
        'List:      Format the out as a IP list only.'
        )
args = parser.parse_args()
IP_source = args.source
firewall_format = args.format

#Firewall Format validation
if firewall_format.upper() != 'ASA' and firewall_format.upper() != 'LIST':
    raise SystemExit(firewall_format + ' is not a valid output format.')

#URL Setting based on source argument
if IP_source == 'gnremy':
    URL_source = 'gnremy'
    url = url_gnremy + '/raw'
elif IP_source == 'CPS':
    URL_source = 'CPS'
    url = url_CPS
elif IP_source.startswith('http://') or IP_source.startswith('https://'):
    print('IP Source is a Custom URL.')
    URL_source = 'CUSTOM_URL'
    url = IP_source
else:
    print('IP Source is a local file.')
    URL_source = 'LOCAL_FILE'
    path = IP_source
    source_is_local_file = True

if source_is_local_file:
    #Get IP List from local file
    try:
        file_source = open(path, 'r')
        IP_list = file_source.readlines()
    except OSError as error:
        raise SystemExit(error)
else:
    #Validating the URL and getting response
    try:
        response = requests.get(url)
        response.raise_for_status()
        IP_list = response.text.splitlines()
    except requests.exceptions.HTTPError as error:
        raise SystemExit(error)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)

#Response parsing for gnremy source from csv to list
if IP_source == 'gnremy':
    IP_list = []
    reader = csv.DictReader(response.text.splitlines())
    for row in reader:
        IP_list.append(row['ip'])

#Verify and create output directory
if not os.path.isdir('./out'):
    try:
        os.mkdir('./out')
    except OSError:
        print("Creation of the directory ./out failed")
    else:
        print("Successfully created the directory ./out")

#Creating and opening file to save output
file =  open('out/log4j_' + firewall_format.upper() + '_' + URL_source + '_' + current_time + '.txt', 'w')

#Saving output to list only format
if firewall_format.upper() == 'LIST':
        for line in IP_list:
            file.write(line + '\n')
            IP_count += 1

#Saving output to ASA format
if firewall_format.upper() == 'ASA':
    file.write("object-group network Log4j_Blacklist_IP \n")
    for line in IP_list:
        file.write("network-object host " + line.rstrip() + "\n")
        IP_count += 1

print('Total IP from Source: ' + str(IP_count))
print('File out/log4j_' + firewall_format.upper() + '_' + URL_source + '_' + current_time + '.txt created.')