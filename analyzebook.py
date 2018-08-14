import sqlite3
import utils

con = sqlite3.connect('bookswort.sqlite')
cur = con.cursor()

try:
    cur.execute('''SELECT COUNT(*) FROM Words''')
except:
    print('=== Error: db has not been built, run loadbook.py first ===')
    quit()

Books_id = utils.inputBookid()

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Summary (
        Books_id    INTEGER,
        Words_id    INTEGER,
        permillion  REAL,
        weight      REAL,
        PRIMARY KEY (Books_id, Words_id)
    )
''')

#Calculate book word Count
cur.execute(''' SELECT SUM(Counts.count) FROM Counts
            WHERE Counts.books_id = ? ''', (Books_id,))
totalwords = cur.fetchone()[0]

#How many of the top words have stats in db
cur.execute('''SELECT Words.word,Words.id,Counts.count FROM Words JOIN Counts
    ON Counts.Words_id = Words.id AND Counts.Books_id = ? AND Words.status = 1
    ORDER BY Counts.count DESC ''',(Books_id,))
wordsforanalysis = cur.fetchall()

#How many unique words in book
cur.execute('''SELECT COUNT(Words.id) FROM Words JOIN Counts
           ON Counts.Words_id = Words.id AND Counts.Books_id = ?''',(Books_id,))
uniquewords = cur.fetchone()[0]

print('Book has',totalwords,'words,',uniquewords,'are unique and top',len(wordsforanalysis),'have stats')

for record in wordsforanalysis:
    Words_id = record[1]
    wordcount = record[2]
    cur.execute('SELECT permillion FROM Words WHERE id = ?', (Words_id,))
    dbpermillion = cur.fetchone()[0]
    calcpermillion = round(wordcount / totalwords * 1000000)
    weight = round(calcpermillion / dbpermillion)

    cur.execute('SELECT * FROM Summary WHERE Books_id = ? AND Words_id=?',(Books_id,Words_id))
    row = cur.fetchone()

    if row is None: #Record does not exist in db
        cur.execute('''INSERT INTO Summary (Books_id, Words_id, permillion, weight)
                VALUES (?,?,?,?)''',(Books_id, Words_id, calcpermillion, weight))
    else:
        cur.execute('''UPDATE Summary SET permillion=?,weight=? WHERE Books_id = ?
                     AND Words_id=?''', (calcpermillion,weight,Books_id,Words_id))
con.commit()
print('==== Analysis Completed ====')

inputtext = input('Words to show: ')
cur.execute('''SELECT Words.word,Summary.weight FROM Words JOIN Summary
                ON Words.id = Summary.Words_id AND Summary.Books_id = ?
                ORDER BY Summary.weight DESC LIMIT ?''', (Books_id,inputtext))
row = cur.fetchall()
i = 1
print('#    word    weight')
for word,weight in row:
    print(i,':\t',word,'\t',weight)
    i+=1
