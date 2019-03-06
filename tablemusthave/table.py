import csv
import itertools

class Table:
    def __init__(self, colnames, values_by_row):
        colnames = list(colnames)
        values_by_column = list(
            map(list, itertools.zip_longest(*values_by_row)))

        assert(all(is_stringy(c, False) for c in colnames))
        for vals in values_by_column:
            assert(all(is_stringy(v, True) for v in vals))
        assert(len(values_by_column) == len(colnames))

        self.data = dict(zip(colnames, values_by_column))

    def colnames(self):
        return list(self.data.keys())

    def get(self, colname):
        return self.data.get(colname)

    def __contains__(self, colname):
        return colname in self.data

    @classmethod
    def from_csv(cls, f, **csv_reader_args):
        rows = csv.reader(f, **csv_reader_args)
        colnames = next(rows)
        return cls(colnames, rows)

def is_stringy(x, can_be_none):
    if x is None:
        return can_be_none
    else:
        return isinstance(x, str)
