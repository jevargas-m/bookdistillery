# file needs to be renamed auth.py and <<<your key>>> needs RapidAPI key

import requests

def getfreq(word):
    r = requests.get('https://wordsapiv1.p.mashape.com/words/'+ word + '/frequency',
headers={"X-Mashape-Key": '<<<your key>>>',
"X-Mashape-Host": "wordsapiv1.p.mashape.com"})

    return r.json()
