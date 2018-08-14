import sqlite3
import auth, utils

con = sqlite3.connect('bookswort.sqlite')
cur = con.cursor()

try:
    cur.execute('''SELECT COUNT(*) FROM Words''')
except:
    print('=== Error: db has not been built, run loadbook.py first ===')
    quit()

print('database has',cur.fetchone()[0],'words')

Books_id = utils.inputBookid()

cur.execute('''SELECT COUNT(Words.id) FROM Words JOIN Counts
           ON Counts.Words_id = Words.id AND Counts.Books_id = ?''',(Books_id,))
numwords = cur.fetchone()[0]
print('Book has',numwords,'words')

getnum = input('How many of the top words to ensure have stats in db: ')

cur.execute('''SELECT Words.word,Words.status FROM Words JOIN Counts
    ON Counts.Words_id = Words.id AND Counts.Books_id = ? AND Words.status = 0
    ORDER BY Counts.count DESC LIMIT ?''',(Books_id,getnum))
wordswostats = cur.fetchall()

print('===============================================================')
print('From top',getnum,'words,',len(wordswostats),'do not have stats')
inputtext = input('Do you want to retreive from wordsapiv1 the missing words <<yes>>: ')

#get from API
if inputtext == 'yes':
    for word in wordswostats:
        word = word[0]
        res = auth.getfreq(word)
        print('************* word: ',word)
        print(res)
        if 'frequency' not in res:
            print('word not found or stats not present, status = 2')
            cur.execute('UPDATE Words SET status=2 WHERE word = ?', (word,))

        if 'frequency' in res:
            print('word found !!, status = 1')
            zipf = res['frequency']['zipf']
            permillion = res['frequency']['perMillion']
            diversity = res['frequency']['diversity']
            cur.execute('''
                    UPDATE Words SET status=1,zipf=?,permillion=?,diversity=?
                    WHERE word = ?''', (zipf,permillion,diversity,word))
        print('------------------------------------------------------------')
        con.commit()
