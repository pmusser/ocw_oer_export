# OCW OER Export

This demonstration project showcases how to utilize the MIT Open API. It specifically focuses on extracting MIT OpenCourseWare courses' metadata and creating a CSV file for export to OER Commons, aligning with their specific [requirements](https://help.oercommons.org/support/solutions/articles/42000046853-import-resources-with-the-bulk-import-template).

**SECTIONS**

1. [Initial Setup & Usage](#initial-setup)
1. [Requirements](#requirements)
1. [Tests](#tests)
1. [Committing & Formatting](#committing-&-formatting)


## Initial Setup & Usage

The _ocw_oer_export_ package is available [on PyPI](link). To install:

```
pip install ocw_oer_export
```

### Usage as a Python Package

To use `ocw_oer_export` in your Python code:

```
from ocw_oer_export import create_csv
create_csv()
```

By default, the `create_csv` function uses `source="api"` and `output_file="ocw_oer_export.csv"`. The `source` parameter can be altered to `source="json"` if a local JSON file of courses' metadata is available. To generate the JSON file:

```
from ocw_oer_export import create_json
create_json()
```

Then, create the CSV from the JSON file:

```
create_csv(source="json")
```

### CLI Usage

`ocw_oer_export` also provides a Command Line Interface (CLI). After installation, you can use the following commands:

To create the CSV file:

```
ocw-oer-export --create_csv
```

To generate a JSON file:

```
ocw-oer-export --create_json
```

To create a CSV file from the local JSON file:

```
ocw-oer-export --create_csv --source=json
```

## File Output Directory

When using either the Python package or the CLI, the output files (CSV or JSON) are saved in the current working directory from which it is executed.

## Requirements

For successful execution and correct output, ensure the [MIT Open's API](https://mit-open-rc.odl.mit.edu//api/v1/courses/?platform=ocw) contains the following fields:

`title`, `url`, `description`, `topics`, `course_feature`, `runs: instructors`

Additionally, the `mapping_files` should be up-to-date. If new topics are added in OCW without corresponding mappings in `ocw_oer_export/mapping_files/ocw_topic_to_oer_subject.csv`, this will lead to `null` entries for those topics in the CSV (`CR_SUBJECT`).

## Tests

To run unit tests:

```
python -m unittest discover
```

## Committing & Formatting

To ensure commits to GitHub are safe, first install [pre-commit](https://pre-commit.com/):

```
pip install pre-commit
pre-commit install
```

Running pre-commit can confirm your commit is safe to be pushed to GitHub and correctly formatted:

```
pre-commit run --all-files
```
