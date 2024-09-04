import gspread
import typing as t

from util import Columns

class GDSpreadsheet:
    def __init__(self, spreadsheet_id, credential_file, sheet_name):
        self.spreadsheet_id = spreadsheet_id
        self.credential_file = credential_file
        self.sheet_name = sheet_name
        self.gc = gspread.service_account(filename=self.credential_file)
        self.records = self.read_sheet(self.sheet_name)
        self.records = [i for i in self.records if i[Columns.VOCAB.value]] # Remove empty rows



    def read_sheet(self, sheet_name):
        sheet = self.gc.open_by_key(self.spreadsheet_id).worksheet(sheet_name)
        return sheet.get_all_records()
    
    def get_records(self) -> t.List[t.Dict[str, str]]:
        return self.records
