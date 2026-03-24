import pandas as pd
import os

#these functions clean the incoming data

def clean_organisations(input_path):
    filename = os.path.join(input_path, 'Organisations.csv')

    df = pd.read_csv(
        filename,
        dtype=str,
        engine='python',
        on_bad_lines='warn',
    )

    df.columns = df.columns.str.strip()

    # Strip whitespace in all text columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Standardization
    if "Focus" in df.columns:
        df["Focus"] = df["Focus"].str.capitalize()

    if "Area of Operation" in df.columns:
        df["Area of Operation"] = df["Area of Operation"].str.capitalize()
        df["Area of Operation"] = df["Area of Operation"].str.strip()

    # TtoR as numeric
    if "TtoR" in df.columns:
        df["TtoR"] = pd.to_numeric(df["TtoR"], errors="coerce")

    # Variety normalization
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

    # Convert priority flags to booleans
    priority_cols = ["EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]
    for col in priority_cols:
        if col in df.columns:
            s = df[col].astype("string").str.strip().str.upper()
            df[col] = s.isin({"Y", "YES", "TRUE", "1", "T"})

    # Drop fully empty rows
    df.dropna(how='all', inplace=True)

    return df, 'Organisations_processed.csv'
def clean_activities(input_path):
    filename = os.path.join(input_path,'Activities.csv')
    df = pd.read_csv(filename)
    
    df.columns = df.columns.str.strip()

    # Remove leading/trailing spaces in string columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # --- Step 4: Split rows when RENS Yr and Year have comma-separated values ---
    new_rows = []
    
    for _, row in df.iterrows():
        # Split both columns by comma and strip spaces
        rens_list = [x.strip() for x in str(row['RENS Yr']).split(',')]
        year_list = [x.strip() for x in str(row['Year']).split(',')]
    
        # If both columns have same number of parts, zip them (match pairs)
        if len(rens_list) == len(year_list):
            for rens, year in zip(rens_list, year_list):
                new_row = row.copy()
                new_row['RENS Yr'] = rens
                new_row['Year'] = year
                new_rows.append(new_row)
        elif len(rens_list) == 1 and len(year_list) > 1:
            for year in year_list:
                new_row = row.copy()
                new_row['Year'] = year
                new_row['RENS Yr'] = rens_list[0]
                new_rows.append(new_row)
        else:
            # If lengths differ, just keep the original row
            new_rows.append(row)
    
    # Convert list back to DataFrame
    df = pd.DataFrame(new_rows)
    
    df['Category'] = df['Category'].str.split(',')
    df = df.explode('Category')
    
    # Clean up whitespace
    df['Category'] = df['Category'].str.strip()
    
    # List of columns to check (all columns in your case)
    cols = df.columns.tolist()
    
    # Replace empty strings, whitespace, or literal 'nan' with pd.NA
    df[cols] = df[cols].replace(r'^\s*$', pd.NA, regex=True)  # empty/whitespace
    df[cols] = df[cols].replace('nan', pd.NA)                # literal string 'nan'
    
    # Drop rows where all columns are NA
    df.dropna(how='all', inplace=True)
    #year[datetype]--check
    df['Year'] = pd.to_numeric(df['Year'])
    # --- Step 5: Remove duplicate rows (if any) ---
    df.drop_duplicates(inplace=True)
    
    
    df.info()
    
    df.duplicated().sum()
    
    
    for col in df.columns:
        if df[col].dtype == 'object':       # only text columns
            df[col] = df[col].astype(str).str.title()
            
    return df, 'Activities_processed.csv'
    
    
def clean_activities_updated(input_path):
    
    filename = os.path.join(input_path,'Activities2025.csv')
    df = pd.read_csv(filename)
    df.columns = df.columns.str.strip()
    
    # Remove leading/trailing spaces in string columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # List of columns to check (all columns in your case)
    cols = df.columns.tolist()
    
    # Replace empty strings, whitespace, or literal 'nan' with pd.NA
    df[cols] = df[cols].replace(r'^\s*$', pd.NA, regex=True)  # empty/whitespace
    df[cols] = df[cols].replace('nan', pd.NA)                # literal string 'nan'
    
    # Drop rows where all columns are NA
    df.dropna(how='all', inplace=True)
    # --- Step 5: Remove duplicate rows (if any) ---
    df.drop_duplicates(inplace=True)
    


    df.info()
    
    df.duplicated().sum()
    
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    
    return df, 'Activities_processed.csv'
    
def clean_meetings(input_path):
    filename = os.path.join(input_path,'Meetings.csv')

    # --- Step 1: Read the data ---
    df = pd.read_csv(filename)
    # --- Step 2: Clean spaces ---
    # Remove spaces in column names
    df.columns = df.columns.str.strip()
    
    # Remove leading/trailing spaces in string columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
 
    df['Category'] = df['Category'].str.split(',')
    df = df.explode('Category')
    
    # Clean up whitespace
    df['Category'] = df['Category'].str.strip()
    
    df.to_csv("Meetings_processed_1.csv",index=False)
    # print(df.head)
    
    # # List of columns to check (all columns in your case)
    cols = df.columns.tolist()
    
    # # Replace empty strings, whitespace, or literal 'nan' with pd.NA
    df[cols] = df[cols].replace(r'^\s*$', pd.NA, regex=True)  # empty/whitespace
    df[cols] = df[cols].replace('nan', pd.NA)                # literal string 'nan'
    
    # # Drop rows where all columns are NA
    df.dropna(how='all', inplace=True)
    df.to_csv("Meetings_processed_2.csv",index=False)
    df=df.drop(columns=["Type"])
    # df.to_csv("Meetings_processed.csv",index=False)
    # --- Step 5: Remove duplicate rows (if any) ---
    df.drop_duplicates(inplace=True)
    
    # --- Step 6: Reset index ---
    # df.reset_index(drop=True, inplace=True)
    
    df.to_csv("Meetings_processed_3.csv",index=False)
    # Convert Date column to datetime
    
    from dateutil import parser
    
    # --- Safe standardization function ---
    def safe_standardize_date(x):
        if pd.isna(x):
            return None
        try:
            parsed = parser.parse(str(x), dayfirst=False)  # interpret month first
            return parsed.strftime('%m-%d-%Y')             # standardize format
        except Exception:
            return str(x).strip()                          # keep as-is if parsing fails
    
    # --- Apply to DataFrame ---
    df['Date'] = df['Date'].apply(safe_standardize_date)
    
    # Optional: save standardized version before type conversion
    # df.to_csv("Meetings_standardized.csv", index=False)
    
    # --- Convert to datetime dtype ---
    df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y', errors='coerce')
    
    # --- Check result ---
    df.info()
    
    
    for col in df.columns:
         if df[col].dtype == 'object':       # only text columns
             df[col] = df[col].astype(str).str.title()
    
    # --- Done! ---
    return df, 'Meetings_processed.csv'
    

    