import json
import sys
import argparse
from pymongo import MongoClient

QUESTION_START = ('Who', 'Which', 'Where', 'When', 'What', 'Why', 'How', 'Identify')
TOPIC = '- (Topic'
QUESTION_END = 'Answer:'
CHOICES = ('A. ', 'B. ', 'C. ', 'D. ')


def is_question(text) -> bool:
    if (text.startswith(QUESTION_START) or text.__contains__('?') or text.endswith("?")):
        return True
    else:
        return False

def is_answer(text) -> bool:
    return True if text.startswith(QUESTION_END) else False
    
def is_choice(text):
    return True if text.startswith(CHOICES) else False

def is_topic(text):
    return True if text.__contains__(TOPIC) else False

def add_to_db(question):
    try:
        client = MongoClient("connection_string_here")
        db = client['db_name']
        collection = db['collectoin_name']
    except Exception as e:
        print('Unable to connect', e)
    try:
        collection.insert_one(question)
        print('Done \n', question)
    except Exception as e:
        print('{e}')


if __name__ == '__main__':
    with open('prince.txt', 'r') as f, open('out.txt', '+w') as out:
        QS = []
        QA = {}
        q, end = False, False
        for line in f:
            if line == '\n':
                continue
            if is_question(line):
                q = True
            elif is_topic(line):
                QA['topic'] = line
                continue
            elif is_choice(line):
                try:
                    QA['choices'].append(line)
                    q = False
                    continue
                except (KeyError, AttributeError):
                    QA['choices'] = [line]
                    q = False
                    continue
            elif is_answer(line):
                end = True
                QA['answer'] = line.split(':')[1].strip()
                continue
            if q:
                try:
                    QA["question"] += line
                    continue
                except (KeyError, AttributeError):
                    QA["question"] = line
                    continue
            if end:
                QS.append(QA)
                add_to_db(QA)
                QA = {}
        out.write(json.dumps(QS))

    #TODO
    # Create online mongoDB database and load quetions to the database (done)
    # Create simple React App to interact with the database