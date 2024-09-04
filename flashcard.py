import genanki

from util import Columns, get_front_back_from_record

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

class DeckCreator:
    def __init__(self, deck_name: str, deck_id: int) -> None:
        self.deck = genanki.Deck(deck_id, deck_name)
    
    def add_records_to_deck(self, records) -> None:
        for record in records:
            self.add_record_to_deck(record)
        
    def add_record_to_deck(self, record) -> None:
        front, back = get_front_back_from_record(record)
        note = genanki.Note(
            model=my_model,
            fields=[front, back]
        )
        self.deck.add_note(note)

    def export_deck(self, output_file: str) -> None:
        genanki.Package(self.deck).write_to_file(output_file)
