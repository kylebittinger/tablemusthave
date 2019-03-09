import unittest

from tablemusthave.table import *
from tablemusthave.musthave import *

table1_vals = [
    ["a", "b", "c", "m", "r"],
    ["d", None, "f", "m", "r"],
    ["g", "h", None, "q", "r"],
]
table1_cols = [
    "col0", "col1", "col2", "col3", "col4"
]

class TableTests(unittest.TestCase):
    def setUp(self):
        self.t = Table(table1_cols, table1_vals)

    def test_column_names(self):
        self.assertEqual(
            self.t.colnames(),
            ["col0", "col1", "col2", "col3", "col4"])

    def test_vals_for(self):
        self.assertEqual(self.t.get("col1"), ["b", None, "h"])

    def test_has_column(self):
        self.assertIn("col1", self.t)

    def test_columns_named(self):
        req = columns_named(["col0"])
        res = req.check(self.t)
        self.assertTrue(res.success)

    def test_columns_named_fail(self):
        req = columns_named(["zzz"])
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.missing, ["zzz"])

    def test_columns_matching(self):
        req = columns_matching("^col\\d$")
        res = req.check(self.t)
        self.assertTrue(res.success)

    def test_columns_matching_fail(self):
        req = columns_matching("col[1234]")
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.not_matching, ["col0"])

    def test_values_in_set(self):
        accept = ["a", "b", "c", "d", "e", "f", "g"]
        req = values_in_set("col0", accept)
        res = req.check(self.t)
        self.assertTrue(res.success)

    def test_values_in_set_fail(self):
        req = values_in_set("col0", ["a", "b", "d"])
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.not_allowed, ["g"])

    def test_some_value(self):
        req = some_value("col0")
        res = req.check(self.t)
        self.assertTrue(res.success)

    def test_some_value_fail(self):
        req = some_value("col1")
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.idxs, [2])

    def test_some_value_if_another_filled(self):
        # If column 2 is filled in, then column 0 is filled in; True
        req = some_value("col2", "col0")
        res = req.check(self.t)
        self.assertTrue(res.success)

    def test_some_value_if_another_filled_fail(self):
        # If column 0 is filled in, then column 2 is filled in; False
        req = some_value("col0", "col2")
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.idxs, [3])

    def test_values_matching(self):
        res = values_matching("col1", "^[a-z]$").check(self.t)
        self.assertTrue(res.success)

    def test_values_matching_fail(self):
        req = values_matching("col1", "^[a-d]$")
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.not_matching, ["h"])

    def test_unique_values(self):
        req = unique_values("col1")
        res = req.check(self.t)
        self.assertTrue(res.success)

    def test_unique_values_fail(self):
        req = unique_values("col3")
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.repeated, [(("m", ), 2)])
    
    def test_unique_values_together(self):
        req = unique_values("col0", "col1")
        res = req.check(self.t)
        self.assertTrue(res.success)

    def test_unique_values_together_fail(self):
        req = unique_values("col3", "col4")
        res = req.check(self.t)
        self.assertFalse(res.success)
        self.assertEqual(res.repeated, [(("m", "r"), 2)])

    def test_column_missing(self):
        reqs = [
            values_in_set("colz", ["a"]),
            some_value("colz"),
            some_value("colz", "col0"),
            values_matching("colz", "abc"),
            unique_values("colz"),
            unique_values("colz", "col0"),
            ]
        for req in reqs:
            res = req.check(self.t)
            # success is None if the column is missing
            self.assertIsNone(res.success)

    def test_message(self):
        self.assertIn("zzz1", StillNeeds(missing="zzz1").message())
        self.assertIn("zzz2", StillNeeds(not_matching="zzz2").message())
        self.assertIn("1", StillNeeds(idxs=[0]).message())
        self.assertIn("zzz3", StillNeeds(not_allowed="zzz3").message())
        self.assertIn("zzz4", StillNeeds(repeated=[("zzz4", 2)]).message())
