import sqlite3
import utils
import csv

con = sqlite3.connect('bookswort.sqlite')
cur = con.cursor()

def positionStdDev(Books_id,Words_id):
    import statistics
    cur.execute('''SELECT position FROM Textorder WHERE Books_id = ? AND
                    Words_id = ?''', (Books_id,Words_id))
    positions = [v[0] for v in cur.fetchall()]

    cur.execute(''' SELECT SUM(Counts.count) FROM Counts
                WHERE Counts.books_id = ? ''', (Books_id,))
    totalwords = cur.fetchone()[0]

    if len(positions)<2:
        return 0
    else:
        return statistics.stdev(positions)/totalwords

def buildSummary(Books_id,limit):
    cur.execute('''DELETE FROM Summary WHERE Books_id = ?''',(Books_id,))

    cur.execute('''SELECT Words.word,Words.id,Counts.count FROM Words JOIN Counts
        ON Counts.Words_id = Words.id AND Counts.Books_id = ?
        AND (Words.status = 1 OR Words.status = 2)
        ORDER BY Counts.count DESC LIMIT ? ''',(Books_id,limit))
    wordsforanalysis = cur.fetchall()

    #How many unique words in book
    cur.execute('''SELECT COUNT(Words.id) FROM Words JOIN Counts
               ON Counts.Words_id = Words.id AND Counts.Books_id = ?''',(Books_id,))
    uniquewords = cur.fetchone()[0]

    #Calculate book word Count
    cur.execute(''' SELECT SUM(Counts.count) FROM Counts
                WHERE Counts.books_id = ? ''', (Books_id,))
    totalwords = cur.fetchone()[0]

    for record in wordsforanalysis:
        Words_id = record[1]
        wordcount = record[2]
        cur.execute('SELECT permillion FROM Words WHERE id = ?', (Words_id,))
        dbpermillion = cur.fetchone()[0]
        cur.execute('SELECT status FROM Words WHERE id = ?', (Words_id,))
        status = cur.fetchone()[0]
        calcpermillion = round(wordcount / totalwords * 1000000)
        calcstdev = positionStdDev(Books_id,Words_id)
        if status == 1:
            weight = round(calcpermillion / dbpermillion)
        elif status == 2:
            weight = round(calcpermillion / 100 ) #This is the reference frequency for words wo stats

        cur.execute('SELECT * FROM Summary WHERE Books_id = ? AND Words_id=?',(Books_id,Words_id))
        row = cur.fetchone()

        if row is None: #Record does not exist in db
            cur.execute('''INSERT INTO Summary (Books_id, Words_id, permillion, weight, stdevi)
                    VALUES (?,?,?,?,?)''',(Books_id, Words_id, calcpermillion, weight, calcstdev))
        else:
            cur.execute('''UPDATE Summary SET permillion=?,weight=?,stdevi=? WHERE Books_id = ?
                         AND Words_id=?''', (calcpermillion,weight,calcstdev,Books_id,Words_id))
    con.commit()
    return

def getKeywords(Books_id, howmany):
    cur.execute('''SELECT Words.word,Counts.count FROM Words JOIN Summary JOIN Counts
                ON Words.id = Summary.Words_id AND Summary.Books_id = ?
				AND Counts.Books_id=? AND Counts.Words_id = Summary.Words_id
                ORDER BY Summary.weight * Summary.stdevi DESC LIMIT ?''',(Books_id,Books_id,howmany))
    return( cur.fetchall() )


utils.printWordsStats()
utils.printBooks()
Books_id = utils.inputBookid()

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Summary (
        Books_id    INTEGER,
        Words_id    INTEGER,
        permillion  REAL,
        weight      REAL,
        stdevi      REAL,
        PRIMARY KEY (Books_id, Words_id)
    )
''')

while True:
    inputtext = input('(1)Build Summary, (2)Display Keywords :')
    if inputtext == '1':
        limit = input('limit summary to how many of the top words: ')
        buildSummary(Books_id,limit)
    elif inputtext == '2':
        n = input('How many keywords?')
        keywords = getKeywords(Books_id,n)
        print(keywords)
        fwriter = open('keywords.csv','w',newline='')
        with fwriter:
            writer = csv.writer(fwriter)
            for row in keywords:
                writer.writerow(row)
        print('--- File keywords.csv was generated with results ---')
    elif inputtext == 'q':
        break
