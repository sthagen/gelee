# Example Usage

```
$ python -m gelee tests/fixtures
2021-04-28T22:58:54.782 INFO [gelee]: Starting validation visiting a forest with 1 tree
2021-04-28T22:58:54.788 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/toml/key_group_not_on_dedicated_line.toml with error: Key group not on a line by itself. (line 1 column 1 char 0)
2021-04-28T22:58:54.788 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/xml/empty.xml with error: ERROR: Empty XML file
2021-04-28T22:58:54.789 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/ini/missing_section_header.ini with error: File contains no section headers.file: PosixPath('tests/fixtures/invalid/ini/missing_section_header.ini'), line: 1'[section\n'
2021-04-28T22:58:54.790 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/json/invalid.json with error: Expecting property name enclosed in double quotes: line 2 column 1 (char 2)
2021-04-28T22:58:54.790 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/json/empty.geojson with error: Expecting value: line 1 column 1 (char 0)
2021-04-28T22:58:54.790 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/csv/empty.csv with error: ERROR: Empty CSV file
2021-04-28T22:58:54.791 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/yaml/unexpected-dash.yml with error: while parsing a block mapping  in "tests/fixtures/invalid/yaml/unexpected-dash.yml", line 1, column 1expected <block end>, but found '-'  in "tests/fixtures/invalid/yaml/unexpected-dash.yml", line 3, column 1
2021-04-28T22:58:54.792 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/yaml/unexpected-dash.yaml with error: while parsing a block mapping  in "tests/fixtures/invalid/yaml/unexpected-dash.yaml", line 1, column 1expected <block end>, but found '-'  in "tests/fixtures/invalid/yaml/unexpected-dash.yaml", line 3, column 1
2021-04-28T22:58:54.792 INFO [gelee]: - Successfully validated 1 total CSV file.
2021-04-28T22:58:54.792 INFO [gelee]: - Successfully validated 1 total INI file.
2021-04-28T22:58:54.792 INFO [gelee]: - Successfully validated 1 total JSON file.
2021-04-28T22:58:54.792 INFO [gelee]: - Successfully validated 1 total TOML file.
2021-04-28T22:58:54.792 INFO [gelee]: - Successfully validated 1 total XML file.
2021-04-28T22:58:54.792 INFO [gelee]: - Successfully validated 1 total YAML file.
2021-04-28T22:58:54.792 INFO [gelee]: Finished validation of 6 configuration files with 8 failures visiting 32 paths (ignored 1 non-config file in 17 folders)
FAIL
```
