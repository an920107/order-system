from typing import Iterable, Any

def print_table(title: Iterable[Any], rows: Iterable[Iterable[Any]]) -> None:
    '''
    To print a table with the given title and rows.
    '''

    def str_len(text: str):
        length = 0
        for c in text:
            if '\u4e00' <= c <= '\u9fff':
                length += 2
            else:
                length += 1
        return length
    
    def fill_space(text: str, length: int):
        return text + ' ' * (length - str_len(text) + 1)

    max_length = [max(str_len(str(cell)) for cell in col) for col in zip(*[title, *rows])]

    print('┌' + '┬'.join('─' * (length + 1) for length in max_length) + '┐')
    print('│' + '│'.join([fill_space(str(cell), max_length[i]) for i, cell in enumerate(title)]) + '│')
    print('├' + '┼'.join('─' * (length + 1) for length in max_length) + '┤')
    for row in rows:
        print('│' + '│'.join([fill_space(str(cell), max_length[i]) for i, cell in enumerate(row)]) + '│')
    print('└' + '┴'.join('─' * (length + 1) for length in max_length) + '┘')
