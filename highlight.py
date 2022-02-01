from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename)
from typing import IO

def highlight_file(file: str, type = 'cs'):
    return highlight_file_io(open(file, mode = 'r'), type)

def highlight_file_io(file: IO, type = 'cs'):
    return highlight_string(file.read(), type)

def highlight_string(contents: str, type = 'cs'):
    return highlight(contents, get_lexer_by_name(type), HtmlFormatter(noclasses = True, style = 'vs'))