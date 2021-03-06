import time
import datetime
import itertools
import requests
import numpy as np
import pandas as pd
from google.cloud import bigquery

from config import rapid_api_key


def main():

    # Get a list of countries to fetch for.
    headers = {
        'x-rapidapi-key': rapid_api_key, 'x-rapidapi-host': 'covid-193.p.rapidapi.com'
    }
    countries = requests.request(
        'GET', 'https://covid-193.p.rapidapi.com/countries', headers=headers
    ).json()['response']

    # Init dataframe to store the data.
    dates = pd.date_range('2020-03-21', datetime.datetime.now() - datetime.timedelta(1))
    df = pd.DataFrame(
        index=pd.MultiIndex.from_tuples(itertools.product(countries, dates.strftime('%Y-%m-%d')), names=['country', 'date']),
        columns=[
            'population', 'cases_new', 'cases_active', 'cases_recovered',
            'cases_critical', 'cases_total', 'deaths_new', 'deaths_total',
            'tests_total'
        ],
    )

    # Fetch cases, deaths, and tests for each country.
    for country in countries:
        print(country)
        records = requests.request(
            'GET', 'https://covid-193.p.rapidapi.com/history', headers=headers, params={'country': country}
        ).json()['response']
        for record in sorted(records, key=lambda x: x['cases']['total']):  # write largest number last in cases where multiple records exist per day.
            key = (record['country'], record['day'])
            if key not in df.index:
                continue
            df.loc[key, 'population'] = record['population'] or np.nan
            df.loc[key, 'cases_total'] = int(record['cases']['total'] or '0')
            df.loc[key, 'cases_new'] = int((record['cases']['new'] or '+0')[1:])
            df.loc[key, 'cases_active'] = int(record['cases']['active'] or '0')
            df.loc[key, 'cases_recovered'] = int(record['cases']['recovered'] or '0')
            df.loc[key, 'cases_critical'] = int(record['cases']['critical'] or '0')
            df.loc[key, 'deaths_total'] = int(record['deaths']['total'] or '0')
            df.loc[key, 'deaths_new'] = int((record['deaths']['new'] or '+0')[1:])
            df.loc[key, 'tests_total'] = int(record['tests']['total'] or '0')

        time.sleep(1)  # max 60 requests per minute

    # Fill missing values.
    df = df.reset_index().pivot(index='date', columns='country')
    df['population'] = df['population'].fillna(method='ffill').fillna(method='bfill')
    for column in ['cases_total', 'cases_recovered', 'deaths_total', 'tests_total']:
        df[column] = df[column].fillna(method='ffill').fillna(0)
    for column in ['cases_active', 'cases_critical']:
        df[column] = df[column].fillna(method='ffill', limit=5).fillna(0)
    for column in ['cases_new', 'deaths_new']:
        df[column] = df[column].fillna(0)

    # Fix incorrect values.
    df.loc[['2021-01-12', '2021-01-13'], ('tests_total', 'Bahrain')] /= 10

    # Calculate new tests.
    tests_new = df['tests_total'] - df['tests_total'].shift(fill_value=0)
    tests_new.columns = pd.MultiIndex.from_product([['tests_new'], tests_new.columns])
    df = df.join(tests_new)

    # Smooth new cases, deaths, and tests.
    for column in ['cases_new', 'deaths_new', 'tests_new']:
        df[column] = df[column].rolling(7, min_periods=1).mean()

    # Remove non-countries and abbreviations.
    df = df.unstack().unstack(0).reset_index()
    df = df.loc[~df['country'].isin([
        'Diamond-Princess', 'Diamond-Princess-', 'MS-Zaandam', 'MS-Zaandam-',
        'Cura&ccedil;ao', 'R&eacute;union'
    ])]
    df['country'] = df['country'].replace({
        'USA': 'United States', 'UK': 'United Kingdom', 'CAR': 'Central African Republic',
        'UAE': 'United Arab Emirates', 'S-Korea': 'South Korea',
        'Congo': 'Republic of the Congo',  'DRC': 'Democratic Republic of the Congo',
    })

    # Add missing populations.
    df.loc[df['country'] == 'Guam', 'population'] = 170179
    df.loc[df['country'] == 'Puerto-Rico', 'population'] = 2828255
    df.loc[df['country'] == 'Tanzania', 'population'] = 61498437
    df.loc[df['country'] == 'US-Virgin-Islands', 'population'] = 104363

    # Convert dataframe values to integers.
    integer_colums = [
        'population', 'cases_new', 'cases_active', 'cases_recovered',
        'cases_critical', 'cases_total', 'deaths_new', 'deaths_total',
        'tests_total', 'tests_new'
    ]
    df[integer_colums] = df[integer_colums].astype(int)

    # Calculate metrics.
    df['cases_per_person'] = df['cases_total'] / df['population']
    df['deaths_per_person'] = df['deaths_total'] / df['population']
    df['tests_per_person'] = df['tests_total'] / df['population']
    df['new_cases_per_mil'] = df['cases_new'] / df['population'] * 1000000
    df['new_deaths_per_mil'] = df['deaths_new'] / df['population'] * 1000000
    df['new_tests_per_mil'] = df['tests_new'] / df['population'] * 1000000
    df['deaths_per_case_pct'] = (df['deaths_total'] / df['cases_total']).replace(np.inf, 0) * 100
    df['cases_per_test_pct'] = (df['cases_total'] / df['tests_total']).replace(np.inf, 0) * 100

    df = df.drop(['cases_recovered', 'cases_active'], axis=1)

    # Create BigQuery table if it does not exists.
    client = bigquery.Client(project='covid-19-dashboard-304803')
    table_id = 'covid-19-dashboard-304803.covid19_data.cases'
    schema = [
        bigquery.SchemaField('country', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('date', 'DATE', mode='REQUIRED'),
        bigquery.SchemaField('population', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('cases_total', 'INTEGER'),
        bigquery.SchemaField('cases_new', 'INTEGER'),
        bigquery.SchemaField('cases_critical', 'INTEGER'),
        bigquery.SchemaField('deaths_total', 'INTEGER'),
        bigquery.SchemaField('deaths_new', 'INTEGER'),
        bigquery.SchemaField('tests_total', 'INTEGER'),
        bigquery.SchemaField('tests_new', 'INTEGER'),
        bigquery.SchemaField('cases_per_person', 'FLOAT'),
        bigquery.SchemaField('deaths_per_person', 'FLOAT'),
        bigquery.SchemaField('tests_per_person', 'FLOAT'),
        bigquery.SchemaField('new_cases_per_mil', 'FLOAT'),
        bigquery.SchemaField('new_deaths_per_mil', 'FLOAT'),
        bigquery.SchemaField('new_tests_per_mil', 'FLOAT'),
        bigquery.SchemaField('deaths_per_case_pct', 'FLOAT'),
        bigquery.SchemaField('cases_per_test_pct', 'FLOAT'),
    ]
    client.delete_table(table_id, not_found_ok=True)
    table = bigquery.Table(table_id, schema=schema)
    table.expires = None
    table = client.create_table(table)

    # Insert data into table.
    client.insert_rows_from_dataframe(table, df)


if __name__ == '__main__':
    main()
