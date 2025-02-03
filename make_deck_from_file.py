import os
import random
from collections import defaultdict
import pandas as pd
import genanki
from slide_creator import SlideCreator
from util import Columns

SHUFFLE = True

WRITE = '◆'
READ = '◇'

df = pd.read_excel('QUARTET_word_index.xlsx', header=None)

df.columns = ['idx', 'reading', 'kanji', 'tl', 'req1', 'l1', 'req2', 'l2']

deck_dict = {}
lesson_set = defaultdict(set)
document_dict = {}


st = """
    .card {
        font-family: arial;
        font-size: 20px;
        text-align: center;
        color: black;
        background-color: white;
    }
"""

my_model = genanki.Model(
1607392319,
'Simple Model',
fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
],
templates=[
    {
    'name': 'Card 1',
    'qfmt': '{{Question}}',
    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'
    },
],
css=st)

def get_lesson_deck(lesson):
    if lesson not in deck_dict:
        deck_dict[lesson] = genanki.Deck(random.randint(1, 1000000000), lesson)

    return deck_dict[lesson]

def get_lesson_document(lesson):
    if lesson not in document_dict:
        document_dict[lesson] = SlideCreator(lesson)
    return document_dict[lesson]

def add_to_deck(front, reading, tl, req, lesson, make_pdf=True):
    if front in lesson_set[lesson]:
        print(f'Duplicate: {front}. Not adding to deck.')
        return
    if not lesson:
        return
    if pd.isnull(front):
        front = reading
    if not pd.isnull(req):
        front = f'{front} {req}'
    # By adding the lesson to back, we can avoid duplicates
    back = f'{reading}: {tl}<br><br>{lesson}'
    note = genanki.Note(
        model=my_model,
        fields=[front, back]
    )
    deck = get_lesson_deck(lesson)
    deck.add_note(note)

    if make_pdf:
        if front.endswith(WRITE):
            front = front.replace(WRITE, '**')
        elif front.endswith(READ):
            front = front.replace(READ, '*')
        document = get_lesson_document(lesson)
        record = {Columns.VOCAB.value: front, Columns.READING.value: reading, Columns.MEANING.value: tl, Columns.CLASS.value: None, Columns.N3_5.value: False}
        document.add_record_to_slide(record)

def parse_lesson(l):
    if pd.isnull(l):
        return None
    # L11-読1
    return l

df['l1'] = df['l1'].apply(parse_lesson)
df['l2'] = df['l2'].apply(parse_lesson)

for idx, row in df.iterrows():
    front = row['kanji']
    reading = row['reading']
    tl = row['tl']

    add_to_deck(front, reading, tl, row['req1'], row['l1'])
    add_to_deck(front, reading, tl, row['req2'], row['l2'])
    if not pd.isnull(row['req1']) or not pd.isnull(row['req2']):
        lesson = f'{row["l1"]} - Essential'
        add_to_deck(front, reading, tl, row['req1'], lesson)
    # if not pd.isnull(row['req1']):
    #     lesson = f'{row["l1"]} - Essential'
    #     add_to_deck(front, reading, tl, row['req1'], lesson)
    # if not pd.isnull(row['req2']):
    #     lesson = f'{row["l2"]} - Essential'
    #     add_to_deck(front, reading, tl, row['req2'], lesson)
        
def romanize_lesson_name(lesson):
    if not lesson:
        return None
    tks = lesson.split('-')
    return f'{tks[0]}-{tks[1][1:]}'

os.makedirs('decks', exist_ok=True)
os.makedirs('slides', exist_ok=True)

for lesson, deck in deck_dict.items():
    genanki.Package(deck).write_to_file(f'decks/{lesson}.apkg')

for lesson, document in document_dict.items():
    filepath_no_ext = f'slides/{lesson}'
    if SHUFFLE:
        document.shuffle()
    document.export_slide(filepath_no_ext)
