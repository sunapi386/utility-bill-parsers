#!/usr/bin/env python3
"""
Parses PG&E utility PDF into a json.
Author: Jason Sun <sunapi386@gmail.com>
Date: 2019-03-28

Example:
$ python3 extract_pge.py 0000custbill20182006.pdf
{
    "account": "000000000-0",
    "days": "05/19/2018 - 06/19/2018 (32 billing days)",
    "due": "07/11/2018",
    "electricConsumed": "274.000000 kWh",
    "electricTotal": "$61.15",
    "file": "0000custbill20182006.pdf",
    "gasConsumed": "8.000000 Therms",
    "gasTotal": "$10.45"
}

"""

import pdftotext
import re
import json
import sys


class PGEPdfParser():
    """Parse PGE pdfs determined by hand"""

    def __init__(self, pdf_path):
        self.file = pdf_path
        self.pdf_str = PGEPdfParser.pdf2str(pdf_path)
        self.rxAccountNo = r"Account No: \d+-\d"
        self.rxDueDate = r"Due Date:\s+\d\d/\d\d/\d\d\d\d"
        self.rxDays = r"\d\d/\d\d/\d\d\d\d - \d\d/\d\d/\d\d\d\d \(\d+ billing days\)"
        self.rxElectricTotal = r"Total Electric Charges\s+\$\d+\.\d\d"
        self.rxElectricConsumed = r"Total Usage\s+\d+\.\d+\skWh"
        self.rxGasTotal = r"Total Gas Charges\s+\$\d+\.\d\d"
        self.rxGasConsumed = r"Gas Usage This Period\:\s+\d+\.\d+\s+Therms"
        self.rxTotalDue = r"Total Amount Due by \d+\/\d+\/\d+\s+\$\d+.\d\d"

    def pdf2str(docPath):
        with open(docPath, "rb") as f:
            pdf = pdftotext.PDF(f)
            return "\n\n".join(pdf)

    def rx(self, regex):
        matches = re.finditer(regex, self.pdf_str, re.MULTILINE)
        if not matches:
            return ""
        first_match = next(matches)
        matched_str = first_match.group()
        single_spaces = re.sub(' +', ' ', matched_str)
        return single_spaces

    def dict(self):
        acct = self.rx(self.rxAccountNo).split()[-1]
        date = self.rx(self.rxDueDate).split()[-1]
        days_summary = self.rx(self.rxDays)
        summary_split = days_summary.split()
        e_total = self.rx(self.rxElectricTotal).split()[-1]
        e_cons = " ".join(self.rx(self.rxElectricConsumed).split()[-2:])
        g_total = self.rx(self.rxGasTotal).split()[-1]
        g_cons = " ".join(self.rx(self.rxGasConsumed).split()[-2:])
        total = self.rx(self.rxTotalDue).split()[-1]
        return {
            "file": self.file,
            "account": acct,
            "due": date,
            "days_start": days_summary[0],
            "days_end": days_summary[2],
            "days_count": days_summary[3][1:],
            "electricTotal": e_total,
            "electricConsumed": e_cons,
            "gasTotal": g_total,
            "gasConsumed": g_cons,
            "total": total
        }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Specify the pdf name (e.g. 0000custbill20182012.pdf)")
        exit(-1)

    document = sys.argv[1]
    # document = '0000custbill20182012.pdf'

    pgeParser = PGEPdfParser(document)
    d = pgeParser.dict()
    print(json.dumps(d, sort_keys=True, indent=4, separators=(',', ': ')))
