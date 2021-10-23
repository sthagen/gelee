# Use

<!-- MarkdownTOC -->

- Examples
  - Version
  - General Help
  - Cook Help
  - Cook

<!-- /MarkdownTOC -->

## Examples

### Version

```console
$ gelee version
Gelee - a finer confiture. version 2021.10.24
```

### General Help

```console
$ gelee
Usage: gelee [OPTIONS] COMMAND [ARGS]...

  Gelee - a finer confiture.

  Validate configuration files against their format and maybe schema.

Options:
  -V, --version  Display the gelee version and exit  [default: False]
  -h, --help     Show this message and exit.

Commands:
  cook     Cook the gelee from the files in the tree below path.
  version  Display the gelee version and exit
```

### Cook Help

```console
$ gelee cook --help
Usage: gelee cook [OPTIONS] UNIQUE_TREES...

  Cook the gelee from the files in the tree below path.

Arguments:
  UNIQUE_TREES...  [required]

Options:
  -a, --abort  Flag to abort execution on first fail (default is False)
               [default: False]

  -d, --debug  Flag to debug execution by adding more context info (default is
               False)  [default: False]

  -h, --help   Show this message and exit.
```


### Cook

```
$ gelee cook tests/fixtures
2021-10-23T18:47:18.979 INFO [gelee]: Starting validation visiting a forest with 1 tree
2021-10-23T18:47:18.994 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/toml/key_group_not_on_dedicated_line.toml with error: Key group not on a line by itself. (line 1 column 1 char 0)
2021-10-23T18:47:18.994 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/xml/empty.xml with error: ERROR: Empty XML file
2021-10-23T18:47:18.996 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/ini/duplicate_section.ini with error: While reading from PosixPath('tests/fixtures/invalid/ini/duplicate_section.ini') [line  3]: section 'section' already exists
2021-10-23T18:47:18.997 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/ini/missing_section_header.ini with error: File contains no section headers.file: PosixPath('tests/fixtures/invalid/ini/missing_section_header.ini'), line: 1'[section\n'
2021-10-23T18:47:18.998 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/json/invalid.json with error: Expecting property name enclosed in double quotes: line 2 column 1 (char 2)
2021-10-23T18:47:18.998 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/json/empty.geojson with error: Expecting value: line 1 column 1 (char 0)
2021-10-23T18:47:18.999 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/csv/empty.csv with error: ERROR: Empty CSV file
2021-10-23T18:47:19.000 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/yaml/unexpected-dash.yml with error: while parsing a block mapping  in "tests/fixtures/invalid/yaml/unexpected-dash.yml", line 1, column 1did not find expected key  in "tests/fixtures/invalid/yaml/unexpected-dash.yml", line 3, column 1
2021-10-23T18:47:19.001 ERROR [gelee]: Failed validation for path tests/fixtures/invalid/yaml/unexpected-dash.yaml with error: while parsing a block mapping  in "tests/fixtures/invalid/yaml/unexpected-dash.yaml", line 1, column 1did not find expected key  in "tests/fixtures/invalid/yaml/unexpected-dash.yaml", line 3, column 1
2021-10-23T18:47:19.001 INFO [gelee]: - Successfully validated 1 total CSV file.
2021-10-23T18:47:19.001 INFO [gelee]: - Successfully validated 1 total INI file.
2021-10-23T18:47:19.001 INFO [gelee]: - Successfully validated 1 total JSON file.
2021-10-23T18:47:19.001 INFO [gelee]: - Successfully validated 1 total TOML file.
2021-10-23T18:47:19.001 INFO [gelee]: - Successfully validated 1 total XML file.
2021-10-23T18:47:19.001 INFO [gelee]: - Successfully validated 1 total YAML file.
2021-10-23T18:47:19.001 INFO [gelee]: Finished validation of 6 configuration files with 9 failures visiting 33 paths (ignored 1 non-config file in 17 folders)
FAIL
```
