On `res.company`, `l10n_au_income_year(date)` returns `date_from`,
`date_to` and `label` (`2026-27`) for the standard Australian income
year containing that date. It returns the standard year even when the
company is on a substituted accounting period.

`l10n_au_standard_income_year` is True when the company's fiscal
country is Australia and its fiscal year ends 30 June, which is what
`l10n_au` configures for an Australian company.

Do not use this module to lodge BAS, STP or an income-tax return.
