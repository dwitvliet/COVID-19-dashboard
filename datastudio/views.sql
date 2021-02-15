CREATE VIEW covid19_data.cases_global AS
SELECT
    `date`,
    SUM(cases_total) AS cases_total,
    SUM(cases_new) AS cases_new,
    CASE
        WHEN SUM(tests_total) = 0 THEN NULL
        ELSE SUM(deaths_total) / SUM(cases_total)
    END AS fatality_rate,
    CASE
        WHEN SUM(tests_total) = 0 THEN NULL
        ELSE SUM(cases_total) / SUM(tests_total)
    END AS cases_per_test_pct,
FROM `covid19_data.cases`
GROUP BY `date`
ORDER BY `date` ASC;