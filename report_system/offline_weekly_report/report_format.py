import pandas as pd
'''
import numpy as np
data = pd.DataFrame(np.zeros((5,7)))
filename='test.xlsx'
sheet='shot'
engine='xlsxwriter'
'''


def area_format(data, filename, sheet, engine='xlsxwriter'):
    rows = len(data.index)
    cols = len(data.columns)

    writer = pd.ExcelWriter(filename, engine=engine)
    data.to_excel(writer, index=False, sheet_name=sheet)

    workbook = writer.book
    worksheet = writer.sheets[sheet]

    col_fmt = workbook.add_format({'valign': 'middle',
                                   'align': 'center',
                                   'font': 'Arial',
                                   'size': 10})

    label_fmt = workbook.add_format({'bold': True,
                                     'fg_color': '#339966',
                                     'border': 1})
    # set label:
    worksheet.set_row(0, 40.0, cell_format=label_fmt)
    # set row:
    for rownum in range(1, rows+1):
        worksheet.set_row(rownum, 40.0, col_fmt)

    # set column:
    worksheet.set_column('A:R', 18.75, col_fmt)

    writer.save()
