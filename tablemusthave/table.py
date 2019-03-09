import csv
import itertools

default_null_values = frozenset((
    "", "0000-00-00",
    "Null", "null",
    "NA", "N/A", "na", "n/a",
    "None", "none",
))

class Table:
    def __init__(
            self, colnames, values_by_row, null_values=default_null_values):
        colnames = list(colnames)
        values_by_column = list(
            map(list, itertools.zip_longest(*values_by_row)))

        assert(all(is_stringy(c, False) for c in colnames))
        for vals in values_by_column:
            assert(all(is_stringy(v, True) for v in vals))
        assert(len(values_by_column) == len(colnames))

        self.data = {}
        for colname, vs in zip(colnames, values_by_column):
            self.data[colname] = [
                v if v not in null_values else None
                for v in vs]

    def colnames(self):
        return list(self.data.keys())

    def get(self, colname):
        return self.data.get(colname)

    def __contains__(self, colname):
        return colname in self.data

    @classmethod
    def from_csv(cls, f, null_values=default_null_values, **csv_reader_args):
        rows = csv.reader(f, **csv_reader_args)
        colnames = next(rows)
        return cls(colnames, rows, null_values)

def is_stringy(x, can_be_none):
    if x is None:
        return can_be_none
    else:
        return isinstance(x, str)
