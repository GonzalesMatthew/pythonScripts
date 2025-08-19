import pandas as pd

# Input and output file names
input_file = 'accountExtract.csv'
output_file = 'duplicatesImportantFieldsEnhanced.csv'

# Columns needed for processing (required for sorting and duplicate detection)
processing_columns = ['LASTNAME', 'FIRSTNAME', 'PERSONEMAIL', 'PERSONBIRTHDATE', 'PERSONMAILINGSTREET', 'PERSONMAILINGCITY', 'PERSONMAILINGSTATE']

# Columns to include in the output file (replace with your 10-20 desired fields)
output_columns = ['LASTNAME', 'FIRSTNAME', 'PERSONEMAIL', 'PERSONBIRTHDATE', 'CREATEDBYID', 'CREATEDDATE', 'ID',
                  'SYSTEMMODSTAMP']  # Add your fields here

# Combine processing and output columns to read from the input file
read_columns = list(set(processing_columns + output_columns))  # Ensure no duplicates

# Read only the needed columns with string dtype to avoid DtypeWarning
df = pd.read_csv(input_file, encoding='windows-1252', usecols=read_columns, dtype=str)

# Sort the dataframe by LASTNAME, FIRSTNAME, PERSONEMAIL, PERSONBIRTHDATE
df = df.sort_values(by=processing_columns)

# Identify duplicates based on LASTNAME, FIRSTNAME and either PERSONEMAIL or PERSONBIRTHDATE
mask = (
    # Duplicates with same LASTNAME, FIRSTNAME, and non-empty PERSONEMAIL
    ((df.duplicated(subset=['LASTNAME', 'FIRSTNAME', 'PERSONEMAIL'], keep=False)) & (df['PERSONEMAIL'].notna() & (df['PERSONEMAIL'] != ''))) |
    # Duplicates with same LASTNAME, FIRSTNAME, and PERSONBIRTHDATE
    (df.duplicated(subset=['LASTNAME', 'FIRSTNAME', 'PERSONBIRTHDATE'], keep=False)) |
    # Duplicate with same LASTLANE, FIRSTNAME, PERSONMAILINGSTREET, PERSONMAILINGCITY, and PERSONMAILINGSTATE
    (df.duplicated(subset=['LASTNAME', 'FIRSTNAME', 'PERSONMAILINGSTREET', 'PERSONMAILINGCITY', 'PERSONMAILINGSTATE'], keep=False))
)

# Filter duplicates
duplicates = df[mask]

# Write duplicates to a new CSV file with only the specified output columns
if not duplicates.empty:
    # Ensure only available columns are written (in case some output_columns are missing)
    available_columns = [col for col in output_columns if col in duplicates.columns]
    duplicates.to_csv(output_file, columns=available_columns, index=False)

print(f"Script completed. Found {len(duplicates)} duplicate rows.")
