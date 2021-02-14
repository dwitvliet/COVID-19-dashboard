import os
import zipfile
import urllib.request

import pandas as pd
from google.cloud import bigquery

if not os.path.exists('data'):
    os.mkdir('data')

data_path = 'data/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports'

#urllib.request.urlretrieve('https://github.com/CSSEGISandData/COVID-19/archive/master.zip', 'data/covid.zip')
# with zipfile.ZipFile('data/covid.zip', 'r') as zip_ref:
#     zip_ref.extractall('data')

# Load data into DataFrame.
csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
dfs = []
for csv_file in csv_files:
    month, day, year = csv_file[:-4].split('-')

    df = pd.read_csv(os.path.join(data_path, csv_file)).rename({
        'Country_Region': 'country', 'Country/Region': 'country',
        'Confirmed': 'cases', 'Deaths': 'deaths', 'Recovered': 'recovered',
    }, axis=1)

    if len({'country', 'cases', 'deaths', 'recovered'}.intersection(df.columns)) != 4:
        print('Some columns are missing!')
        continue

    df = df.groupby('country')[['cases', 'deaths', 'recovered']].sum()
    df['date'] = f'{year}-{month}-{day}'
    dfs.append(df)

df = pd.concat(dfs)

# Create BigQuery table if it does not exists.
client = bigquery.Client()
table_id = "covid-19-dashboard-304803.covid19_data.cases_and_vaccinations"
schema = [
    bigquery.SchemaField('country', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('date', 'DATE', mode='REQUIRED'),
    bigquery.SchemaField('cases', 'INTEGER'),
    bigquery.SchemaField('deaths', 'INTEGER'),
    bigquery.SchemaField('recovered', 'INTEGER'),
#     bigquery.SchemaField('vaccination_doses', 'INTEGER'),
#     bigquery.SchemaField('vaccination_people', 'INTEGER'),
#     bigquery.SchemaField('vaccination_people_fully', 'INTEGER'),
]
table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table, exists_ok=True)

#