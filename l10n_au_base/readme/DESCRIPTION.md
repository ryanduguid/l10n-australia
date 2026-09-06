Australian ABN checksum/format helpers and the standard 1 July–30 June
income year.

Core Odoo already validates AU VAT through `python-stdnum`. This module
exposes the ABR published weighting so other l10n_au addons can format
and checksum ABNs without a network call, and it labels the standard
income year (not FBT year, not a substituted accounting period).

A passing checksum is not proof of ABR registration. PASS on the income
year helper is not lodgment or close approval.
