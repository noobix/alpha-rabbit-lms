# Author: Kelvin Kabute
# Last-updated: 2026-10-04

# Author: Kelvin Kabute
# Last-updated: 2026-10-04

"""Tests for vendor corporate information validation.

Vendors are corporate entities (businesses, publishers, distributors),
not natural persons. Ghana Card ID is a personal identifier and is NOT
collected for vendors. Instead, corporate identifiers are used:
- Business registration (Ghana Enterprises Agency): EA-XXXXXX
- Tax ID (Ghana Revenue Authority): TIN-XXXXXXXXX
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Validation helpers (mirror the logic in main/security.ts / db:save-vendor)
# ---------------------------------------------------------------------------

BUSINESS_REGISTRATION_PATTERN = re.compile(r"^EA-\d{6}$")
TAX_ID_PATTERN = re.compile(r"^TIN-\d{9}$")
GHANA_CARD_PATTERN = re.compile(r"^[A-Z]{3}-\d{9}-\d$")


def validate_business_registration(reg: str) -> bool:
    """Return True when reg matches Ghana Enterprises Agency format EA-XXXXXX."""
    if not reg or not isinstance(reg, str):
        return False
    return bool(BUSINESS_REGISTRATION_PATTERN.match(reg))


def validate_tax_id(tin: str) -> bool:
    """Return True when TIN matches Ghana Revenue Authority format TIN-XXXXXXXXX."""
    if not tin or not isinstance(tin, str):
        return False
    return bool(TAX_ID_PATTERN.match(tin))


def is_ghana_card(value: str) -> bool:
    """Return True when value looks like a Ghana Card ID (personal identifier)."""
    return bool(GHANA_CARD_PATTERN.match(value))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestBusinessRegistrationValidation:
    """Business registration must follow EA-XXXXXX format."""

    def test_valid_registration(self):
        assert validate_business_registration("EA-123456") is True

    def test_valid_registration_minimum(self):
        assert validate_business_registration("EA-000001") is True

    def test_valid_registration_maximum(self):
        assert validate_business_registration("EA-999999") is True

    def test_invalid_registration_missing_prefix(self):
        assert validate_business_registration("123456") is False

    def test_invalid_registration_wrong_prefix(self):
        assert validate_business_registration("GH-123456") is False

    def test_invalid_registration_too_short(self):
        assert validate_business_registration("EA-12345") is False

    def test_invalid_registration_too_long(self):
        assert validate_business_registration("EA-1234567") is False

    def test_invalid_registration_letters_in_digits(self):
        assert validate_business_registration("EA-12A456") is False

    def test_invalid_registration_empty(self):
        assert validate_business_registration("") is False

    def test_invalid_registration_none(self):
        assert validate_business_registration(None) is False

    def test_invalid_registration_lowercase_prefix(self):
        assert validate_business_registration("ea-123456") is False

    def test_invalid_registration_with_spaces(self):
        assert validate_business_registration("EA 123456") is False


class TestTaxIdValidation:
    """Tax ID must follow TIN-XXXXXXXXX format."""

    def test_valid_tax_id(self):
        assert validate_tax_id("TIN-123456789") is True

    def test_valid_tax_id_minimum(self):
        assert validate_tax_id("TIN-000000001") is True

    def test_valid_tax_id_maximum(self):
        assert validate_tax_id("TIN-999999999") is True

    def test_invalid_tax_id_missing_prefix(self):
        assert validate_tax_id("123456789") is False

    def test_invalid_tax_id_wrong_prefix(self):
        assert validate_tax_id("TIN-12345678") is False

    def test_invalid_tax_id_too_long(self):
        assert validate_tax_id("TIN-1234567890") is False

    def test_invalid_tax_id_letters(self):
        assert validate_tax_id("TIN-12345A789") is False

    def test_invalid_tax_id_empty(self):
        assert validate_tax_id("") is False

    def test_invalid_tax_id_none(self):
        assert validate_tax_id(None) is False

    def test_invalid_tax_id_lowercase(self):
        assert validate_tax_id("tin-123456789") is False


class TestGhanaCardNotUsedForVendors:
    """Ghana Card ID is a personal identifier and must NOT be collected for vendors."""

    def test_ghana_card_format_is_recognised(self):
        """The format itself is valid (for staff/patron use)."""
        assert is_ghana_card("GHA-123456789-0") is True

    def test_ghana_card_not_accepted_as_business_registration(self):
        """A Ghana Card ID must NOT pass business registration validation."""
        assert validate_business_registration("GHA-123456789-0") is False

    def test_ghana_card_not_accepted_as_tax_id(self):
        """A Ghana Card ID must NOT pass tax ID validation."""
        assert validate_tax_id("GHA-123456789-0") is False

    def test_business_registration_not_ghana_card(self):
        """A business registration must NOT be mistaken for a Ghana Card ID."""
        assert is_ghana_card("EA-123456") is False

    def test_tax_id_not_ghana_card(self):
        """A TIN must NOT be mistaken for a Ghana Card ID."""
        assert is_ghana_card("TIN-123456789") is False


class TestVendorDocumentValidation:
    """Simulate the db:save-vendor validation logic."""

    def test_valid_vendor_document(self):
        vendor = {
            "name": "Accra Educational Publishers",
            "businessRegistration": "EA-123456",
            "taxId": "TIN-123456789",
            "businessType": "company",
            "contactPerson": "Kwame Asante",
            "phone": "+233241234567",
            "email": "info@accraedu.com",
            "address": "12 Independence Ave",
            "city": "Accra",
            "region": "Greater Accra",
            "country": "Ghana",
        }
        # Should not raise
        _validate_vendor_or_fail(vendor)

    def test_vendor_missing_business_registration(self):
        vendor = {
            "name": "Accra Educational Publishers",
            "taxId": "TIN-123456789",
        }
        try:
            _validate_vendor_or_fail(vendor)
            assert False, "Expected validation to fail"
        except ValueError as e:
            assert "business registration" in str(e).lower()

    def test_vendor_invalid_business_registration(self):
        vendor = {
            "name": "Accra Educational Publishers",
            "businessRegistration": "INVALID",
        }
        try:
            _validate_vendor_or_fail(vendor)
            assert False, "Expected validation to fail"
        except ValueError as e:
            assert "business registration" in str(e).lower()

    def test_vendor_ghana_card_rejected(self):
        """A vendor document with a Ghana Card ID should be rejected."""
        vendor = {
            "name": "Accra Educational Publishers",
            "businessRegistration": "GHA-123456789-0",
        }
        try:
            _validate_vendor_or_fail(vendor)
            assert False, "Expected validation to fail for Ghana Card as business registration"
        except ValueError as e:
            assert "business registration" in str(e).lower()


# ---------------------------------------------------------------------------
# Helper used by TestVendorDocumentValidation
# ---------------------------------------------------------------------------

def _validate_vendor_or_fail(vendor: dict) -> None:
    """Mirror the validation in db:save-vendor IPC handler."""
    reg = vendor.get("businessRegistration")
    if not reg or not validate_business_registration(reg):
        raise ValueError(
            "Invalid business registration format. Expected: EA-XXXXXX"
        )
    tin = vendor.get("taxId")
    if tin and not validate_tax_id(tin):
        raise ValueError(
            "Invalid tax ID format. Expected: TIN-XXXXXXXXX"
        )
    # Ensure no Ghana Card ID is being stored as a corporate identifier
    if is_ghana_card(reg):
        raise ValueError(
            "Ghana Card ID is a personal identifier and must not be used for vendors"
        )
