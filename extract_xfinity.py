#!/usr/bin/env python3
"""
Parses Xfinity statement PDF into a json.
Author: Jason Sun <sunapi386@gmail.com>
Date: 2019-03-28

Example:
$ python3 extract_xfinity.py xfinity-201903.pdf
{
    "account": "0000 00 000 0000000",
    "days_count": "30",
    "days_end": "Apr 13, 2019",
    "days_start": "Mar 14, 2019",
    "due": "Mar 09, 2019",
    "file": "xfinity-201903.pdf",
    "total": "$89.99"
}

"""

import pdftotext
import re
import json
import sys
from dateutil import parser

class XfinityPdfParser():
    """Parse Xfinity pdfs determined by hand"""

    def __init__(self, pdf_path):
        self.file = pdf_path
        self.pdf_str = XfinityPdfParser.pdf2str(pdf_path)
        self.rxAccountNo = r"Account number\s+\d\d\d\d \d\d \d\d\d \d\d\d\d\d\d\d"
        self.rxDays = r"... \d+, \d\d\d\d\s+... \d+, \d\d\d\d to ... \d+, \d\d\d\d"
        self.rxTotalDue = r"Amount due\s+\$\d+\.\d\d"

    def pdf2str(docPath):
        with open(docPath, "rb") as f:
            pdf = pdftotext.PDF(f)
            return "\n\n".join(pdf)

    def rx(self, regex):
        matches = re.finditer(regex, self.pdf_str, re.MULTILINE)
        try:
            first_match = next(matches)
            matched_str = first_match.group()
            single_spaces = re.sub(' +', ' ', matched_str)
            return single_spaces
        except StopIteration:
            return "NOT FOUND: " + regex

    def dict(self):
        acct = " ".join(self.rx(self.rxAccountNo).split()[-4:])
        total = self.rx(self.rxTotalDue).split()[-1]
        days3 = self.rx(self.rxDays)
        days_split = days3.split()
        day_billed = " ".join(days_split[0:3])
        day_end = " ".join(days_split[7:])
        day_start = " ".join(days_split[3:6])
        days_count = str((parser.parse(day_end) - parser.parse(day_start)).days)
        return {
            "file": self.file,
            "account": acct,
            "due": day_billed,
            "days_start": day_start,
            "days_end": day_end,
            "days_count": days_count,
            "total": total
        }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Specify the pdf name (e.g. xfinity-201903.pdf)")
        exit(-1)

    document = sys.argv[1]

    pgeParser = XfinityPdfParser(document)
    d = pgeParser.dict()
    print(json.dumps(d, sort_keys=True, indent=4, separators=(',', ': ')))
