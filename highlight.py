from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename)
from typing import IO

def highlight_file(file: str, type = 'c#', style = 'vs', encoding = 'utf_8_sig'):
    return highlight_file_io(open(file, mode = 'r', encoding=encoding), type)

def highlight_file_io(file: IO, type = 'c#', style = 'vs'):
    return highlight_string(file.read(), type)

def highlight_string(contents: str, type = 'c#', style = 'vs'):
    return highlight(contents, get_lexer_by_name(type), HtmlFormatter(noclasses = True, style = style))