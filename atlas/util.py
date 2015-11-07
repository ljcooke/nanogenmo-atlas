import textwrap


DEFAULT_TEXT_WIDTH = 78


def titlecase(text):
    return ' '.join(t.capitalize() for t in text.split())

def wrap(text, width=DEFAULT_TEXT_WIDTH, indent=''):
    return textwrap.fill(text, width,
                         initial_indent=indent,
                         subsequent_indent=indent,
                         break_long_words=False,
                         break_on_hyphens=False)
