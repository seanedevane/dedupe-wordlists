# How to use this script

This Python script (tested in Python 3.11, but should work on earlier versions of Python 3 at minimum) takes in text files, currently saved with the `.txt` extension, and deduplicates individual lines. To make the script non-destructive the output is saved to a new file specified in a directory.

## Command Info

```
usage: wordlist-dedup.py [-h] [-o OUTPUT_PATH] {dedupe,combine} input_path

Inputs a wordlist file, or directory of wordlist files (in .txt format) and
returns deduplicated copies at a specified output directory (defaults to
subdirectory of current working directory)

positional arguments:
  {dedupe,combine}      Mode toggle: "dedupe" to remove duplicates from
                        individual lists, "combine" to take all wordlists and
                        merge and deduplicate (writes to
                        output_path/combined_wordlist.txt)
  input_path            Path to file or directory

options:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output directory path [default: /output]
```

## Usage

Receive one or more wordlists and output deduplicated copies of each ***individual*** wordlist to a target directory

`python3 wordlist-dedupe.py dedupe /path/to/input_dir -o /path/to/output_dir`

Combine multiple wordlists into a deduplicated single wordlist. Current version writes this out to the filename `combined_wordlist.txt`

`python3 wordlist-dedupe.py combine /path/to/input_dir -o /path/to/output_dir`

WARNING: current implementation will overwrite any files with matching filenames in the target directory. Adding in logic to prevent this and allow it to be overwritten is on the shortlist of features to add.