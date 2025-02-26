import csv
import itertools

default_null_values = frozenset(
    (
        "",
        "0000-00-00",
        "Null",
        "null",
        "NA",
        "N/A",
        "na",
        "n/a",
        "None",
        "none",
    )
)


class Table:
    def __init__(self, colnames, values_by_row, null_values=default_null_values):
        colnames = list(colnames)
        values_by_column = list(map(list, itertools.zip_longest(*values_by_row)))

        if not all(is_stringy(c, False) for c in colnames):
            msg = "Expected column names to be strings. Saw {0}"
            raise TypeError(msg.format(colnames))
        for vals in values_by_column:
            if not all(is_stringy(v, True) for v in vals):
                msg = "Expected table values to be strings or None. Saw {0}"
                raise TypeError(msg.format(vals))
        if not (len(values_by_column) == len(colnames)):
            msg = (
                "Expected number of column names to equal number of columns"
                "of values. Saw {0} column names and {1} columns of values."
            )
            raise ValueError(msg.format(len(colnames), len(values_by_column)))

        self.data = {}
        for colname, vs in zip(colnames, values_by_column):
            self.data[colname] = [v if v not in null_values else None for v in vs]

    def colnames(self):
        return list(self.data.keys())

    def normal_colnames(self):
        return {normalize_name(c): c for c in self.colnames()}

    def get(self, colname):
        return self.data.get(colname)

    def __contains__(self, colname):
        return colname in self.data

    @classmethod
    def from_csv(cls, f, null_values=default_null_values, **csv_reader_args):
        rows = csv.reader(f, **csv_reader_args)
        colnames = next(rows)
        return cls(colnames, rows, null_values)

    @classmethod
    def from_data(cls, data, null_values=default_null_values):
        """Read a dictionary into the Table format.

        Args:
            data (dict[str, str | None]): A dictionary with column names as keys and lists of values as values.
            null_values (iterable, optional): Null values to recognize. Defaults to default_null_values.

        Returns:
            Table: A Table object with the column-wise data from the dictionary converted into Table's row-wise format.
        """
        return cls(
            data.keys(), list(zip(*[data[col] for col in data.keys()])), null_values
        )


def is_stringy(x, can_be_none):
    if x is None:
        return can_be_none
    else:
        return isinstance(x, str)


def normalize_name(name):
    return "".join(ch for ch in name.strip().lower() if ch.isalnum()) if name else ""
