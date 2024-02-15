#!/usr/bin/python3
# Author: Sean Edevane
# Wordlist (or general line) deduplication script
# Takes in one or more wordlists and returns a new copy of the list with duplicates removed
# Also supports combining multiple wordlists into one merged wordlist, also deduped.
from pathlib import Path
import re

def dedupe_individual_wordlists(input_path: Path, output_path: Path) -> None:
    '''Receives a wordlist files, parses each individually, and outputs deduplicated versions to a copy in the output_path directory'''
    if input_path.is_dir():
        # create a file list
        files = input_path.glob('*.txt')
        for wordlist in files:
            # get filename only
            filename = wordlist.name
            print(f'Processing {filename}\n')
            deduped_set = process_wordlists(wordlist)
            # write out with newlines re-added
            print(f'Writing deduped {filename} to {output_path / filename}\n')
            with open(output_path / filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(deduped_set))
            
    elif input_path.is_file():
        file = input_path
        filename = file.name
        print(f'Processing {filename}\n')
        deduped_set = process_wordlists(file)
        print(f'Writing deduped {filename} to {output_path / filename}\n')

        with open(output_path / filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(deduped_set))
    else:
        raise Exception(f'The input_path provided is not a file or directory, exiting.')

def process_wordlists(file_or_dir_path: Path) -> set:
    '''Takes either a single file path, or directory and parses through to add into a single set.
    Function is split out here to provide separation for either combining or only deduping single wordlists.

    Returns: set of strings
    '''
    deduped_list = set()
    # Combining wordlists mode
    if file_or_dir_path.is_dir():
        files = input_path.glob('*.txt')
        for wordlist in files:
            with open(wordlist, 'rb') as file:
                for line in file:
                    # avoiding encoding issues with binary read, return to string
                    line_str = str(line)
                    line_str = re.sub(r"^b'", '', line_str)
                    line_str = re.sub(r"\\n'", '', line_str)
                    # clear any preceding whitespace and holdover line numbers
                    line_str = line_str.strip()
                    line_str = re.sub(r'^[0-9] ', '', line_str)
                    deduped_list.add(line_str)
    # Single wordlist mode
    elif file_or_dir_path.is_file():
        with open(file_or_dir_path, 'rb') as file:
            for line in file:
                line_str = str(line)
                line_str = re.sub(r"^b'", '', line_str)
                line_str = re.sub(r"\\n'", '', line_str)
                # clear any preceding whitespace and holdover line numbers
                line_str = line_str.strip()
                line_str = re.sub(r'^[0-9] ', '', line_str)
                deduped_list.add(line_str)
    return deduped_list

def combine_wordlists(input_path: Path, output_path: Path) -> None:
    '''Receives multiple wordlists and combines into a deduplicated single list in the output directory.'''
    if input_path.is_dir():
        # create file list
        print(f'Combining and deduplicating lists from {input_path}\n')
        # All items added to a single list
        deduped_combined_list = process_wordlists(input_path)
        print(f'Writing combined wordlist out to {output_path / "combined_wordlist.txt"}\n')
        with open(output_path / 'combined_wordlist.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(deduped_combined_list))
    else:
        raise Exception(f'Input_path value was not a directory with text files. Exiting.')



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=
    '''
    Inputs a wordlist file, or directory of wordlist files (in .txt format) and 
    returns deduplicated copies at a specified output directory (defaults to subdirectory of current working directory)
    '''
    )
    parser.add_argument('mode', choices=['dedupe', 'combine'], help='Mode toggle: "dedupe" to remove duplicates from individual lists, "combine" to take all wordlists and merge and deduplicate (writes to output_path/combined_wordlist.txt)')
    parser.add_argument('input_path', help='Path to file or directory')
    parser.add_argument('-o', '--output_path', help='Output directory path [default: /output]')

    args = parser.parse_args()

    input_path = Path(args.input_path)

    if args.output_path:
        output_path = Path(args.output_path)
    else: 
        cwd = Path.cwd()
        output_path = cwd / 'output'


    # create subdirectory
    if not output_path.exists():
        print(f'Creating output directory {output_path}.\n')
        output_path.mkdir()
    else:
        print(f'Output directory, {output_path} already exists.\n')

    # call the correct function
    if args.mode == 'dedupe':
        print(f'Deduplicate called for {input_path}\n')
        dedupe_individual_wordlists(input_path, output_path)
    elif args.mode == 'combine':
        print(f'Combine called for {input_path}\n')
        combine_wordlists(input_path, output_path)
