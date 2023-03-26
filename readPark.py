# Open web Thailand Netional Park and get National Park Detail and GPS location
# by Choke E29AHU

import requests
from lxml import html
import pandas as pd



# config

# National Park Web URL
url = r"https://portal.dnp.go.th/Content/nationalpark?contentId=24757"

# Open web National Park and Get All Park ID
response = requests.get(url, verify=False)
park_urls = []
for line in response.iter_lines():
    if line:
        line = line.decode("utf-8")
        if r'https://portal.dnp.go.th/Content/nationalpark?contentId=' in line:
               park_id = line.split(r'https://portal.dnp.go.th/Content/nationalpark?contentId=')[1].split(r'"')[0]
               park_urls.append('https://portal.dnp.go.th/Content/nationalpark?contentId=' + park_id)

# Open web each park to collected park detail and GPS location.
park_names = [0] * len(park_urls)
park_locations = [0] * len(park_urls)
park_gpss = [0] * len(park_urls)
index = 0
for park_url in park_urls:
     
    # Get Parks Name
    response = requests.get(park_url, verify=False)
    tree = html.fromstring(response.content)
    for div in tree.xpath('//div[@class="headline"]'):
        if "อุทยาน" in div.text_content():
            park_names[index] = div.text_content().strip()
        

    # get Parks Province
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if "สถานที่ติดต่อ" in line:
                d1 = line.split("</strong>")[1]
                d2 = html.fromstring(d1)
                park_locations[index] = d2.text_content()

    # get Parks GPS
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if "http://www.google.co.th/maps" in line:
                d1 = line.split("dir//")[1].split("/")[0]
                park_gpss[index] = d1

    index = index +1

# Summary
print("Total " , len(park_urls) , " Parks collected")
print("Total " , len(park_names) , " Parks Name collected")
print("Total " , len(park_locations) , " Parks Location collected")
print("Total " , len(park_gpss) , " Parks GPS collected")


sumdat = [['Park Name', 'Park Location', "Park GPS"]]
for i in  range(len(park_names)):
    d1 = []
    d1.append(park_names[i])
    d1.append(park_locations[i])
    d1.append(park_gpss[i])
    sumdat.append(d1)

for element in sumdat:
    print(element)

df = pd.DataFrame(sumdat)
# Save the DataFrame to a CSV file
df.to_csv('data.csv', index=False)
