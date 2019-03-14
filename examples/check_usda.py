#import tablemusthave
from tablemusthave import *
from pathlib import Path

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
    unique_values_for("SampleID"),
    values_matching("reverse_barcode_location", "^[A-H][0-9]{2}$"),
    unique_values_for(
        "reverse_barcode_location", "reverse_barcode_plate",
        "forward_barcode_location", "forward_barcode_plate",
    ),
    values_matching("forward_barcode_location", "^[A-H][0-9]{2}$"),
    some_value_for("SubjectID", "HostSpecies"),
    )
specification.extend(some_value_for(c) for c in chop_mandatory)

for d in specification.descriptions():
    print(d)
print()

csv_fp = Path(__file__).resolve().parent / "usda21.csv"
with open(csv_fp, newline='') as f:
    t = Table.from_csv(f)

for req, res in specification.check(t):
    print(req.description())
    print(res.message())
