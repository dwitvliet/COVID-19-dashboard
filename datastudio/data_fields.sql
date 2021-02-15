CASE
    WHEN metric = 'cases_total' THEN 'Total cases'
    WHEN metric = 'cases_per_person' THEN 'Total cases per person'
    WHEN metric = 'cases_new' THEN 'New cases (weekly moving average)'
    WHEN metric = 'new_cases_per_person' THEN 'New cases per person'

    WHEN metric = 'deaths_total' THEN 'Total deaths'
    WHEN metric = 'deaths_per_person' THEN 'Total deaths per person'
    WHEN metric = 'deaths_new' THEN 'New deaths (weekly moving average)'
    WHEN metric = 'new_deaths_per_person' THEN 'New deaths per person'

    WHEN metric = 'tests_total' THEN 'Total tests'
    WHEN metric = 'tests_per_person' THEN 'Total tests per person'
    WHEN metric = 'tests_new' THEN 'New tests (weekly moving average)'
    WHEN metric = 'new_tests_per_person' THEN 'New tests per person'

    WHEN metric = 'deaths_per_case' THEN 'Fatality rate'
    WHEN metric = 'cases_per_test' THEN 'Proportion positive tests'

    ELSE 'Other'
END