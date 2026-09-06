# Copyright 2026 Ryan Duguid
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from odoo.addons.l10n_au_base.tools.abn import (
    abn_checksum_ok,
    compact_abn,
    format_abn,
)


class TestAbn(TransactionCase):
    def test_ato_example_checksum(self):
        # ABR worked example: https://abr.business.gov.au/Help/AbnFormat
        self.assertTrue(abn_checksum_ok("51 824 753 556"))
        self.assertEqual(compact_abn("51 824 753 556"), "51824753556")
        self.assertEqual(format_abn("51824753556"), "51 824 753 556")

    def test_au_prefix_and_spaces(self):
        self.assertTrue(abn_checksum_ok("AU 51 824 753 556"))
        self.assertEqual(compact_abn("au51824753556"), "51824753556")

    def test_known_invalid(self):
        self.assertFalse(abn_checksum_ok("99 999 999 999"))
        self.assertFalse(abn_checksum_ok("51824753557"))
        self.assertFalse(abn_checksum_ok("123"))
        self.assertFalse(abn_checksum_ok("n/a"))

    def test_empty_is_not_valid(self):
        self.assertEqual(compact_abn(""), "")
        self.assertEqual(format_abn(None), "")
        self.assertFalse(abn_checksum_ok(""))
        self.assertFalse(abn_checksum_ok(None))

    def test_abstract_model(self):
        helper = self.env["l10n.au.abn"]
        self.assertTrue(helper.checksum_ok("51 824 753 556"))
        self.assertEqual(helper.format("51824753556"), "51 824 753 556")
        self.assertFalse(helper.checksum_ok("99 999 999 999"))
