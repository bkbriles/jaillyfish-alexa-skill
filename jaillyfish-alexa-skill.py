from flask import Flask
from flask_ask import Ask, statement, question, session
import bs4
import requests

app = Flask(__name__)
ask = Ask(app, "/ngrok_testing_env")


def jaillyfish():
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

    return len(jaillyfish)
    '''
    if len(jaillyfish) == 0:
        # no one you know is in jail
        return 0
    else:
        for i in range(len(jaillyfish)):
            print(jaillyfish[i])
    '''

@app.route('/')
def homepage():
    return "ngrok_testing_env"

@ask.launch
def start_skill():
    welcome_msg = "Do you want me to check if any of your friends are in jail?"
    return question(welcome_msg)

@ask.intent("YesIntent")
def yes_intent():
    number_in_jail = jaillyfish()
    if number_in_jail == 0:
        roster_msg = "It doesn't look like anyone you know is in Marion County Jail."
    else:
        roster_msg = 'Uh oh, it looks like people you know are in jail.'
    return statement(roster_msg)

@ask.intent("NoIntent")
def no_intent():
    closing_msg = 'Okay, goodbye.'
    return statement(closing_msg)

'''
if __name__ == '__main__':
    app.run(debug=True)
'''