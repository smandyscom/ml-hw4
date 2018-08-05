import re
import sqlite3


db = sqlite3.connect('database.db')
file_training_data = open('training_label.txt','r')

linePattern = r"^([0|1])[\s](\+\+\+\$\+\+\+)[\s](.+)$"
wordPattern = ""

while True :
    line =file_training_data.readline()
    if not line:
        break # empty string
    #disamble
    match = re.match(linePattern,line)
    label = match.group(1)
    sentence = match.group(3)
    # write into database
    db.execute("insert into labeled_sentences  values (NULL,?,?)",(label,sentence))

db.commit()

