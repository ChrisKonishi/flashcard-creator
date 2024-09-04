# Flashcard Creator
Takes a spreadsheet with vocabulary and creates flashcards (Anki and PDF)

## Requirements

- Tested on python3.10 and python.3.12
- Install the required packages with `pip install -r requirements.txt`
- A LaTeX distribution (e.g. MiKTeX, TeX Live) is required to generate PDFs
- A Google service account with access to Google Sheets API and Google Drive API, with the credentials saved in a JSON file
- Noto Sans CJK JP font
  > sudo apt-get install "fonts-noto-cjk"
