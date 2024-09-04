import enum

class Columns(enum.Enum):
    VOCAB = 'Vocabulário*'
    READING = 'Leitura*'
    CLASS = 'Classe'
    MEANING = 'Significado*'
    N3_5 = 'N3-N5'

def get_front_back_from_record(record, linebreak='<br>', front_break=True) -> tuple:
    front = record[Columns.VOCAB.value]
    reading = record[Columns.READING.value]
    tl = record[Columns.MEANING.value]
    wordclass = record[Columns.CLASS.value]
    n3_5 = record[Columns.N3_5.value] == 'TRUE'
    back = f'{reading}: {tl}'
    if wordclass:
        back += f' {linebreak} {wordclass}'

    if n3_5:
        if front_break:
            front = f'{front} {linebreak} (N3-N5)'
        else:
            front = f'{front} (N3-N5)'
    return front, back