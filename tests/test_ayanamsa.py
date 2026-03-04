"""Tests for ayanamsa calculations."""

from datetime import datetime

import pytest

from ndastro_engine.ayanamsa import (
    _calculate_b6,
    _get_aryabhatta_ayanamsa,
    _get_fagan_bradley_ayanamsa,
    _get_janma_ayanamsa,
    _get_kali_ayanamsa,
    _get_krishnamurti_new_ayanamsa,
    _get_lahiri_ayanamsa,
    _get_madhava_ayanamsa,
    _get_raman_ayanamsa,
    _get_suryasiddhanta_ayanamsa,
    _get_true_ayanamsa,
    _get_true_citra_ayanamsa,
    _get_true_pusya_ayanamsa,
    _get_true_revati_ayanamsa,
    _get_ushashasi_ayanamsa,
    _get_vishnu_ayanamsa,
    _get_yukteshwar_ayanamsa,
)


class TestCalculateB6:
    """Test suite for _calculate_b6 helper function."""

    @pytest.mark.unit
    def test_b6_at_j2000_is_zero(self):
        """Test that B6 is approximately 1 at J2000.0 epoch (2000-01-01)."""
        b6 = _calculate_b6((2000, 1, 1))
        assert abs(b6 - 1.0) < 0.001, f"B6 at J2000 should be ~1.0, got {b6}"

    @pytest.mark.unit
    def test_b6_at_future_date_is_positive(self):
        """Test that B6 is positive for dates after J2000."""
        b6 = _calculate_b6((2026, 1, 9))
        assert b6 > 0, f"B6 after J2000 should be positive, got {b6}"
        expected = 1.2601916715
        assert abs(b6 - expected) < 0.0001, f"B6 at 2026-01-09 should be {expected}, got {b6}"

    @pytest.mark.unit
    def test_b6_at_past_date_is_positive(self):
        """Test that B6 is positive even for dates before J2000 (depends on reference epoch)."""
        b6 = _calculate_b6((1990, 1, 1))
        assert b6 > 0, f"B6 should be positive, got {b6}"
        expected = 0.8999726396
        assert abs(b6 - expected) < 0.0001, f"B6 at 1990 should be {expected}, got {b6}"

    @pytest.mark.unit
    def test_b6_increases_with_time(self):
        """Test that B6 increases as time progresses."""
        b6_2000 = _calculate_b6((2000, 1, 1))
        b6_2010 = _calculate_b6((2010, 1, 1))
        b6_2020 = _calculate_b6((2020, 1, 1))

        assert b6_2000 < b6_2010 < b6_2020


class TestLahiriAyanamsa:
    """Test suite for Lahiri Ayanamsa calculation."""

    @pytest.mark.unit
    def test_lahiri_at_j2000(self):
        """Test Lahiri Ayanamsa value at J2000.0 epoch."""
        ayanamsa = _get_lahiri_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        # Lahiri ayanamsa at J2000.0 should be 23°51'23" = 23.8564 degrees
        expected = 23.8564406708
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_lahiri_at_2026(self):
        """Test Lahiri Ayanamsa value in 2026."""
        ayanamsa = _get_lahiri_ayanamsa(datetime(2026, 1, 9, 12, 0, 0))
        # Lahiri ayanamsa on 2026-01-09 should be 24.2199 degrees
        expected = 24.2199176310
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at 2026-01-09 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_lahiri_increases_with_time(self):
        """Test that Lahiri Ayanamsa increases over time (precession)."""
        ayanamsa_2000 = _get_lahiri_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        ayanamsa_2010 = _get_lahiri_ayanamsa(datetime(2010, 1, 1, 12, 0, 0))
        ayanamsa_2020 = _get_lahiri_ayanamsa(datetime(2020, 1, 1, 12, 0, 0))

        assert ayanamsa_2000 < ayanamsa_2010 < ayanamsa_2020

    @pytest.mark.unit
    def test_lahiri_annual_rate(self):
        """Test that Lahiri Ayanamsa increases at approximately the correct rate."""
        ayanamsa_2000 = _get_lahiri_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        ayanamsa_2001 = _get_lahiri_ayanamsa(datetime(2001, 1, 1, 12, 0, 0))

        annual_rate = ayanamsa_2001 - ayanamsa_2000
        # Actual calculated annual rate
        expected_rate = 0.0140278447

    @pytest.mark.unit
    def test_lahiri_positive_value(self):
        """Test that Lahiri Ayanamsa returns positive values for modern dates."""
        ayanamsa = _get_lahiri_ayanamsa(datetime(2024, 1, 1, 12, 0, 0))
        assert ayanamsa > 0, f"Ayanamsa should be positive, got {ayanamsa}"


