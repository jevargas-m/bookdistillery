mashkey = '<<RapidAPI key>>'
mashhost = '<<WordsAPI host>>'

def getfreq(word):
    import requests
    r = requests.get('https://wordsapiv1.p.mashape.com/words/'+ word + '/frequency',
headers={"X-Mashape-Key": mashkey,
"X-Mashape-Host": mashhost})

    return r.json()
