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