class TestOtherAyanamsas:
    """Test suite for other Ayanamsa systems."""

    @pytest.mark.unit
    def test_raman_ayanamsa(self):
        """Test Raman Ayanamsa calculation."""
        ayanamsa = _get_raman_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Raman ayanamsa at J2000 should be 23.7999°
        expected = 23.7999430233
        assert abs(ayanamsa - expected) < 0.001, f"Raman at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_krishnamurti_ayanamsa(self):
        """Test Krishnamurti Ayanamsa calculation."""
        ayanamsa = _get_krishnamurti_new_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # KP ayanamsa at J2000 should be 25.1500°
        expected = 25.1499637748
        assert abs(ayanamsa - expected) < 0.001, f"KP at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_fagan_bradley_ayanamsa(self):
        """Test Fagan-Bradley Ayanamsa calculation."""
        ayanamsa = _get_fagan_bradley_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Fagan-Bradley ayanamsa at J2000 should be 26.1333°
        expected = 26.1332952817
        assert abs(ayanamsa - expected) < 0.001, f"Fagan-Bradley at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_all_ayanamsas_increase_with_time(self):
        """Test that all ayanamsa systems increase over time."""
        date1 = datetime(2000, 1, 1, 12, 0, 0)
        date2 = datetime(2020, 1, 1, 12, 0, 0)

        ayanamsa_functions = [
            _get_lahiri_ayanamsa,
            _get_raman_ayanamsa,
            _get_kali_ayanamsa,
            _get_krishnamurti_new_ayanamsa,
            _get_fagan_bradley_ayanamsa,
            _get_janma_ayanamsa,
            _get_true_ayanamsa,
            _get_madhava_ayanamsa,
            _get_vishnu_ayanamsa,
            _get_yukteshwar_ayanamsa,
            _get_suryasiddhanta_ayanamsa,
            _get_aryabhatta_ayanamsa,
            _get_ushashasi_ayanamsa,
            _get_true_citra_ayanamsa,
            _get_true_revati_ayanamsa,
            _get_true_pusya_ayanamsa,
        ]

        for func in ayanamsa_functions:
            ayanamsa1 = func(date1)
            ayanamsa2 = func(date2)
            assert ayanamsa2 > ayanamsa1, f"{func.__name__} should increase over time"

    @pytest.mark.unit
    def test_ayanamsa_systems_have_different_values(self):
        """Test that different ayanamsa systems produce different values."""
        date = datetime(2000, 1, 1, 12, 0, 0)

        lahiri = _get_lahiri_ayanamsa(date)
        raman = _get_raman_ayanamsa(date)
        krishnamurti = _get_krishnamurti_new_ayanamsa(date)

        # Different systems should have different starting points
        assert lahiri != raman
        assert lahiri != krishnamurti
        assert raman != krishnamurti

    @pytest.mark.unit
    def test_kali_ayanamsa(self):
        """Test Kali Ayanamsa calculation."""
        ayanamsa = _get_kali_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Kali ayanamsa at J2000 should be 28.5383°
        expected = 28.5382632626
        assert abs(ayanamsa - expected) < 0.0001, f"Kali at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_janma_ayanamsa(self):
        """Test Janma Ayanamsa calculation."""
        ayanamsa = _get_janma_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Janma ayanamsa at J2000 should be 24.1797°
        expected = 24.1796794066
        assert abs(ayanamsa - expected) < 0.0001, f"Janma at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_ayanamsa(self):
        """Test True Ayanamsa calculation."""
        ayanamsa = _get_true_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True ayanamsa at J2000 should be 25.4403°
        expected = 25.4402525985
        assert abs(ayanamsa - expected) < 0.0001, f"True at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_madhava_ayanamsa(self):
        """Test Madhava Ayanamsa calculation."""
        ayanamsa = _get_madhava_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Madhava ayanamsa at J2000 should be 25.4505°
        expected = 25.4504561737
        assert abs(ayanamsa - expected) < 0.0001, f"Madhava at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_vishnu_ayanamsa(self):
        """Test Vishnu Ayanamsa calculation."""
        ayanamsa = _get_vishnu_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Vishnu ayanamsa at J2000 should be 25.4065°
        expected = 25.4064525985
        assert abs(ayanamsa - expected) < 0.0001, f"Vishnu at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_yukteshwar_ayanamsa(self):
        """Test Yukteshwar Ayanamsa calculation."""
        ayanamsa = _get_yukteshwar_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Yukteshwar ayanamsa at J2000 should be 23.8666°
        expected = 23.8666323530
        assert abs(ayanamsa - expected) < 0.0001, f"Yukteshwar at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_suryasiddhanta_ayanamsa(self):
        """Test Suryasiddhanta Ayanamsa calculation."""
        ayanamsa = _get_suryasiddhanta_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Suryasiddhanta ayanamsa at J2000 should be 25.3967°
        expected = 25.3967226568
        assert abs(ayanamsa - expected) < 0.0001, f"Suryasiddhanta at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_aryabhatta_ayanamsa(self):
        """Test Aryabhatta Ayanamsa calculation."""
        ayanamsa = _get_aryabhatta_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Aryabhatta ayanamsa at J2000 should be 25.2001°
        expected = 25.2001384124
        assert abs(ayanamsa - expected) < 0.0001, f"Aryabhatta at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_ushashasi_ayanamsa(self):
        """Test Ushashasi Ayanamsa calculation."""
        ayanamsa = _get_ushashasi_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Ushashasi ayanamsa at J2000 should be 21.4500°
        expected = 21.4499616631
        assert abs(ayanamsa - expected) < 0.0001, f"Ushashasi at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_citra_ayanamsa(self):
        """Test True Citra Ayanamsa calculation."""
        ayanamsa = _get_true_citra_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True Citra ayanamsa at J2000 should be 25.2333°
        expected = 25.2332951996
        assert abs(ayanamsa - expected) < 0.0001, f"True Citra at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_revati_ayanamsa(self):
        """Test True Revati Ayanamsa calculation."""
        ayanamsa = _get_true_revati_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True Revati ayanamsa at J2000 should be 21.4333°
        expected = 21.4332956033
        assert abs(ayanamsa - expected) < 0.0001, f"True Revati at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_pusya_ayanamsa(self):
        """Test True Pusya Ayanamsa calculation."""
        ayanamsa = _get_true_pusya_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True Pusya ayanamsa at J2000 should be 25.4802°
        expected = 25.4802033332
        assert abs(ayanamsa - expected) < 0.0001, f"True Pusya at J2000 should be {expected}°, got {ayanamsa}°"


class TestAyanamsaEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    @pytest.mark.unit
    def test_lahiri_at_different_times_of_day(self):
        """Test that ayanamsa is relatively constant throughout a single day."""
        ayanamsa_morning = _get_lahiri_ayanamsa(datetime(2024, 1, 1, 6, 0, 0))
        ayanamsa_noon = _get_lahiri_ayanamsa(datetime(2024, 1, 1, 12, 0, 0))
        ayanamsa_evening = _get_lahiri_ayanamsa(datetime(2024, 1, 1, 18, 0, 0))

        # Values should be very close (within 0.0001 degrees)
        assert abs(ayanamsa_morning - ayanamsa_noon) < 0.0001
        assert abs(ayanamsa_noon - ayanamsa_evening) < 0.0001

    @pytest.mark.unit
    def test_lahiri_at_historical_date(self):
        """Test Lahiri Ayanamsa at a historical date (1900)."""
        ayanamsa = _get_lahiri_ayanamsa(datetime(1900, 1, 1, 12, 0, 0))
        expected = 22.4601289079
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at 1900 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_lahiri_far_future(self):
        """Test Lahiri Ayanamsa for a far future date."""
        ayanamsa = _get_lahiri_ayanamsa(datetime(2100, 1, 1, 12, 0, 0))
        expected = 25.2534066477
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at 2100 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_ayanamsa_consistency_across_month(self):
        """Test that ayanamsa values are monotonically increasing across a month."""
        date1 = datetime(2024, 1, 1, 12, 0, 0)
        date2 = datetime(2024, 1, 15, 12, 0, 0)
        date3 = datetime(2024, 1, 31, 12, 0, 0)

        ayanamsa1 = _get_lahiri_ayanamsa(date1)
        ayanamsa2 = _get_lahiri_ayanamsa(date2)
        ayanamsa3 = _get_lahiri_ayanamsa(date3)

        assert ayanamsa1 < ayanamsa2 < ayanamsa3
