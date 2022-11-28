# Command Line API

## `gelee`

Gelee - a finer confiture.

Validate configuration files against their format and maybe schema.

**Usage**:

```console
❯ gelee [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-V, --version`: Display the gelee version and exit  [default: False]
* `-h, --help`: Show this message and exit.

**Commands**:

* `cook`: Cook the gelee from the files in the tree...
* `version`: Display the gelee version and exit

### `gelee cook`

Cook the gelee from the files in the tree below path.

**Usage**:

```console
❯ gelee cook [OPTIONS] UNIQUE_TREES...
```

**Arguments**:

* `UNIQUE_TREES...`: [required]

**Options**:

* `-a, --abort`: Flag to abort execution on first fail (default is False)  [default: False]
* `-d, --debug`: Flag to debug execution by adding more context info (default is False)  [default: False]
* `-h, --help`: Show this message and exit.

### `gelee version`

Display the gelee version and exit

**Usage**:

```console
❯ gelee version [OPTIONS]
```

**Options**:

* `-h, --help`: Show this message and exit.

