# Copyright 2026 Ryan Duguid
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, datetime

from odoo.tests.common import TransactionCase

from odoo.addons.l10n_au_income_year.tools.income_year import (
    income_year_bounds,
    income_year_label,
)


class TestIncomeYear(TransactionCase):
    def test_30_june_is_end_of_prior_label(self):
        start, end = income_year_bounds(date(2026, 6, 30))
        self.assertEqual(start, date(2025, 7, 1))
        self.assertEqual(end, date(2026, 6, 30))
        self.assertEqual(income_year_label(date(2026, 6, 30)), "2025-26")

    def test_1_july_opens_next_year(self):
        start, end = income_year_bounds(date(2026, 7, 1))
        self.assertEqual(start, date(2026, 7, 1))
        self.assertEqual(end, date(2027, 6, 30))
        self.assertEqual(income_year_label(date(2026, 7, 1)), "2026-27")

    def test_calendar_year_end_sits_in_current_income_year(self):
        self.assertEqual(income_year_label(date(2026, 12, 31)), "2026-27")
        self.assertEqual(income_year_bounds(date(2026, 12, 31))[1], date(2027, 6, 30))

    def test_company_flag_and_helper(self):
        au = self.env.ref("base.au")
        company = self.env.company
        company.country_id = au
        company.account_fiscal_country_id = au
        company.write({"fiscalyear_last_month": "6", "fiscalyear_last_day": 30})
        self.assertTrue(company.l10n_au_standard_income_year)
        pack = company.l10n_au_income_year(date(2026, 8, 31))
        self.assertEqual(pack["label"], "2026-27")
        self.assertEqual(pack["date_from"], date(2026, 7, 1))
        self.assertEqual(pack["date_to"], date(2027, 6, 30))

        company.write({"fiscalyear_last_month": "12", "fiscalyear_last_day": 31})
        self.assertFalse(company.l10n_au_standard_income_year)

    def test_tool_rejects_datetime(self):
        with self.assertRaises(TypeError):
            income_year_label(datetime(2026, 6, 30, 15, 30))

    def test_company_helper_reads_datetime_in_user_timezone(self):
        company = self.env.company
        # 30 June 15:30 UTC is 1 July 01:30 in Sydney.
        moment = datetime(2026, 6, 30, 15, 30)
        sydney = company.with_context(tz="Australia/Sydney")
        pack = sydney.l10n_au_income_year(moment)
        self.assertEqual(pack["label"], "2026-27")
        self.assertEqual(pack["date_from"], date(2026, 7, 1))
        self.assertEqual(pack["date_to"], date(2027, 6, 30))
        # 30 June 13:59 UTC is still 30 June 23:59 in Sydney.
        pack = sydney.l10n_au_income_year(datetime(2026, 6, 30, 13, 59))
        self.assertEqual(pack["label"], "2025-26")
        utc = company.with_context(tz="UTC")
        self.assertEqual(utc.l10n_au_income_year(moment)["label"], "2025-26")
