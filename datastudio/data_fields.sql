CASE
    WHEN metric_raw = 'cases_total' THEN 'Cases - total'
    WHEN metric_raw = 'cases_per_person' THEN 'Cases - total per person'
    WHEN metric_raw = 'cases_new' THEN 'Cases - new (weekly moving average)'
    WHEN metric_raw = 'new_cases_per_person' THEN 'Cases - new per person'

    WHEN metric_raw = 'deaths_total' THEN 'Deaths - total'
    WHEN metric_raw = 'deaths_per_person' THEN 'Deaths - total per person'
    WHEN metric_raw = 'deaths_new' THEN 'Deaths - new (weekly moving average)'
    WHEN metric_raw = 'new_deaths_per_person' THEN 'Deaths - new per person'

    WHEN metric_raw = 'tests_total' THEN 'Tests - total'
    WHEN metric_raw = 'tests_per_person' THEN 'Tests - total per person'
    WHEN metric_raw = 'tests_new' THEN 'Tests - new (weekly moving average)'
    WHEN metric_raw = 'new_tests_per_person' THEN 'Tests - new per person'

    WHEN metric_raw = 'deaths_per_case' THEN 'Fatality rate'
    WHEN metric_raw = 'cases_per_test' THEN 'Tests - proportion positive'

    ELSE 'Other'
END