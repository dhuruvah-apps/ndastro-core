"""Tests for dasa calculations."""

from datetime import date as _date
from datetime import datetime, timedelta

import pytest
import pytz

from ndastro_engine.dasa import (
    DasaContext,
    DasaDefinition,
    DasaQuery,
    RunningDasa,
    get_dasa_birth_info,
    get_dasa_timeline,
    get_running_dasa,
    get_supported_dasa_types,
    register_dasa_type,
)
from ndastro_engine.enums import Nakshatras, Planets


class TestSupportedDasaTypes:
    @pytest.mark.unit
    def test_supported_dasa_types_include_vimshottari_only_by_default(self) -> None:
        supported = get_supported_dasa_types()

        assert supported == ("vimshottari",)


class TestDasaBirthInfo:
    @pytest.mark.unit
    def test_birth_info_returns_valid_values(self) -> None:
        birth = datetime(1990, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)

        info = get_dasa_birth_info(
            DasaContext(
                birth_datetime=birth,
                lat=12.97,
                lon=77.59,
                ayanamsa_system="lahiri",
                dasa_type="vimshottari",
            )
        )

        assert 0.0 <= info.sidereal_moon_longitude < 360.0
        assert 0.0 <= info.nakshatra_progress_fraction <= 1.0
        assert 0.0 <= info.nakshatra_remaining_fraction <= 1.0
        assert info.start_lord


