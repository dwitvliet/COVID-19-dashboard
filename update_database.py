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

# Create BigQuery table if it does not exists.
table_id = "covid-19-dashboard-304803.covid19_data.cases_and_vaccinations"
schema = [
    bigquery.SchemaField('country', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('date', 'DATE', mode='REQUIRED'),
    bigquery.SchemaField('cases', 'INTEGER'),
    bigquery.SchemaField('deaths', 'INTEGER'),
    bigquery.SchemaField('recovered', 'INTEGER'),
    bigquery.SchemaField('vaccination_doses', 'INTEGER'),
    bigquery.SchemaField('vaccination_people', 'INTEGER'),
    bigquery.SchemaField('vaccination_people_fully', 'INTEGER'),
]
table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table, exists_ok=True)

#