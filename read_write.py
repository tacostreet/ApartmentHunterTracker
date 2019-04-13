import gspread
import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
import psycopg2 
import io

def df_import():
    '''Imports "Active Ads" sheets from the Houston Master Apartment google sheet. Returns a list of lists of lists (in other words, a list of 2D arrays which contain the contents of each sheet)'''
    
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-sync-test-53bcd85506ab.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by url and open each
    # Make sure you use the right name here.
    sh = client.open_by_url('https://docs.google.com/spreadsheets/d/1StYgk8i3NuC5DF5W7M2FQOU0DSzZtk3zQQttCCoEuu4/edit?ts=5c858e73#gid=1950841107')

    sheets = []
    for i in range(0, len(sh.worksheets())-1):
        sht = sh.get_worksheet(i)
        if sht.acell('A2').value == 'Contact #':
            sheets.append(sht.get_all_values())
    
    return sheets

def df_convertloc(data):
    '''Unpacks/translates data from the google sheets' information-dense first columns (column A). Returns a dataframe containing 2 new columns to append to the input dataframe: one for 'Building/Complex' and one for 'Building Address'.'''
    
    new_columns = pd.DataFrame(columns=['Building/Complex','Building Address'], index=range(1,len(data)))
    building = ''
    address = ''
    # List of standard entries in the dataframe's first columns. Includes common typos and potential typos: any un-included typo will result in complete malformation of the dataset.
    valid_types = ['1BR', '1 BR', '2BR', '2 BR', '3BR','3 BR', '4BR','4 BR', '5BR','5 BR', 'Studio']
    count = 0
    
    for index, row in data.iterrows():
        if row['Apartment Type'] not in valid_types:
            # Entries that represent a building's address all have commas in them (before denoting the city names)
            # Building titles/names do not, at least, not in any of these entries
            if ',' in str(row['Apartment Type']):
                address = row['Apartment Type']
            else:
                building = row['Apartment Type']
            if count <= 2:
                count += 1
            else:
                count = 0
        else:
            # If the value is a standard entry, than it is part of the previously declared set. Label it accordingly.
            new_columns['Building/Complex'][index] = building
            new_columns['Building Address'][index] = address    
    return new_columns

def df_export(data, table_name):
    '''Takes a single dataframe object and a desired SQL table name. Truncates the contents of the table on the attached Heroku database and replaces them with the contents of the dataframe.'''
    engine = create_engine(os.environ.get('DATABASE_URL', default))
    #Truncate/Clear the table if it exists
    df.head(0).to_sql(table_name, engine, if_exists='replace',index=False)
    
    #Fast data import using artifical cursor
    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, table_name, null="") # null values become ''
    conn.commit()
    
def df_test_export(data, table_name):
    '''As df_export, but attaches to the Heroku database via direct link rather than environment variable. WARNING: LINK ADDRESS WILL CHANGE OVER TIME; this function is meant for testing putposes only, or when not operating within the Heroku environment.'''
    engine = create_engine('postgres://xaaqozeqikgbkr:65cfd905b68bce05b836746c07886c03a74bfc4b919dee528ed9d8fa09c60d63@ec2-107-22-189-136.compute-1.amazonaws.com:5432/dlb0l5a96o19e')
    #Truncate/Clear the table if it exists
    data.head(0).to_sql(table_name, engine, if_exists='replace',index=False)
    
    #Fast data import using artifical cursor
    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    data.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, table_name, null="") # null values become ''
    conn.commit()

def df_main():
    '''Runs google sheets -> postgres data fetch-and-push, handling all necessary data cleaning, transforms, and concatanation. Exports the contents of all "Active Ads" sheets into a single SQL table.'''
    sheets = df_import()
    sheet_data = []

    for s in sheets:
        df = pd.DataFrame(s)
        # Set the first row of the spreadsheet as the column headers. 
        # Label unlabeled Aolumn A, and drop duplicate columns.
        df[0][0] = 'Apartment Type'
        df.columns = df.iloc[0]
        df = df.loc[:,~df.columns.duplicated()]
        
        # Drop whitespace rows and correct indicies
        df = df.drop([0,1,2,3,4])
        df = df.replace(['',' ','  '],np.NaN)   
        df = df.dropna(how='all')
        df.index = range(len(df))
        
        # Unpack information in Column A and further data cleaning
        df = df.join(df_convertloc(df))
        df = df.dropna(subset=['Building Address'])
        df.index = range(len(df))
        df.drop('#', axis=1, inplace=True)
        for i in df.columns:
            if i == '':
                df.drop(i, axis=1, inplace=True, errors='ignore')
        
        sheet_data.append(df)
        
    # Concatanate dataframes from each google sheet and export
    final_data = pd.concat(sheet_data, axis=0, ignore_index=True)
    
    # Insert 'id' column to play nice with Django
    final_data.insert(loc=0,column='id',value=list(range(1,len(final_data.index)+1)))
    
    df_export(final_data, 'houston_listings')
    #df_test_export(final_data, 'houston_listings')
    #return final_data

