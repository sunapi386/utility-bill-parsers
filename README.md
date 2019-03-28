# utility-bill-parsers
Tools to convert utility bills in PDF to a json so it can be easily managed

Convert PG&E PDF statement into a JSON. (Account numbers removed.)

```bash
$ python3 pge_extract.py 0000custbill20182006.pdf
{
    "account": "00000000-0",
    "days": "05/19/2018 - 06/19/2018 (32 billing days)",
    "due": "07/11/2018",
    "electricConsumed": "274.000000 kWh",
    "electricTotal": "$61.15",
    "file": "0000custbill20182006.pdf",
    "gasConsumed": "8.000000 Therms",
    "gasTotal": "$10.45"
}
```
Xfinity PDF statements to JSON.
```bash
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
```
