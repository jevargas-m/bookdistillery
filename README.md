# bookdistillery

This project aims to automatically generate keywords from a text file using
Python 3.  All data is stored in a SQLite database.

For now a keyword is defined as a word that is used in the text more frequently
than in general English texts.  This has lots of room for improvement
keyword weight = (permillion times word appears in text / permillion times word appears in any given Engligh corpus )


Word statistics are retreived from WordsAPI
check https://www.wordsapi.com/docs/#frequency for reference.
#### Important file rauth.py needs to be renamed auth.py including your API key , for now API allows 2,500 requests per day for free, you just have to be registered in RapidAPI https://rapidapi.com/

Database structure is in database.pdf file.

## Structure
1. Use loadbook.py to load text in database, program counts how many times each words appears.  This is the first program to run as it builds the database file.
2. Use getwordstats.py to retreive statistics from API and store in db.
3. Use analyzebook.py to calculate keyword weight and store results in db (Summary)

## Special Thanks
This project is my final project from Python for Enverybody specialization taken in Coursera.  Thanks to Dr.Chuck for being a great teacher.
