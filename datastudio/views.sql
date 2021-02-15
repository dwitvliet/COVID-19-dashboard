CREATE VIEW `covid19_data.fatality_rate` AS
SELECT
    `date`,
    SUM(deaths_total) / SUM(cases_total) AS fatality_rate
FROM `covid19_data.cases`
GROUP BY `date`
ORDER BY `date` DESC;