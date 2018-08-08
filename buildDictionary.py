import re
import sqlite3


db = sqlite3.connect('database.db')
currentId = 1
totalCount = db.execute("select count(*) from labeled_sentences").fetchone()[0]
wordPattern = r"(\w+)[\s\W]+"

aeiouPattern = r"[a|e|i|o|u]\w*"
bcdfgPattern = r"[b|c|d|f|g]\w*"
hjklmPattern = r"[h|j|k|l|m]\w*"
pqrstPattern = r"[p|q|r|s|t]\w*"


while currentId < totalCount :
    sentence = db.execute("select sentence from labeled_sentences where id=?",(currentId,)).fetchone()[0]
    currentId = currentId+1
    #disamble
    groups = re.findall(wordPattern,sentence)
    
    if (currentId % 1000) == 0 :
        print(currentId)

    for word in groups:
        #not case sensitive
        word = word.lower()
        #aeiou sort
        if re.match(aeiouPattern,word) :
            table = "word_dictionary_aeiou"
        elif re.match(bcdfgPattern,word) :
            table = "word_dictionary_bcdfg"
        elif re.match(hjklmPattern,word) :
            table = "word_dictionary_hjklm"
        elif re.match(pqrstPattern,word) :
            table = "word_dictionary_pqrst"
        else :
            table = "word_dictionary_else"    
        

        #query table if existed
        _id = db.execute('select id from {0} where word=?'.format(table),(word,)).fetchone()
        if not _id :
            db.execute('insert into {0} values (NULL,?,1)'.format(table),(word,))
        else  :
            counter = db.execute('select counter from {0} where id=?'.format(table),_id).fetchone()[0]
            counter = counter+1
            db.execute('update  {0} set counter=? where id=?'.format(table),(counter,_id[0]))

    db.commit()