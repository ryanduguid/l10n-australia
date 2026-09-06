# Copyright 2026 Ryan Duguid
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models

from ..tools.abn import abn_checksum_ok, compact_abn, format_abn


class L10nAuAbn(models.AbstractModel):
    _name = "l10n.au.abn"
    _description = "Australian Business Number helpers"

    @api.model
    def compact(self, value):
        return compact_abn(value)

    @api.model
    def format(self, value):
        return format_abn(value)

    @api.model
    def checksum_ok(self, value):
        return abn_checksum_ok(value)
