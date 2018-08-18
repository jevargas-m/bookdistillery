import sqlite3

con = sqlite3.connect('bookswort.sqlite')
cur = con.cursor()

def inputBookid():
    while True:
        Books_id = input('Enter id of book under analysis: ')
        if Books_id == 'q':
            quit()

        cur.execute('SELECT name FROM Books WHERE id = ?',(Books_id,))
        bookname = cur.fetchone()
        if bookname is None:
            print('==== Book id is not valid ====')
            continue
        inputtext = 'Book under analysis is: ** ' + bookname[0] + ' ** <<yes>> to continue: '
        instruction = input(inputtext)
        if instruction == 'yes':
            return Books_id
        elif instruction == 'q':
            quit()

def statsWordsdb():
    try:
        cur.execute('''SELECT COUNT(*) FROM Words''')
        numwords = cur.fetchone()[0]
    except:
        return({'status':'Error: db has not been built, run loadbook.py first'})

    cur.execute('SELECT COUNT(*) FROM WORDS WHERE status = 1 OR status = 2')
    numfetched = cur.fetchone()[0]

    cur.execute('SELECT COUNT(*) FROM WORDS WHERE status = 1')
    numwithstats = cur.fetchone()[0]

    return {'status':'db OK','numwords':numwords,'fetched':numfetched, 'numwithstats':numwithstats}

def printWordsStats():
    ws = statsWordsdb()
    print('------------------------------')
    print('DB Status:',ws['status'])
    if 'numwords' in ws:
        print('Words in database:\t',ws['numwords'])
        print('Words fetched from API:\t',ws['fetched'])
        print('Words with stats:\t',ws['numwithstats'])
    return
