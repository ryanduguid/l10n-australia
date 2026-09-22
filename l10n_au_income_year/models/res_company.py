# Copyright 2026 Ryan Duguid
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from ..tools.income_year import (
    income_year_bounds,
    income_year_label,
    is_standard_income_year_end,
)


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_au_standard_income_year = fields.Boolean(
        string="AU standard income year (30 June)",
        compute="_compute_l10n_au_standard_income_year",
        help="True when the company's fiscal country is Australia and the "
        "fiscal year ends 30 June. Substituted accounting periods exist; "
        "this flag is not lodgment advice.",
    )

    @api.depends(
        "fiscalyear_last_day",
        "fiscalyear_last_month",
        "account_fiscal_country_id",
        "country_id",
    )
    def _compute_l10n_au_standard_income_year(self):
        for company in self:
            country = company.account_fiscal_country_id or company.country_id
            company.l10n_au_standard_income_year = bool(
                country
                and country.code == "AU"
                and is_standard_income_year_end(
                    company.fiscalyear_last_month or 0,
                    company.fiscalyear_last_day or 0,
                )
            )

    def l10n_au_income_year(self, day=None):
        """Return start, end, and label for the standard AU income year.

        ``day`` defaults to today. The result is the 1 July–30 June year
        containing that date, even if this company uses a substituted
        accounting period.
        """
        self.ensure_one()
        current = fields.Date.context_today(self) if day is None else day
        start, end = income_year_bounds(current)
        return {
            "date_from": start,
            "date_to": end,
            "label": income_year_label(current),
        }
