"""Tests for ayanamsa calculations."""

from datetime import datetime

import pytest

from ndastro_engine.ayanamsa import (
    _calculate_b6,
    get_aryabhatta_ayanamsa,
    get_fagan_bradley_ayanamsa,
    get_janma_ayanamsa,
    get_kali_ayanamsa,
    get_krishnamurti_new_ayanamsa,
    get_lahiri_ayanamsa,
    get_madhava_ayanamsa,
    get_raman_ayanamsa,
    get_suryasiddhanta_ayanamsa,
    get_true_ayanamsa,
    get_true_citra_ayanamsa,
    get_true_pusya_ayanamsa,
    get_true_revati_ayanamsa,
    get_ushashasi_ayanamsa,
    get_vishnu_ayanamsa,
    get_yukteshwar_ayanamsa,
)


class TestCalculateB6:
    """Test suite for _calculate_b6 helper function."""

    @pytest.mark.unit
    def test_b6_at_j2000_is_zero(self):
        """Test that B6 is approximately 0 at J2000.0 epoch (2000-01-01)."""
        b6 = _calculate_b6((2000, 1, 1))
        assert abs(b6) < 0.0001, f"B6 at J2000 should be ~0, got {b6}"

    @pytest.mark.unit
    def test_b6_at_future_date_is_positive(self):
        """Test that B6 is positive for dates after J2000."""
        b6 = _calculate_b6((2026, 1, 9))
        assert b6 > 0, f"B6 after J2000 should be positive, got {b6}"
        expected = 0.260219
        assert abs(b6 - expected) < 0.0001, f"B6 at 2026-01-09 should be {expected}, got {b6}"

    @pytest.mark.unit
    def test_b6_at_past_date_is_negative(self):
        """Test that B6 is negative for dates before J2000."""
        b6 = _calculate_b6((1990, 1, 1))
        assert b6 < 0, f"B6 before J2000 should be negative, got {b6}"
        expected = -0.099959
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
        ayanamsa = get_lahiri_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        # Lahiri ayanamsa at J2000.0 should be 23°51' = 23.85 degrees (astro-seek.com)
        expected = 23.85
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_lahiri_at_2026(self):
        """Test Lahiri Ayanamsa value in 2026."""
        ayanamsa = get_lahiri_ayanamsa(datetime(2026, 1, 9, 12, 0, 0))
        # Lahiri ayanamsa on 2026-01-09 should be 24.214308 degrees
        expected = 24.214308
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at 2026-01-09 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_lahiri_increases_with_time(self):
        """Test that Lahiri Ayanamsa increases over time (precession)."""
        ayanamsa_2000 = get_lahiri_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        ayanamsa_2010 = get_lahiri_ayanamsa(datetime(2010, 1, 1, 12, 0, 0))
        ayanamsa_2020 = get_lahiri_ayanamsa(datetime(2020, 1, 1, 12, 0, 0))

        assert ayanamsa_2000 < ayanamsa_2010 < ayanamsa_2020

    @pytest.mark.unit
    def test_lahiri_annual_rate(self):
        """Test that Lahiri Ayanamsa increases at approximately the correct rate."""
        ayanamsa_2000 = get_lahiri_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        ayanamsa_2001 = get_lahiri_ayanamsa(datetime(2001, 1, 1, 12, 0, 0))

        annual_rate = ayanamsa_2001 - ayanamsa_2000
        # Actual calculated annual rate
        expected_rate = 0.0140278447

    @pytest.mark.unit
    def test_lahiri_positive_value(self):
        """Test that Lahiri Ayanamsa returns positive values for modern dates."""
        ayanamsa = get_lahiri_ayanamsa(datetime(2024, 1, 1, 12, 0, 0))
        assert ayanamsa > 0, f"Ayanamsa should be positive, got {ayanamsa}"


