Call `env["l10n.au.abn"]` to compact, format (`NN NNN NNN NNN`), or
checksum an ABN. The algorithm is the ABR weighting (subtract 1 from
the first digit, weights 10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, total
divisible by 89).

On `res.company`, `l10n_au_income_year(date)` returns `date_from`,
`date_to`, and `label` (`2026-27`) for the standard Australian income
year containing that date. `l10n_au_standard_income_year` is True when
the fiscal country is Australia and the fiscal year ends 30 June.

Do not use this module to lodge BAS, STP, or an income-tax return.
