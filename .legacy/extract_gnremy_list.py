import requests
import csv
import datetime
import os.path

url = 'https://gist.githubusercontent.com/gnremy/c546c7911d5f876f263309d7161a7217/raw'
response = requests.get(url)
results = []
reader = csv.DictReader(response.text.splitlines())
count = 0
current_time = datetime.datetime.now().strftime("%Y-%b-%d_%H-%M")

if not os.path.isdir('./out'):
    try:
        os.mkdir('./out')
    except OSError:
        print("Creation of the directory ./out failed")
    else:
        print("Successfully created the directory ./out")

for row in reader:
    results.append(row)

with open('out/log4j_IP_List_gnremy_' + current_time + '.txt', 'w') as f:
    for d in results:
        f.write(d['ip'] + "\n")
        count += 1

print("Total IP in List: " + str(count))