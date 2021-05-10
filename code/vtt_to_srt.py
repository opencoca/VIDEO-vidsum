#!/usr/bin/python
# OpenCo Alexander Somma
# Jansen A. Simanullang / Jeison Cardoso

import os
import re
import sys
import hashlib
from stat import *

def convert_content(file_contents):
    """Convert convert of vtt file to str format

       Keyword arguments:
       file_contents
       """
    replacement = re.sub(r"(\d\d:\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n", r"\1,\2 --> \3,\4\n", file_contents)
    replacement = re.sub(r"(\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n", r"\1,\2 --> \3,\4\n", replacement)
    replacement = re.sub(r"(\d\d).(\d\d\d) --> (\d\d).(\d\d\d)(?:[ \-\w]+:[\w\%\d:]+)*\n", r"\1,\2 --> \3,\4\n", replacement)
    replacement = re.sub(r"WEBVTT\n", "", replacement)
    replacement = re.sub(r"Kind:[ \-\w]+\n", "", replacement)
    replacement = re.sub(r"Language:[ \-\w]+\n", "", replacement)
    replacement = re.sub(r"<c[.\w\d]*>", "", replacement)
    replacement = re.sub(r"</c>", "", replacement)
    replacement = re.sub(r"<\d\d:\d\d:\d\d.\d\d\d>", "", replacement)
    replacement = re.sub(r"::[\-\w]+\([\-.\w\d]+\)[ ]*{[.,:;\(\) \-\w\d]+\n }\n", "", replacement)
    replacement = re.sub(r"Style:\n##\n", "", replacement)
    # remove spaces
    lines = replacement.splitlines()
    nospaces = [line for line in lines if not  line.isspace()]
    completed_lines_hash = set()
    completed_lines = list()
    for line in nospaces:
        #hash the line
        hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
        if hashValue not in completed_lines_hash:
            completed_lines_hash.add(hashValue)
            completed_lines.append(line)

    lines = srt_segment_reduce(completed_lines)
    lines = srt_segment_number(lines)
    return "\n".join(lines)


def srt_segment_reduce(lines):
    """ Reduce the number srt segments

    Args:
        lines: an aray of Srt segments

    Returns:
        str: cleaned str
    """

    i = 0
    while i < len(lines):
        if i+1 < len(lines):
            if lines[i].startswith("00:0") and lines[i+1].startswith("00:0"):
                lines[i] = lines[i].split("-->")[0] + " --> " + lines[i+1].split("-->")[-1]
                lines.pop(i+1)

                i -= 1
        i += 1
    #import pdb; pdb.set_trace()
    return lines

def srt_segment_number(lines):
    """
    Number segments for use as an SRT file

    Ars:
        lines: a list of lines

    Returns:
        srt: a list of numbered segments
    """

    i = 0
    seg = 1
    while i < len(lines):
        if lines[i].startswith("00:0"):
            lines.insert(i, str(seg))
            seg += 1
            i +=2
        else:
            i +=1

    return lines

def file_create(str_name_file, str_data):
    """Create a file with some data

       Keyword arguments:
       str_name_file -- filename pat
       str_data -- dat to write
       """
    # --------------------------------
    # file_create(str_name_file, str_data)
    # create a text file
    try:
        f = open(str_name_file, "w", encoding='utf-8')
        f.writelines(str(str_data))
        f.close()
    except IOError:
        str_name_file = str_name_file.split(os.sep)[-1]
        f = open(str_name_file, "w")
        f.writelines(str(str_data))
        f.close()
    print("file created: " + str_name_file + "\n")


def read_text_file(str_name_file):
    """Read a file text

       Keyword arguments:
       str_name_file -- filename pat
       """
    f = open(str_name_file, mode="r", encoding='utf-8')
    print("file being read: " + str_name_file + "\n")
    return f.read()


def vtt_to_srt(str_name_file):
    """Convert vtt file to a srt file

       Keyword arguments:
       str_name_file -- filename path
       """
    file_contents: str = read_text_file(str_name_file)
    str_data: str = ""
    str_data = convert_content(file_contents)
    str_name_file: str = str_name_file.replace(".vtt", ".srt")
    #print(str_name_file)
    file_create(str_name_file, str_data)


def walk_tree(top_most_path, callback):
    """Recursively descend the directory tree rooted at top_most_path,
       calling the callback function for each regular file

       Keyword arguments:
       top_most_path -- parent directory
       callback -- function to call
       """
    for f in os.listdir(top_most_path):
        pathname = os.path.join(top_most_path, f)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It"s a directory, recurse into it
            walk_tree(pathname, callback)
        elif S_ISREG(mode):
            # It"s a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print("Skipping %s" % pathname)


def walk_dir(top_most_path, callback):
    """Walk a directory

       Keyword arguments:
       top_most_path -- parent directory
       callback -- function to call
       """
    for f in os.listdir(top_most_path):
        pathname = os.path.join(top_most_path, f)
        if not os.path.isdir(pathname):
            # It"s a file, call the callback function
            callback(pathname)


def convert_vtt_to_str(f):
    """Convert vtt fuke to string

       Keyword arguments:
       f -- file to convert
       """
    if ".vtt" in f:
        vtt_to_srt(f)


def vtts_to_srt(directory, rec = False):
    """Walk down directory seaching for vtt files

       Keyword arguments:
       directory -- path to search
       rec -- enable recursive
       """
    top_most_path = directory
    if rec:
        walk_tree(top_most_path, convert_vtt_to_str)
    else:
        walk_dir(top_most_path, convert_vtt_to_str)


def print_usage():
    """Show a info message about the usage"""
    print("\nUsage:\tvtt_to_srt pathname [-r]\n")
    print("\tpathname\t- a file or directory with files to be converted")
    print("\t-r\t\t- walk path recursively\n")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--help" or not os.path.exists(sys.argv[1]):
        print_usage()
        exit()
    path = sys.argv[1]
    rec = True if len(sys.argv) > 2 and sys.argv[2] == "-r" else False
    if os.path.isdir(path):
        vtts_to_srt(path, rec)
    else:
        vtt_to_srt(path)

if __name__ == "__main__":
    main()

