#This program creates db, reads a text file and stores words and word count into db
#word status: 0: default value, unknown; 1: Retrieved, 2: word not found in API

import sqlite3
import re

con = sqlite3.connect('bookswort.sqlite')
cur = con.cursor()

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Books (
        id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name        TEXT UNIQUE,
        filename    TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Words (
        id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        word        TEXT UNIQUE,
        status      INTEGER DEFAULT 0,
        zipf        REAL,
        permillion  REAL,
        diversity   REAL
    );

    CREATE TABLE IF NOT EXISTS Counts (
        Books_id    INTEGER,
        Words_id    INTEGER,
        count       INTEGER,
        PRIMARY KEY (Books_id, Words_id)
    );

    CREATE TABLE IF NOT EXISTS Textorder (
        Books_id    INTEGER,
        position    INTEGER,
        Words_id    INTEGER,
        PRIMARY KEY (Books_id, position)
    )
''')

filename = input('Enter file name, type <<q>> to quit: ')
if filename == 'q': quit()

try:
    path = 'Books/'
    fhandler = open(path+filename, encoding='UTF-8')
except:
    print('==== invalid file ====')
    quit()

#Seek if file has already been processed
#TODO process and rewrite existing files
cur.execute('SELECT id FROM Books WHERE filename = ?',(filename,))
row = cur.fetchone()
if row is not None:
    print('=====File already processed=====')
    quit()

name = input('Enter Book name: ')

cur.execute('INSERT INTO Books (filename,name) VALUES ( ?,? )',(filename,name))
con.commit()
cur.execute('SELECT id FROM Books WHERE filename = ? ',(filename,))
Books_id = cur.fetchone()[0]

position = 0
for line in fhandler:
    # Everything in lower case ignoring punctuation
    #TODO try str.maketrans instead
    line = line.lower()
    words = re.sub(r'[^\w\s]','',line).split()

    for word in words:
        #find if word is already in db, insert and get id
        cur.execute('SELECT id FROM Words WHERE word = ?', (word,))
        row = cur.fetchone()
        if row is None: #word is not already in db
            cur.execute('INSERT INTO Words (word) VALUES (?)', (word,))
            cur.execute('SELECT id FROM Words WHERE word = ?', (word,))
            row = cur.fetchone()
        Words_id = row[0]

        position += 1
        cur.execute('''INSERT INTO Textorder (Books_id,position,Words_id) VALUES
            (?,?,?)''',(Books_id,position,Words_id))

        cur.execute('''SELECT Counts.count
                        FROM Books JOIN Words JOIN Counts
                        ON Counts.Books_id = ? AND
                            Counts.Words_id = ? ''',(Books_id, Words_id))
        row = cur.fetchone()
        # word does not exist in Counts
        if row is None:
            cur.execute('''INSERT INTO Counts (Books_id, Words_id, count) VALUES
                (?,?,1)''', (Books_id,Words_id))
        # word already exists in Counts
        else:
            cur.execute('''UPDATE Counts SET count = count + 1 WHERE
            (Books_id=? AND Words_id=?) ''', (Books_id,Words_id))

    con.commit() #commit once per line

print('File:',filename,'has been succesfully processed')