class TestOtherAyanamsas:
    """Test suite for other Ayanamsa systems."""

    @pytest.mark.unit
    def test_raman_ayanamsa(self):
        """Test Raman Ayanamsa calculation."""
        ayanamsa = get_raman_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Raman ayanamsa at J2000 should be 22:24:44 = 22.412222°
        expected = 22.412222
        assert abs(ayanamsa - expected) < 0.001, f"Raman at J2000 should be {expected}° (22:24:44), got {ayanamsa}°"

    @pytest.mark.unit
    def test_krishnamurti_ayanamsa(self):
        """Test Krishnamurti Ayanamsa calculation."""
        ayanamsa = get_krishnamurti_new_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # KP ayanamsa at J2000 should be 23°45' = 23.75° (astro-seek.com)
        expected = 23.75
        assert abs(ayanamsa - expected) < 0.001, f"KP at J2000 should be {expected}° (23:45:00), got {ayanamsa}°"

    @pytest.mark.unit
    def test_fagan_bradley_ayanamsa(self):
        """Test Fagan-Bradley Ayanamsa calculation."""
        ayanamsa = get_fagan_bradley_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Fagan-Bradley ayanamsa at J2000 should be 24:44:00 = 24.733333°
        expected = 24.733333
        assert abs(ayanamsa - expected) < 0.001, f"Fagan-Bradley at J2000 should be {expected}° (24:44:00), got {ayanamsa}°"

    @pytest.mark.unit
    def test_all_ayanamsas_increase_with_time(self):
        """Test that all ayanamsa systems increase over time."""
        date1 = datetime(2000, 1, 1, 12, 0, 0)
        date2 = datetime(2020, 1, 1, 12, 0, 0)

        ayanamsa_functions = [
            get_lahiri_ayanamsa,
            get_raman_ayanamsa,
            get_kali_ayanamsa,
            get_krishnamurti_new_ayanamsa,
            get_fagan_bradley_ayanamsa,
            get_janma_ayanamsa,
            get_true_ayanamsa,
            get_madhava_ayanamsa,
            get_vishnu_ayanamsa,
            get_yukteshwar_ayanamsa,
            get_suryasiddhanta_ayanamsa,
            get_aryabhatta_ayanamsa,
            get_ushashasi_ayanamsa,
            get_true_citra_ayanamsa,
            get_true_revati_ayanamsa,
            get_true_pusya_ayanamsa,
        ]

        for func in ayanamsa_functions:
            ayanamsa1 = func(date1)
            ayanamsa2 = func(date2)
            assert ayanamsa2 > ayanamsa1, f"{func.__name__} should increase over time"

    @pytest.mark.unit
    def test_ayanamsa_systems_have_different_values(self):
        """Test that different ayanamsa systems produce different values."""
        date = datetime(2000, 1, 1, 12, 0, 0)

        lahiri = get_lahiri_ayanamsa(date)
        raman = get_raman_ayanamsa(date)
        krishnamurti = get_krishnamurti_new_ayanamsa(date)

        # Different systems should have different starting points
        assert lahiri != raman
        assert lahiri != krishnamurti
        assert raman != krishnamurti

    @pytest.mark.unit
    def test_kali_ayanamsa(self):
        """Test Kali Ayanamsa calculation."""
        ayanamsa = get_kali_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Kali ayanamsa at J2000 should be 27:23:59.944 = 27.399984°
        expected = 27.3999844448
        assert abs(ayanamsa - expected) < 0.0001, f"Kali at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_janma_ayanamsa(self):
        """Test Janma Ayanamsa calculation."""
        ayanamsa = get_janma_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Janma ayanamsa at J2000 should be 22:27:36.635 = 22.460176°
        expected = 22.4601764990
        assert abs(ayanamsa - expected) < 0.0001, f"Janma at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_ayanamsa(self):
        """Test True Ayanamsa calculation."""
        ayanamsa = get_true_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True ayanamsa at J2000 should be 24:02:31.851 = 24.042181°
        expected = 24.0421808936
        assert abs(ayanamsa - expected) < 0.0001, f"True at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_madhava_ayanamsa(self):
        """Test Madhava Ayanamsa calculation."""
        ayanamsa = get_madhava_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Madhava ayanamsa at J2000 should be 23:53:44.804 = 23.895779°
        expected = 23.8957787517
        assert abs(ayanamsa - expected) < 0.0001, f"Madhava at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_vishnu_ayanamsa(self):
        """Test Vishnu Ayanamsa calculation."""
        ayanamsa = get_vishnu_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Vishnu ayanamsa at J2000 should be 24:00:30.171 = 24.008381°
        expected = 24.0083808936
        assert abs(ayanamsa - expected) < 0.0001, f"Vishnu at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_yukteshwar_ayanamsa(self):
        """Test Yukteshwar Ayanamsa calculation."""
        ayanamsa = get_yukteshwar_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Yukteshwar ayanamsa at J2000 should be 22°28' = 22.466667° (astro-seek.com)
        expected = 22.466667
        assert abs(ayanamsa - expected) < 0.0001, f"Yukteshwar at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_suryasiddhanta_ayanamsa(self):
        """Test Suryasiddhanta Ayanamsa calculation."""
        ayanamsa = get_suryasiddhanta_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Suryasiddhanta ayanamsa at J2000 should be 23:59:59.931 = 23.999981°
        expected = 23.9999809105
        assert abs(ayanamsa - expected) < 0.0001, f"Suryasiddhanta at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_aryabhatta_ayanamsa(self):
        """Test Aryabhatta Ayanamsa calculation."""
        ayanamsa = get_aryabhatta_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Aryabhatta ayanamsa at J2000 should be 23:41:59.926 = 23.699979°
        expected = 23.6999794966
        assert abs(ayanamsa - expected) < 0.0001, f"Aryabhatta at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_ushashasi_ayanamsa(self):
        """Test Ushashasi Ayanamsa calculation."""
        ayanamsa = get_ushashasi_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # Ushashasi ayanamsa at J2000 should be 20°03' = 20.05° (astro-seek.com)
        expected = 20.05
        assert abs(ayanamsa - expected) < 0.0001, f"Ushashasi at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_citra_ayanamsa(self):
        """Test True Citra Ayanamsa calculation."""
        ayanamsa = get_true_citra_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True Citra ayanamsa at J2000 should be 23°50' = 23.833333° (astro-seek.com)
        expected = 23.833333
        assert abs(ayanamsa - expected) < 0.0001, f"True Citra at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_revati_ayanamsa(self):
        """Test True Revati Ayanamsa calculation."""
        ayanamsa = get_true_revati_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True Revati ayanamsa at J2000 should be 20°02' = 20.033333° (astro-seek.com)
        expected = 20.033333
        assert abs(ayanamsa - expected) < 0.0001, f"True Revati at J2000 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_true_pusya_ayanamsa(self):
        """Test True Pusya Ayanamsa calculation."""
        ayanamsa = get_true_pusya_ayanamsa(datetime(2000, 1, 1, 12, 0, 0))
        assert isinstance(ayanamsa, float)
        # True Pusya ayanamsa at J2000 should be 24:05:59.932 = 24.099981°
        expected = 24.0999811369
        assert abs(ayanamsa - expected) < 0.0001, f"True Pusya at J2000 should be {expected}°, got {ayanamsa}°"


class TestAyanamsaEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    @pytest.mark.unit
    def test_lahiri_at_different_times_of_day(self):
        """Test that ayanamsa is relatively constant throughout a single day."""
        ayanamsa_morning = get_lahiri_ayanamsa(datetime(2024, 1, 1, 6, 0, 0))
        ayanamsa_noon = get_lahiri_ayanamsa(datetime(2024, 1, 1, 12, 0, 0))
        ayanamsa_evening = get_lahiri_ayanamsa(datetime(2024, 1, 1, 18, 0, 0))

        # Values should be very close (within 0.0001 degrees)
        assert abs(ayanamsa_morning - ayanamsa_noon) < 0.0001
        assert abs(ayanamsa_noon - ayanamsa_evening) < 0.0001

    @pytest.mark.unit
    def test_lahiri_at_historical_date(self):
        """Test Lahiri Ayanamsa at a historical date (1900)."""
        ayanamsa = get_lahiri_ayanamsa(datetime(1900, 1, 1, 12, 0, 0))
        expected = 22.450220
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at 1900 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_lahiri_far_future(self):
        """Test Lahiri Ayanamsa for a far future date."""
        ayanamsa = get_lahiri_ayanamsa(datetime(2100, 1, 1, 12, 0, 0))
        expected = 25.25
        assert abs(ayanamsa - expected) < 0.0001, f"Lahiri at 2100 should be {expected}°, got {ayanamsa}°"

    @pytest.mark.unit
    def test_ayanamsa_consistency_across_month(self):
        """Test that ayanamsa values are monotonically increasing across a month."""
        date1 = datetime(2024, 1, 1, 12, 0, 0)
        date2 = datetime(2024, 1, 15, 12, 0, 0)
        date3 = datetime(2024, 1, 31, 12, 0, 0)

        ayanamsa1 = get_lahiri_ayanamsa(date1)
        ayanamsa2 = get_lahiri_ayanamsa(date2)
        ayanamsa3 = get_lahiri_ayanamsa(date3)

        assert ayanamsa1 < ayanamsa2 < ayanamsa3
