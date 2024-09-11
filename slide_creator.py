import pylatex as pl
import subprocess
import os

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
    
    def remove_lastpage(self, tex_file):
        with open(tex_file, 'r') as file:
            lines = file.readlines()

        with open(tex_file, 'w') as file:
            for line in lines:
                # Skip the line with the lastpage package
                if '\\usepackage{lastpage}' not in line:
                    file.write(line)

    def export_slide(self, output_file: str) -> None:
        output_file_tex = output_file
        self.doc.generate_tex(output_file_tex)
        output_file_tex += '.tex'
        self.remove_lastpage(output_file_tex)
        basename = os.path.basename(output_file_tex)

        subprocess.run(['xelatex', basename], check=True, cwd=os.path.dirname(output_file_tex))

        self.cleanup(output_file)

    def cleanup(self, output_file: str) -> None:
        os.remove(output_file + '.aux')
        os.remove(output_file + '.log')
        os.remove(output_file + '.nav')
        os.remove(output_file + '.out')
        os.remove(output_file + '.snm')
        os.remove(output_file + '.tex')
        os.remove(output_file + '.toc')
