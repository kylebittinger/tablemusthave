#import tablemusthave
from tablemusthave import *

chop_mandatory = [
        "SampleID", "SampleType", "reverse_barcode_plate",
        "reverse_barcode_location", "forward_barcode_plate",
        "forward_barcode_location", "flow_cell_id",
]

specification = MustHave(
    columns_named(chop_mandatory),
    columns_matching("^[0-9A-Za-z._]+$"),
    columns_matching("^[A-Za-z]"),
    values_matching("SampleID", "^[0-9A-Za-z.]+$"),
    values_matching("SampleID", "^[A-Za-z]"),
    unique_values("SampleID"),
    values_matching("reverse_barcode_location", "^[A-H][0-9]{2}$"),
    unique_values_together([
        "reverse_barcode_location", "reverse_barcode_plate",
        "forward_barcode_location", "forward_barcode_plate",
    ]),
    values_matching("forward_barcode_location", "^[A-H][0-9]{2}$"),
    )
specification.extend(some_value(c) for c in chop_mandatory)

for d in specification.descriptions():
    print(d)
print()

with open('usda21.csv', newline='') as f:
    t = Table.from_csv(f)

for req, res in specification.check(t):
    print(req.description())
    print(res.message())
