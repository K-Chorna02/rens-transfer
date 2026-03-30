import pandas as pd
import os

#these functions clean the incoming data

def basic_clean_df(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    return df


def clean_organisations_df(df):
    df = basic_clean_df(df)

    if "Focus" in df.columns:
        df["Focus"] = df["Focus"].str.capitalize()

    if "Area of Operation" in df.columns:
        df["Area of Operation"] = df["Area of Operation"].str.capitalize()
        df["Area of Operation"] = df["Area of Operation"].str.strip()

    if "TtoR" in df.columns:
        df["TtoR"] = pd.to_numeric(df["TtoR"], errors="coerce")

    if "Variety" in df.columns:
        df["Variety"] = (
            df["Variety"]
            .astype("string")
            .str.strip()
            .str.upper()
            .replace({
                "1": "A",
                "2": "B",
                "3": "C"
            })
        )

    priority_cols = ["EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]
    for col in priority_cols:
        if col in df.columns:
            s = df[col].astype("string").str.strip().str.upper()
            df[col] = s.isin({"Y", "YES", "TRUE", "1", "T"})

    df.dropna(how='all', inplace=True)
    df.drop_duplicates(inplace=True)

    return df


def clean_activities_df(df):
    df = basic_clean_df(df)

    cols = df.columns.tolist()
    df[cols] = df[cols].replace(r'^\s*$', pd.NA, regex=True)
    df[cols] = df[cols].replace('nan', pd.NA)

    df.dropna(how='all', inplace=True)
    df.drop_duplicates(inplace=True)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], format='%d-%b-%y', errors='coerce')

    if "Hours" in df.columns:
        df["Hours"] = pd.to_numeric(df["Hours"], errors="coerce")

    return df


def clean_meetings_df(df):
    df = basic_clean_df(df)

    cols = df.columns.tolist()
    df[cols] = df[cols].replace(r'^\s*$', pd.NA, regex=True)
    df[cols] = df[cols].replace('nan', pd.NA)

    df.dropna(how='all', inplace=True)
    df.drop_duplicates(inplace=True)

    if "Date" in df.columns:
        from dateutil import parser

        def safe_standardize_date(x):
            if pd.isna(x):
                return None
            try:
                parsed = parser.parse(str(x), dayfirst=False)
                return parsed.strftime('%m-%d-%Y')
            except Exception:
                return str(x).strip()

        df["Date"] = df["Date"].apply(safe_standardize_date)
        df["Date"] = pd.to_datetime(df["Date"], format='%m-%d-%Y', errors='coerce')

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.title()

    return df


def clean_df(df, dataset_type):
    if dataset_type == 'organisations':
        return clean_organisations_df(df)
    if dataset_type == 'activities':
        return clean_activities_df(df)
    if dataset_type == 'meetings':
        return clean_meetings_df(df)

    return basic_clean_df(df)