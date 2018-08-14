import sqlite3

con = sqlite3.connect('bookswort.sqlite')
cur = con.cursor()

def inputBookid():
    while True:
        Books_id = input('Enter id of book under analysis: ')
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
