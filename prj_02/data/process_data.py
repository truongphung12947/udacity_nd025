import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(file_path, name):
    # load csv file and return pandas object
    data = pd.read_csv(file_path)
    print('\t{0}: {1}'.format(name, file_path))
    return data

def merge_data(message_df, categories_df):
    # merge 2 dataset by id
    df = message_df.merge(categories_df, left_on='id', right_on='id', how='inner')
    return df

def convert_categories(df):
    # convert each categories become seperate columns
    categories = df['categories'].str.split(';', expand=True)
    row = categories[0:1]
    category_colnames = row.apply(lambda x: x.str[:-2]).values.tolist()
    categories.columns = category_colnames
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
        # convert column from string to numeric
        categories[column] = pd.to_numeric(categories[column])
    df.drop(['categories'], axis=1, inplace = True)
    df = pd.concat([df, categories], axis=1)
    return df

def save_to_db(df, db_path):
    # save to sqlite
    print('\tDATABASE: {0}'.format(db_path))
    engine = create_engine('sqlite:///{0}'.format(db_path))
    df.to_sql('DisasterResponseTable', engine, if_exists = 'replace', index=False)

def drop_duplicates(df):
    df = df.drop_duplicates()
    return df

def main():
    if len(sys.argv) == 4:
        messages_csv_path, categories_csv_path, db_path = sys.argv[1:]
        print('Loading data...')
        message_df = load_data(messages_csv_path, 'MESSAGES')
        categories_df = load_data(categories_csv_path, 'CATEGORIES')
        df = merge_data(message_df, categories_df)
        print('Cleaning data...')
        df = convert_categories(df)
        df = drop_duplicates(df)
        print('Saving data...')
        save_to_db(df, db_path)
        print('Cleaned data saved to database!')
    else:
        print('Error! Lack of arguments. Please enter parameters as sample belows.\nEx: python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db')

if __name__ == '__main__':
    main()