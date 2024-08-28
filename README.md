# OCW OER Export

This demonstration project showcases how to utilize the MIT Learn API. It specifically focuses on extracting MIT OpenCourseWare courses' metadata and creating a CSV file for export to OER Commons, aligning with their specific [requirements](https://help.oercommons.org/support/solutions/articles/42000046853-import-resources-with-the-bulk-import-template).

**SECTIONS**

1. [Initial Setup & Usage](#initial-setup)
1. [Requirements](#requirements)
1. [Tests](#tests)
1. [Committing & Formatting](#committing-&-formatting)


## Initial Setup & Usage

1. Build the container:

```
docker compose build
```

2. Start the container:

```
docker compose run --rm app
```

To generate a JSON file containing complete API data:

```
docker compose run --rm app --create_json
```

To create a CSV file from the local JSON file:

```
docker compose run --rm app --create_csv --source=json
```

## File Output Directory

The output files, whether in CSV or JSON format, are stored within the `private/output` directory relative to the current working directory from which the command is executed.

Therefore, the above commands will generate `private/output/ocw_oer_export.csv` or `private/output/ocw_api_data.json` in the current working directory.

If you want to change this, you will not only have to change the `output_path` in the function (`create_csv` or `create_json`) but also have to change the mapping in `docker-compose.yml`.

## Environment Variables

By default, this project uses MIT Learn's Production API, as given in `ocw_oer_export/config.py`.
To use the RC API or local, create an environment file, `.env` in the project's root directory and add the relevant base URL:
e.g., `API_BASE_URL=https://api.rc.learn.mit.edu` or `API_BASE_URL=http://localhost:8063`

## Requirements

For successful execution and correct output, ensure the [MIT Learn's API](https://api.rc.learn.mit.edu/api/v1/courses/?platform=ocw) contains the following fields:

`title`, `url`, `runs: level`, `description`, `topics`, `runs: instructors`, `runs: semester`, `runs: year`, `course_feature`
Additionally, the `mapping_files` should be up-to-date. If new topics are added in OCW without corresponding mappings in `ocw_oer_export/mapping_files/ocw_topic_to_oer_subject.csv`, this will lead to `null` entries for those topics in the CSV (`CR_SUBJECT`). In addition to that, make sure `fm_keywords_exports.csv` is also present.

## Tests

To run unit tests:

```
docker run --rm ocw_oer_export python -m unittest discover -s tests
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
