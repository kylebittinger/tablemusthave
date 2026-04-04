import unittest
from tablemusthave.table import *
from . import table1_cols, table1_vals


class TableTests(unittest.TestCase):
    def setUp(self):
        self.t = Table(table1_cols, table1_vals)

    def test_column_names(self):
        self.assertEqual(self.t.colnames(), ["col0", "col1", "col2", "col3", "col4"])

    def test_vals_for(self):
        self.assertEqual(self.t.get("col1"), ["b", None, "h"])

    def test_has_column(self):
        self.assertIn("col1", self.t)

    def test_nulls(self):
        t = Table(["a", "b"], [[None, "None"], ["NA", "c"]])
        self.assertEqual(t.get("a"), [None, None])
        self.assertEqual(t.get("b"), [None, "c"])

    def test_from_csv(self):
        t = Table.from_csv(["a,b", "1,2", "NA,3"])
        self.assertEqual(t.get("a"), ["1", None])
        self.assertEqual(t.get("b"), ["2", "3"])

    def test_from_csv_nulls(self):
        t = Table.from_csv(["a,b", "1,2", "NA,3"], null_values=["3"])
        self.assertEqual(t.get("a"), ["1", "NA"])
        self.assertEqual(t.get("b"), ["2", None])

    def test_from_tsv(self):
        t = Table.from_csv(["a\tb", "1\t2", "NA\t3"], delimiter="\t")
        self.assertEqual(t.get("a"), ["1", None])
        self.assertEqual(t.get("b"), ["2", "3"])

    def test_from_data(self):
        t = Table.from_data({"a": ["1", "2"], "b": ["3", "4"]})
        self.assertEqual(t.get("a"), ["1", "2"])
        self.assertEqual(t.get("b"), ["3", "4"])

    def test_normalize_name(self):
        self.assertEqual(normalize_name("Col_1"), "col1")
        self.assertEqual(normalize_name("col1"), "col1")
        self.assertEqual(normalize_name("col 1"), "col1")
        self.assertEqual(normalize_name("col_1"), "col1")
        self.assertEqual(normalize_name("COL-1 "), "col1")
        self.assertEqual(normalize_name(" C$O%L^1"), "col1")
