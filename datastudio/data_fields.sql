CASE
    WHEN metric = 'cases_total' THEN 'Cases, total'
    WHEN metric = 'cases_per_person' THEN 'Cases, total per person'
    WHEN metric = 'cases_new' THEN 'Cases, new (weekly moving average)'
    WHEN metric = 'new_cases_per_person' THEN 'Cases, new per person'

    WHEN metric = 'deaths_total' THEN 'Deaths, total'
    WHEN metric = 'deaths_per_person' THEN 'Deaths, total per person'
    WHEN metric = 'deaths_new' THEN 'Deaths, new (weekly moving average)'
    WHEN metric = 'new_deaths_per_person' THEN 'Deaths, new per person'

    WHEN metric = 'tests_total' THEN 'Tests, total'
    WHEN metric = 'tests_per_person' THEN 'Tests, total per person'
    WHEN metric = 'tests_new' THEN 'Tests, new (weekly moving average)'
    WHEN metric = 'new_tests_per_person' THEN 'Tests, new per person'

    WHEN metric = 'deaths_per_case' THEN 'Fatality rate'
    WHEN metric = 'cases_per_test' THEN 'Tests, proportion positive'

    ELSE 'Other'
END