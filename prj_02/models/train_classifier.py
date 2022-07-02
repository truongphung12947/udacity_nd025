# import libraries
import re
import sys
import pandas as pd
import nltk
import pickle
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download(['punkt', 'wordnet', 'omw-1.4'])

def load_data(db_path):
    # load sqlite data to dataframe and split dataset
    # load data from database
    engine = create_engine('sqlite:///{0}'.format(db_path))
    df = pd.read_sql_table('DisasterResponseTable', engine)
    X = df.message
    # load features set
    y = df[df.columns[4:]]
    print('\tDATABASE: {0}'.format(db_path))
    return X, y

def tokenize(text):
    # url regex for matching an URL to clean URL in string, url has no use in classification disaster message and easy confuse with news or links
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    found_urls = re.findall(url_regex, text)
    for url in found_urls:
        text = text.replace(url, 'url')
    # tokenize words, normalize and remove empty spaces
    tokens = word_tokenize(text)
    # clean words
    lemmatizer = WordNetLemmatizer()
    processed_tokens = [lemmatizer.lemmatize(token).lower().strip() for token in tokens]
    return processed_tokens

def build_model():
    # build model using RandomForest
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
    ])
    # using optimized parameter after run some try to find best model but still keeping model file size small
    parameters = {
        'clf__estimator__n_estimators': [10],
        'clf__estimator__min_samples_split': [2]
    }
    model = GridSearchCV(pipeline, param_grid=parameters, n_jobs=4)
    return model

def evaluate_model(model, X_test, y_test):
    # run evaluation on our model
    y_pred = model.predict(X_test)
    i = 0
    for col in y_test:
        print(col)
        print(classification_report(y_test[col], y_pred[:, i]))
        i += 1
    print('\tACCURACY: {:.3f}'.format((y_pred == y_test.values).mean()))

def save_model(model, model_path):
    # save model to file for later use
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    print('\tMODEL: {0}'.format(model_path))

def main():
    if len(sys.argv) == 3:
        db_path, model_path = sys.argv[1:]
        print('Loading data...')
        X, y = load_data(db_path)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        print('Building model...')
        model = build_model()
        print('Traning model...')
        model.fit(X_train, y_train)
        print('Evaluating model...')
        evaluate_model(model, X_test, y_test)
        print('Saving mode...')
        save_model(model, model_path)
        print('Trained model saved!')
    else:
        print('Error! Lack of arguments. Please enter parameters as sample belows.\nEx: python train_classifier.py DisasterResponse.db classifier.pkl')

if __name__ == '__main__':
    main()