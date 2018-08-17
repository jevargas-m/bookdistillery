SELECT Words.word,Summary.weight, Summary.stdevi FROM Words JOIN Summary
                ON Words.id = Summary.Words_id AND Summary.Books_id = 4
                ORDER BY Summary.weight DESC