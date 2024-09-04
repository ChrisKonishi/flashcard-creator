import argparse
import os
import tempfile

from vocabulary import GDSpreadsheet
from flashcard import DeckCreator
from slide_creator import SlideCreator

def main(args: argparse.Namespace) -> None:
    gd = GDSpreadsheet(args.spreadsheet_id, args.credential_file, args.sheet_name)
    records = gd.get_records()

    deck = DeckCreator(args.deck_name, args.deck_id)
    deck.add_records_to_deck(records)
    output_file_deck = os.path.join(tempfile.gettempdir(), f'{args.deck_name}.apkg')
    deck.export_deck(output_file_deck)
    print(f'Deck exported to {output_file_deck}')

    sl = SlideCreator(args.deck_name)
    sl.add_records_to_slide(records)
    output_file_slide = os.path.join(tempfile.gettempdir(), f'{args.deck_name}')
    sl.export_slide(output_file_slide)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spreadsheet_id", type=str, default='1cvW0rMK9Chk_S8Nv1Af2yH7W6RP3oW4Y0OTGzg1ypEE')
    parser.add_argument("--credential_file", type=str, default="credentials.json")
    parser.add_argument("--sheet_name", type=str, default="Vocabulário")
    parser.add_argument("--deck_name", type=str, default="Guru Guru Deck")
    parser.add_argument("--deck_id", type=int, default=32131)
    args = parser.parse_args()
    main(args)