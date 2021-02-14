import os
import zipfile
import urllib.request
from google.cloud import bigquery

if not os.path.exists('data'):
    os.mkdir('data')

data_path = 'data/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports'
vaccinations_path = 'data/vaccinations.csv'


#urllib.request.urlretrieve('https://github.com/owid/covid-19-data/raw/master/public/data/vaccinations/vaccinations.csv', vaccinations_path)
#urllib.request.urlretrieve('https://github.com/CSSEGISandData/COVID-19/archive/master.zip', 'data/covid.zip')
# with zipfile.ZipFile('data/covid.zip', 'r') as zip_ref:
#     zip_ref.extractall('data')

client = bigquery.Client()

table_id = "covid-19-dashboard-304803.covid19_data.your_table_name"

schema = [
    bigquery.SchemaField('full_name', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED'),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table, exists_ok=True)
