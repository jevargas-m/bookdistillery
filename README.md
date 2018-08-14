# bookdistillery

This project aims to automatically generate keywords from a text file using
Python 3.  All data is stored in a SQLite database.

For now a keyword is defined as a word that is used in the text more frequently
than in general English texts. For example words like: "the", "is" or "that" are very common on any given text so simply counting how many times a word appears on a text is not enough.  This algorithm for sure has lots of room for improvement.

keyword weight = (permillion times word appears in text / permillion times word appears in any given English corpus )


Word statistics are retrieved from WordsAPI
check https://www.wordsapi.com/docs/#frequency for reference.
#### IMPORTANT: file rauth.py needs to be renamed auth.py including your API key , for now API allows 2,500 requests per day for free, you just have to be registered in RapidAPI https://rapidapi.com/

Database structure is in database.pdf file.

## Structure
1. Use loadbook.py to load text in database, program counts how many times each words appears.  This is the first program to run as it builds the database file.  
2. Use getwordstats.py to retrieve statistics from API and store in db (Words).  Idea is to only retrieve a word from db once.
3. Use analyzebook.py to calculate keyword weight and store results in db (Summary)

## Future Improvements
### 1.How words in text are generated
1. Automatically deal with different encodings.
2. Improve REGEX to deal with different versions of same words: e.g. don't = dont, john = john's

### 2.How keyword weight is defined
1. If a word appears a lot but is not in API db, may be important anyway.  Such as person name or nickname.
2. API has lots of information that can be used such as synonyms or words that can be related together.  This could be used to look for words that are related together and give more weight. (e.g. if driver, car, gasoline are present their importance could be raised as text may be talking about a particular subject.)

### 3.Better user interface
1. Easier to use experience
2. Results visualization

## Special Thanks
This project is my final project from Python for Everybody specialization taken in Coursera https://www.py4e.com/.  Thanks to Dr.Chuck for being a great teacher.
