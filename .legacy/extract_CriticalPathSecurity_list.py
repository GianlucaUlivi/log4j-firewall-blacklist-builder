import requests
import datetime
import os.path

url = 'https://raw.githubusercontent.com/CriticalPathSecurity/Public-Intelligence-Feeds/master/log4j.txt'
response = requests.get(url)
count = 0
list = response.text.splitlines()
current_time = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M")

if not os.path.isdir('./out'):
    try:
        os.mkdir('./out')
    except OSError:
        print("Creation of the directory ./out failed")
    else:
        print("Successfully created the directory ./out")

with open('out/log4j_IP_List_CriticalPathSecurity_' + current_time + '.txt', 'w') as f:
    for line in list:
        f.write(line + "\n")
        count += 1

print("Total IP in List: " + str(count))