class TestDasaTimeline:
    @pytest.mark.unit
    def test_timeline_has_four_levels(self) -> None:
        birth = datetime(1992, 7, 15, 6, 30, 0, tzinfo=pytz.UTC)

        timeline = get_dasa_timeline(
            DasaContext(
                birth_datetime=birth,
                lat=13.0827,
                lon=80.2707,
                dasa_type="vimshottari",
            ),
            DasaQuery(levels=4, years=20),
        )

        assert timeline

        maha = timeline[0]
        assert maha.level_name == "maha"
        assert maha.children

        antara = maha.children[0]
        assert antara.level_name == "antara"
        assert antara.children

        pratyantara = antara.children[0]
        assert pratyantara.level_name == "pratyantara"
        assert pratyantara.children

        sookshma = pratyantara.children[0]
        assert sookshma.level_name == "sookshma"

    @pytest.mark.unit
    def test_timeline_is_contiguous(self) -> None:
        birth = datetime(2001, 5, 21, 9, 45, 0, tzinfo=pytz.UTC)

        timeline = get_dasa_timeline(
            DasaContext(
                birth_datetime=birth,
                lat=28.6139,
                lon=77.2090,
                dasa_type="vimshottari",
            ),
            DasaQuery(levels=1, years=40),
        )

        assert len(timeline) > 1
        for idx in range(1, len(timeline)):
            assert timeline[idx - 1].end_utc == timeline[idx].start_utc

    @pytest.mark.unit
    def test_running_dasa_returns_all_levels(self) -> None:
        birth = datetime(1995, 11, 4, 4, 0, 0, tzinfo=pytz.UTC)
        query = birth + timedelta(days=5000)

        running = get_running_dasa(
            query,
            DasaContext(
                birth_datetime=birth,
                lat=19.076,
                lon=72.8777,
                dasa_type="vimshottari",
            ),
            DasaQuery(years=40),
        )

        assert running.maha is not None
        assert running.antara is not None
        assert running.pratyantara is not None
        assert running.sookshma is not None

    @pytest.mark.unit
    @pytest.mark.usefixtures("dasa_registry_cleanup")
    def test_custom_registered_cycle_uses_expected_total_years(self) -> None:
        register_dasa_type(
            "custom_cycle",
            DasaDefinition(
                lords=(Planets.SUN.name, Planets.MOON.name, Planets.MARS.name),
                years_by_lord={
                    Planets.SUN.name: 6.0,
                    Planets.MOON.name: 4.0,
                    Planets.MARS.name: 5.0,
                },
                cycle_years=15.0,
                start_lord_resolver=lambda _n: Planets.SUN.name,
            ),
        )

        birth = datetime(1990, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        timeline = get_dasa_timeline(
            DasaContext(
                birth_datetime=birth,
                lat=12.97,
                lon=77.59,
                dasa_type="custom_cycle",
            ),
            DasaQuery(years=15),
        )

        last_end_from_birth = (timeline[-1].end_utc - birth).total_seconds() / 86400
        expected_days = 15 * 365.256364
        assert abs(last_end_from_birth - expected_days) < 1
        assert timeline[0].start_utc < birth

    @pytest.mark.unit
    @pytest.mark.usefixtures("dasa_registry_cleanup")
    def test_default_cycle_horizon_subtracts_elapsed_start_dasa_time(self) -> None:
        register_dasa_type(
            "custom_cycle_default_horizon",
            DasaDefinition(
                lords=(Planets.SUN.name, Planets.MOON.name, Planets.MARS.name),
                years_by_lord={
                    Planets.SUN.name: 6.0,
                    Planets.MOON.name: 4.0,
                    Planets.MARS.name: 5.0,
                },
                cycle_years=15.0,
                start_lord_resolver=lambda _n: Planets.SUN.name,
            ),
        )

        birth = datetime(1990, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        context = DasaContext(
            birth_datetime=birth,
            lat=12.97,
            lon=77.59,
            dasa_type="custom_cycle_default_horizon",
        )

        default_timeline = get_dasa_timeline(context)
        explicit_timeline = get_dasa_timeline(context, DasaQuery(years=15))

        default_days = (default_timeline[-1].end_utc - default_timeline[0].start_utc).total_seconds() / 86400
        explicit_days = (explicit_timeline[-1].end_utc - explicit_timeline[0].start_utc).total_seconds() / 86400

        assert default_days < explicit_days

    @pytest.mark.unit
    def test_removed_builtin_raises_value_error(self) -> None:
        birth = datetime(1985, 6, 10, 8, 0, 0, tzinfo=pytz.UTC)

        with pytest.raises(ValueError, match="Unsupported dasa_type"):
            get_dasa_timeline(
                DasaContext(
                    birth_datetime=birth,
                    lat=13.0827,
                    lon=80.2707,
                    dasa_type="ashtottari",
                )
            )

    @pytest.mark.unit
    @pytest.mark.usefixtures("dasa_registry_cleanup")
    def test_register_custom_dasa_type_works(self) -> None:
        """Custom dasa type can be registered and produces a valid timeline."""
        custom_lords = (Planets.SUN.name, Planets.MOON.name, Planets.MARS.name)
        custom_years = {Planets.SUN.name: 5.0, Planets.MOON.name: 7.0, Planets.MARS.name: 3.0}

        register_dasa_type(
            "custom_test",
            DasaDefinition(
                lords=custom_lords,
                years_by_lord=custom_years,
                cycle_years=15.0,
                start_lord_resolver=lambda _n: Planets.SUN.name,
            ),
        )

        assert "custom_test" in get_supported_dasa_types()

        birth = datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        timeline = get_dasa_timeline(
            DasaContext(birth_datetime=birth, lat=0.0, lon=0.0, dasa_type="custom_test"),
            DasaQuery(levels=1),
        )

        assert timeline
        for idx in range(1, len(timeline)):
            assert timeline[idx - 1].end_utc == timeline[idx].start_utc

    @pytest.mark.unit
    def test_register_builtin_name_raises(self) -> None:
        with pytest.raises(ValueError, match="Cannot overwrite built-in"):
            register_dasa_type(
                "vimshottari",
                DasaDefinition(
                    lords=("SUN",),
                    years_by_lord={"SUN": 1.0},
                    cycle_years=1.0,
                    start_lord_resolver=lambda _n: "SUN",
                ),
            )

    @pytest.mark.unit
    def test_register_empty_name_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty string"):
            register_dasa_type(
                "",
                DasaDefinition(
                    lords=("SUN",),
                    years_by_lord={"SUN": 1.0},
                    cycle_years=1.0,
                    start_lord_resolver=lambda _n: "SUN",
                ),
            )

    @pytest.mark.unit
    def test_invalid_level_raises_value_error(self) -> None:
        birth = datetime(1990, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        with pytest.raises(ValueError, match="levels must be between 1 and 4"):
            get_dasa_timeline(
                DasaContext(
                    birth_datetime=birth,
                    lat=0.0,
                    lon=0.0,
                ),
                DasaQuery(levels=5),
            )

    @pytest.mark.unit
    def test_invalid_years_raises_value_error(self) -> None:
        birth = datetime(1990, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)

        with pytest.raises(ValueError, match="years must be greater than 0"):
            get_dasa_timeline(
                DasaContext(
                    birth_datetime=birth,
                    lat=0.0,
                    lon=0.0,
                ),
                DasaQuery(years=0),
            )


class TestKnownRunningDasa:
    """Snapshot tests: fixed birth data cross-checked against known period values."""

    # Birth: 1985-10-24 06:30 IST (01:00 UTC), Chennai, Lahiri ayanamsa, Vimshottari
    _BIRTH = datetime(1985, 10, 24, 1, 0, 0, tzinfo=pytz.UTC)
    _QUERY_DT = datetime(2026, 4, 18, 12, 0, 0, tzinfo=pytz.UTC)
    _CTX = DasaContext(
        birth_datetime=_BIRTH,
        lat=13.08,
        lon=80.28,
        ayanamsa_system="lahiri",
        dasa_type="vimshottari",
    )

    @pytest.fixture
    def running_dasa(self):
        return get_running_dasa(self._QUERY_DT, self._CTX, DasaQuery(levels=4))

    @pytest.mark.integration
    def test_dasa_birth_info(self) -> None:
        """The query date must fall within the maha dasa period."""
        birth_info = get_dasa_birth_info(self._CTX)

        assert birth_info.start_lord == "RAHU"
        assert birth_info.janma_nakshatra == Nakshatras.SHATHAYAM

    @pytest.mark.integration
    def test_maha_dasa_lord_and_dates(self, running_dasa: RunningDasa) -> None:
        """Maha dasa should be SATURN from 2009-03-28 to 2028-03-28."""
        maha = running_dasa.maha if running_dasa.maha else None
        assert maha is not None
        assert maha.lord == "SATURN"
        assert maha.start_utc.date() == _date(2009, 3, 28)
        assert maha.end_utc.date() == _date(2028, 3, 28)

    @pytest.mark.integration
    def test_antara_dasa_lord_and_dates(self, running_dasa: RunningDasa) -> None:
        """Antara dasa should be JUPITER from 2025-09-15 to 2028-03-28."""
        antara = running_dasa.antara if running_dasa.antara else None
        assert antara is not None
        assert antara.lord == "JUPITER"
        assert antara.start_utc.date() == _date(2025, 9, 15)
        assert antara.end_utc.date() == _date(2028, 3, 28)

    @pytest.mark.integration
    def test_pratyantara_dasa_lord_and_dates(self, running_dasa: RunningDasa) -> None:
        """Pratyantara dasa should be SATURN from 2026-01-16 to 2026-06-12."""
        pratyantara = running_dasa.pratyantara if running_dasa.pratyantara else None
        assert pratyantara is not None

        assert pratyantara.lord == "SATURN"
        assert pratyantara.start_utc.date() == _date(2026, 1, 16)
        assert pratyantara.end_utc.date() == _date(2026, 6, 12)

    @pytest.mark.integration
    def test_sookshma_dasa_lord_and_dates(self, running_dasa: RunningDasa) -> None:
        """Sookshma dasa should be MOON from 2026-04-10 to 2026-04-23."""
        sookshma = running_dasa.sookshma if running_dasa.sookshma else None
        assert sookshma is not None

        assert sookshma.lord == "MOON"
        assert sookshma.start_utc.date() == _date(2026, 4, 10)
        assert sookshma.end_utc.date() == _date(2026, 4, 23)

    @pytest.mark.integration
    def test_all_levels_are_non_none(self, running_dasa: RunningDasa) -> None:
        """All four dasa levels must be populated for the query date."""
        assert running_dasa.maha is not None
        assert running_dasa.antara is not None
        assert running_dasa.pratyantara is not None
        assert running_dasa.sookshma is not None

    @pytest.mark.integration
    def test_period_hierarchy_is_nested(self, running_dasa: RunningDasa) -> None:
        """Each level's window must be fully contained within its parent's window."""
        maha = running_dasa.maha if running_dasa.maha else None
        antara = running_dasa.antara if running_dasa.antara else None
        pratyantara = running_dasa.pratyantara if running_dasa.pratyantara else None
        sookshma = running_dasa.sookshma if running_dasa.sookshma else None
        assert maha is not None
        assert antara is not None
        assert pratyantara is not None
        assert sookshma is not None

        assert maha.start_utc <= antara.start_utc
        assert antara.end_utc <= maha.end_utc
        assert antara.start_utc <= pratyantara.start_utc
        assert pratyantara.end_utc <= antara.end_utc
        assert pratyantara.start_utc <= sookshma.start_utc
        assert sookshma.end_utc <= pratyantara.end_utc
