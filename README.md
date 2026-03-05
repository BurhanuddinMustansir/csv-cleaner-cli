# CSV Cleaning CLI Tool

A command-line tool to:

- Normalize phone numbers (E.164 format)
- Validate email addresses
- Optional strict DNS email validation
- Auto-detect email and phone columns
- Remove duplicates
- Generate cleaning summary

## Usage
```
python csv_cleaning_pd.py input.csv output.csv

Optional arguments:

--strict                    Enable DNS email validation
--summary file.json         Output summary to JSON
--email-col  col1 col2      
--phone-col  col1 col2      
--country US                default US
```

## Example
```bash
python cleaner.py customers.csv cleaned.csv --strict --summary report.json --email-col Email --phone-col Phone1 Phone2
```
If --email-col or --phone-col are not provided, the script will attempt to auto-detect columns containing 'mail', 'phone', or 'tel'.\
Example dataset included, generated using Faker library
