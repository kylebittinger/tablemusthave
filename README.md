# tablemusthave

A python library to define and check constraints for data arranged in a table.

## Summary

We developed this library to use with tables of sample information in
DNA sequencing experiments.  Here, the table must have columns with
certain names, which are used by downstream appplications. For
example, we require a column of sample identifiers named `SampleID`.
Some of the columns must have values matching a pattern, for example,
sample identifiers must begin with a letter to avoid errors in our
bioinformatics pipelines. Some columns must always be filled in,
whereas others are optional.  For example, we always need a value for
the sample identifier.

This library allows users to define a specification in python code.
Here's a spec for the examples above:

```python
from tablemusthave import (
    MustHave, columns_named, values_matching, some_value_for,
)

spec = MustHave(
    columns_named("SampleID"),
    values_matching("SampleID", "^[A-Za-z]"),
    some_value_for("SampleID")
)
```

Once defined, we can import a table and check it over to see if it
meets our spec.  Tables can be imported or created using the `Table`
class.  From there, the specification can be used to check the columns
and values in the table.  It returns an iterable of pairs, where the
first element is the requirement checked, and the second element is
the result of the check (success or failure).

```python
from tablemusthave import Table

my_table = Table.from_csv("my_file.csv")

for requirement, result in spec.check(my_table):
    print(requirement.description())
    print(result.message())
```

## Installation

To install, clone or download this library, move to the library
directory, and type:

```python
pip install .
```

## Other work

The specifications in this library are very similar to table
definitions in SQL. There is an R library with similar functionality,
[`spec`](https://cran.r-project.org/web/packages/spec/), which seemed
nice but did not quite suit our needs.
