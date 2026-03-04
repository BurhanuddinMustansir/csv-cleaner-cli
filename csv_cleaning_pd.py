import pandas as pd
import phonenumbers
from email_validator import validate_email, EmailNotValidError 
import re
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="CSV cleaning Tool")
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--country", default="US")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--summary")
    parser.add_argument("--email-col", nargs="*")
    parser.add_argument("--phone-col", nargs="*")

    args = parser.parse_args()

    df = pd.read_csv(args.input_file)

    len_before_dup = len(df)
    df = df.drop_duplicates(subset=["First Name", "Last Name", "Company"])
    len_after_dup = len(df)

    #normalizing each phone columns
    phone_cols = args.phone_col
    if phone_cols is None:
        phone_cols = [col for col in df.columns if "phone" in col.lower() or "tel" in col.lower()]
    invalid_phones = 0
    for phone in phone_cols:
        df[phone] = df[phone].apply(lambda x: normalize_phone(x, args.country))
        invalid_phones += int(df[phone].isna().sum())


    #validating emails
    email_cols = args.email_col
    if email_cols is None:
        email_cols = [col for col in df.columns if "mail" in col.lower()]
    invalid_emails = 0
    for email in email_cols:
        df[email] = df[email].apply(lambda x: validate_emails(x, args.strict))
        invalid_emails += int(df[email].isna().sum())

    duplicates_removed = len_before_dup-len_after_dup


    summary = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "phone_cols": phone_cols,
        "email_cols": email_cols,
        "duplicates_removed": duplicates_removed,
        "invalid_emails": invalid_emails,
        "invalid_phones": invalid_phones
    }

    if args.summary:
        with open(args.summary, "w") as json_file:
            json.dump(summary, json_file, indent=4)

    df.to_csv(args.output_file, index=False)


def validate_emails(email, strict):
    if pd.isna(email):
        return None
    try:
        email_info = validate_email(email, check_deliverability=strict)
        email = email_info.normalized
        return email
    except EmailNotValidError:
        return None


def normalize_phone(phone, country):
    if pd.isna(phone):
        return None
    phone = re.split(r'(ext|x|extention)\w*\d+', str(phone), flags=re.IGNORECASE)[0]
    try:
        phone = phonenumbers.parse(phone, country)
        if not phonenumbers.is_possible_number(phone):
            return None
        return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
    except:
        return None
    
if __name__ == "__main__":
    main()