#!/usr/bin/env python3

from flask import Flask
from flask_ask import Ask, statement, question
import bs4
import requests

app = Flask(__name__)
ask = Ask(app, "/ngrok_testing_env")

def jaillyfish():
    url = "http://apps.co.marion.or.us/JailRosters/mccf_roster.html"
    keywords = ['ACATECA-HERNANDEZ'] # TEST CASE
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
        return "It doesn't look like anyone you know is in Marion County Jail."
    elif len(jaillyfish) == 1:
        name = '... '.join(jaillyfish)
        return "Uh oh. Someone you know is in jail. {} is in Marion County Jail.".format(name)
    else:
        name = '... '.join(jaillyfish)
        return "Uh oh. Some people you know are in jail. {}, are in Marion County Jail.".format(name)

@app.route('/')
def homepage():
    return "ngrok_testing_env"

@ask.launch
def start_skill():
    welcome_msg = "Do you want me to check if any of your friends are in jail?"
    return question(welcome_msg)

@ask.intent("YesIntent")
def yes_intent():
    roster_msg = jaillyfish()
    return statement(roster_msg)

@ask.intent("NoIntent")
def no_intent():
    closing_msg = 'Okay, goodbye.'
    return statement(closing_msg)

if __name__ == '__main__':
    app.run(debug=True)
