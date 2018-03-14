import bs4
import requests

url = "http://apps.co.marion.or.us/JailRosters/mccf_roster.html"
keywords = ['ACATECA-HERNANDEZ', 'ZIELINSKI'] # TEST CASE
jaillyfish = []

# scrape data from url and convert to type bs4
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'lxml')

# soup.select('a') instead?
roster = soup.find_all('a')

# iterate through roster[i].get_text()
for i in range(len(roster)):
    if any(keyword in roster[i].get_text(strip=True) for keyword in keywords):
        jaillyfish.append(roster[i].get_text(strip=True))
        print(roster[i].get_text(strip=True)) #DEBUG
    
if len(jaillyfish) == 0:
    # no one you know is in jail
    print('no one is in')
else:
    for i in range(len(jaillyfish)):
        print(jaillyfish[i])

    
    # known to work
    # roster[i].get_text(strip=True)