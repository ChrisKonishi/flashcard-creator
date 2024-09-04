import pylatex as pl
import subprocess

from util import Columns, get_front_back_from_record


class Frame(pl.base_classes.Container):
    def __init__(self, txt, **kwargs) -> None:
        super().__init__(**kwargs)
        self.txt = txt

    def dumps(self) -> str:
        string = pl.base_classes.Command('begin', 'frame').dumps()
        string += '%\n' + r'\centering'
        string += '%\n' + r'\LARGE'
        string += '%\n' + pl.NoEscape(self.txt)
        string += '%\n' + pl.base_classes.Command('end', 'frame').dumps()
        return string
    
    def __repr__(self) -> str:
        return f'Frame({self.txt})'

        # string = Command(self.latex_name + num, self.title).dumps()
        # if self.label is not None:
        #     string += "%\n" + self.label.dumps()
        # string += "%\n" + self.dumps_content()


class SlideCreator:
    def __init__(self, title) -> None:
        self.doc = pl.Document(documentclass='beamer')
        self.doc.preamble.append(pl.Command('usepackage', 'fontspec'))
        self.doc.preamble.append(pl.Command('usepackage', 'xeCJK'))
        self.doc.preamble.append(pl.Command('setCJKmainfont', 'Noto Sans CJK JP'))
        self.doc.preamble.append(pl.Command('title', title))
        self.doc.preamble.append(pl.Command('date', pl.NoEscape(r'\today')))
        author = 'グルグル組'
        self.doc.preamble.append(pl.Command('author', author))    

        self.doc.append(pl.NoEscape(r'\maketitle'))

    def add_records_to_slide(self, records) -> None:
        for record in records:
            self.add_record_to_slide(record)

    def add_record_to_slide(self, record) -> None:
        front, back = get_front_back_from_record(record, linebreak=pl.NoEscape('\\\\%\n\\vspace{0.8cm}%\n\\normalsize%\n'), front_break=True)
        
        # two slides per record, one for the front and one for the back
        self.doc.append(Frame(front))
        self.doc.append(Frame(back))
    
    def export_slide(self, output_file: str) -> None:
        # remove lastpage package
        try:
            self.doc.generate_pdf(output_file, clean_tex=False, compiler='xelatex')
        except subprocess.CalledProcessError as e:
            print(e) # Assume that the error is due to lastpage package, and the PDF is still generated
