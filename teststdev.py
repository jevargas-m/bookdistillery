import sqlite3
import utils


con = sqlite3.connect('bookswort.sqlite')
cur = con.cursor()

def positionStdDev(Books_id,Words_id):
    import statistics
    cur.execute('''SELECT position FROM Textorder WHERE Books_id = ? AND
                    Words_id = ?''', (Books_id,Words_id))
    positions = [v[0] for v in cur.fetchall()]
    return statistics.stdev(positions)


try:
    cur.execute('''SELECT COUNT(*) FROM Words''')
except:
    print('=== Error: db has not been built, run loadbook.py first ===')
    quit()

Books_id = utils.inputBookid()

word = input('word id =')

print(positionStdDev(Books_id,word))
