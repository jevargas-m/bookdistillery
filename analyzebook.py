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

    if len(positions)<2:
        return 0
    else:
        return statistics.stdev(positions)

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
        # Calculate usage
        calcpermillion = round(wordcount / totalwords * 1000000)
        if status == 1:
            usage = round(calcpermillion / dbpermillion)
        elif status == 2:
            usage = 0

        spread = positionStdDev(Books_id,Words_id) * calcpermillion

        cur.execute('SELECT * FROM Summary WHERE Books_id = ? AND Words_id=?',(Books_id,Words_id))
        row = cur.fetchone()

        if row is None: #Record does not exist in db
            cur.execute('''INSERT INTO Summary (Books_id, Words_id, permillion, usage, spread, statusref)
                    VALUES (?,?,?,?,?,?)''',(Books_id, Words_id, calcpermillion, usage, spread, status))
        else:
            cur.execute('''UPDATE Summary SET permillion=?,usage=?,spread=?,statusref=? WHERE Books_id = ?
                         AND Words_id=?''', (calcpermillion,usage,spread,status,Books_id,Words_id))
    con.commit()
    return

def normalizeCriteria(criteria):
    normCriteria = {}
    maximum_id = max(criteria, key=criteria.get)
    maximum = criteria[maximum_id]
    minimum_id = min(criteria, key=criteria.get)
    minimum = criteria[minimum_id]
    for key in criteria:
        normCriteria[key] = (criteria[key] - minimum) / (maximum - minimum)
    return normCriteria

def getKeywords(Books_id, howmany):
    #TODO Implement Weight algorithm for different word selection criteria

    usages = {}
    cur.execute('''SELECT Words_id, usage FROM Summary WHERE Books_id = ?
                    ORDER BY usage DESC''',(Books_id,))
    for row in cur.fetchall():
        usages[row[0]] = row[1]
    normUsages = normalizeCriteria(usages)
    print(normUsages)


    spreads = {}
    cur.execute('''SELECT Words_id, spread FROM Summary WHERE Books_id = ?
                    ORDER BY spread DESC''',(Books_id,))
    for row in cur.fetchall():
        spreads[row[0]] = row[1]


    unknowns = {}
    cur.execute('''SELECT Words_id, permillion FROM Summary WHERE Books_id = ? AND statusref = 2
                    ORDER BY permillion DESC''',(Books_id,))
    for row in cur.fetchall():
        unknowns[row[0]] = row[1]
    unknownranks = sorted(unknowns, key=unknowns.get, reverse=True)


    cur.execute('''SELECT Words.word,Counts.count FROM Words JOIN Summary JOIN Counts
                ON Words.id = Summary.Words_id AND Summary.Books_id = ?
				AND Counts.Books_id=? AND Counts.Words_id = Summary.Words_id
                ORDER BY Summary.usage * Summary.spread DESC LIMIT ?''',(Books_id,Books_id,howmany))
    return( cur.fetchall() )

# This produces a CSV file with all the analysis from Summary to use for improving algorithm parameters
def rawOutputSummary(Books_id):
    cur.execute('''SELECT Words.word,Counts.count, Summary.permillion, Summary.usage,
                    Summary.spread, Summary.statusref
                    FROM Words JOIN Summary JOIN Counts
                    ON Words.id = Summary.Words_id AND Summary.Books_id = ?
				    AND Counts.Books_id=Summary.Books_id AND Counts.Words_id = Summary.Words_id
                    ORDER BY Counts.count DESC''',(Books_id,))
    fwriter = open('rawoutput.csv','w',newline='')
    with fwriter:
        writer = csv.writer(fwriter)
        writer.writerow(('Word','Count','perMillion','usage','spread','StatusRef'))
        for row in cur.fetchall():
            writer.writerow(row)
            print(row)
    print('--- File rawoutput.csv was generated with results ---')
    return

utils.printWordsStats()
utils.printBooks()
Books_id = utils.inputBookid()

#TODO Merge Summary table with Counts table
cur.executescript('''
    CREATE TABLE IF NOT EXISTS Summary (
        Books_id    INTEGER,
        Words_id    INTEGER,
        permillion  REAL,
        usage       REAL,
        spread      REAL,
        statusref   INTEGER,
        PRIMARY KEY (Books_id, Words_id)
    )
''')

while True:
    inputtext = input('(1)Build Summary, (2)Generate Keywords, (3)Raw Output, (q) Quit :')
    if inputtext == '1':
        limit = input('limit summary to how many of the top words, type <<all>> to use all words): ')
        if limit == 'all':
            limit = 10000000 #TODO Put actual limit from SQL Query
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
    elif inputtext == '3':
        rawOutputSummary(Books_id)
    elif inputtext == 'q':
        break
