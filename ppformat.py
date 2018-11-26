def format_table(rows, header=None):
    columns = max(len(row) for row in rows)
    column_widths = [max([len(h) for h in header]+[len(row[c]) for row in rows]) for c in range(0,columns)]
    head_rows = []
    if header is not None:
        head_rows = [header]
    return '\n'.join([('  '.join(h.upper().ljust(cwidth) for (h,cwidth) in zip(header,column_widths))),
                      ('  '.join(cwidth*"-" for (h,cwidth) in zip(header,column_widths)))]
                     +[('  '.join(cell.ljust(cwidth) for (cell,cwidth) in zip(row,column_widths))) for row in rows])

def dimensionality(val):
    if isinstance(val, list):
        return 1+dimensionality(val[0])
    else:
        return 0

def format_obj_table(val, columns):
    return format_table(
        [[("{0:.2f}€".format(v[col]/100.0) if col=='price' else pp(v[col])) for col in columns] for v in val],
        header=[c for c in columns])

def pp(val):
    if isinstance(val, str):
        return val
    if isinstance(val, list):
        d = dimensionality(val)
        if d == 1:
            if isinstance(val[0], dict):
                return format_obj_table(val, val[0].keys())
            else:
                return '\n'.join(pp(v) for v in val)
        elif d == 2:
            return format_table([[pp(cell) for cell in row] for row in val])
    return str(val)
