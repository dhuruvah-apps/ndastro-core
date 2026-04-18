"""Unit tests for ndastro_engine.enums module."""

import pytest

from ndastro_engine.enums import Nakshatras, Planets


class TestPlanetsEnum:
    """Test cases for Planets enum."""

    @pytest.mark.unit
    def test_planets_enum_values(self) -> None:
        """Test that all planet enum values are correct."""
        assert Planets.EMPTY == -1
        assert Planets.ASCENDANT == 0
        assert Planets.SUN == 1
        assert Planets.MOON == 2
        assert Planets.MARS == 3
        assert Planets.MERCURY == 4
        assert Planets.JUPITER == 5
        assert Planets.VENUS == 6
        assert Planets.SATURN == 7
        assert Planets.RAHU == 8
        assert Planets.KETHU == 9

    @pytest.mark.unit
    def test_planets_to_string(self) -> None:
        """Test to_string method converts planet numbers to names."""
        assert Planets.to_string(1) == "SUN"
        assert Planets.to_string(2) == "MOON"
        assert Planets.to_string(5) == "JUPITER"
        assert Planets.to_string(99) == "empty"
        assert Planets.to_string(-1) == "EMPTY"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "planet_num,expected_name",
        [
            (0, "ASCENDANT"),
            (1, "SUN"),
            (2, "MOON"),
            (3, "MARS"),
            (4, "MERCURY"),
            (5, "JUPITER"),
            (6, "VENUS"),
            (7, "SATURN"),
            (8, "RAHU"),
            (9, "KETHU"),
        ],
    )
    def test_planets_to_string_parametrized(self, planet_num: int, expected_name: str) -> None:
        """Test to_string with all valid planets."""
        assert Planets.to_string(planet_num) == expected_name

    @pytest.mark.unit
    def test_planets_from_code(self) -> None:
        """Test from_code method converts planet codes to enums."""
        assert Planets.from_astronomical_code("sun") == Planets.SUN
        assert Planets.from_astronomical_code("moon") == Planets.MOON
        assert Planets.from_astronomical_code("mars barycenter") == Planets.MARS
        assert Planets.from_astronomical_code("mercury") == Planets.MERCURY
        assert Planets.from_astronomical_code("jupiter barycenter") == Planets.JUPITER
        assert Planets.from_astronomical_code("venus") == Planets.VENUS
        assert Planets.from_astronomical_code("saturn barycenter") == Planets.SATURN
        assert Planets.from_astronomical_code("rahu") == Planets.RAHU
        assert Planets.from_astronomical_code("kethu") == Planets.KETHU
        assert Planets.from_astronomical_code("invalid") == Planets.EMPTY

    @pytest.mark.unit
    def test_planets_to_list(self) -> None:
        """Test to_list method returns list of planet names."""
        planet_list = Planets.to_list()

        assert isinstance(planet_list, list)
        assert len(planet_list) == 11  # All planets including EMPTY and ASCENDANT
        assert "SUN" in planet_list
        assert "MOON" in planet_list
        assert "MARS" in planet_list
        assert "JUPITER" in planet_list
        assert "RAHU" in planet_list
        assert "KETHU" in planet_list

    @pytest.mark.unit
    def test_planets_code_property(self) -> None:
        """Test code property returns correct planet short codes."""
        assert Planets.SUN.code == "SU"
        assert Planets.MOON.code == "MO"
        assert Planets.MARS.code == "MA"
        assert Planets.MERCURY.code == "ME"
        assert Planets.JUPITER.code == "JU"
        assert Planets.VENUS.code == "VE"
        assert Planets.SATURN.code == "SA"
        assert Planets.RAHU.code == "RA"
        assert Planets.KETHU.code == "KE"
        assert Planets.ASCENDANT.code == "AS"
        assert Planets.EMPTY.code == "EMPTY"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "planet,expected_code",
        [
            (Planets.SUN, "SU"),
            (Planets.MOON, "MO"),
            (Planets.MARS, "MA"),
            (Planets.MERCURY, "ME"),
            (Planets.JUPITER, "JU"),
            (Planets.VENUS, "VE"),
            (Planets.SATURN, "SA"),
            (Planets.RAHU, "RA"),
            (Planets.KETHU, "KE"),
        ],
    )
    def test_planets_code_property_parametrized(self, planet: Planets, expected_code: str) -> None:
        """Test code property with all major planets."""
        assert planet.code == expected_code

    @pytest.mark.unit
    def test_planets_astronomical_code_property(self) -> None:
        """Test astronomical_code property returns correct astronomical codes."""
        assert Planets.SUN.astronomical_code == "sun"
        assert Planets.MOON.astronomical_code == "moon"
        assert Planets.MARS.astronomical_code == "mars barycenter"
        assert Planets.MERCURY.astronomical_code == "mercury"
        assert Planets.JUPITER.astronomical_code == "jupiter barycenter"
        assert Planets.VENUS.astronomical_code == "venus"
        assert Planets.SATURN.astronomical_code == "saturn barycenter"
        assert Planets.RAHU.astronomical_code == "rahu"
        assert Planets.KETHU.astronomical_code == "kethu"
        assert Planets.ASCENDANT.astronomical_code == "ascendant"
        assert Planets.EMPTY.astronomical_code == "empty"

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "planet,expected_code",
        [
            (Planets.SUN, "sun"),
            (Planets.MOON, "moon"),
            (Planets.MARS, "mars barycenter"),
            (Planets.MERCURY, "mercury"),
            (Planets.JUPITER, "jupiter barycenter"),
            (Planets.VENUS, "venus"),
            (Planets.SATURN, "saturn barycenter"),
            (Planets.RAHU, "rahu"),
            (Planets.KETHU, "kethu"),
        ],
    )
    def test_planets_astronomical_code_property_parametrized(self, planet: Planets, expected_code: str) -> None:
        """Test astronomical_code property with all major planets."""
        assert planet.astronomical_code == expected_code

    @pytest.mark.unit
    def test_planets_color_property(self) -> None:
        """Test color property returns valid hex color codes."""
        colors = {
            Planets.SUN: "#FFD700",
            Planets.MOON: "#C0C0C0",
            Planets.MARS: "#FF0000",
            Planets.MERCURY: "#008000",
            Planets.JUPITER: "#FFFF00",
            Planets.VENUS: "#FF69B4",
            Planets.SATURN: "#00008B",
            Planets.RAHU: "#8A2BE2",
            Planets.KETHU: "#8B0000",
            Planets.ASCENDANT: "#FFFFFF",
            Planets.EMPTY: "#000000",
        }

        for planet, expected_color in colors.items():
            assert planet.color == expected_color
            assert planet.color.startswith("#")
            assert len(planet.color) == 7  # #RRGGBB format

    @pytest.mark.unit
    def test_planets_color_property_hex_format(self) -> None:
        """Test that all color codes are valid hex format."""
        for planet in Planets:
            color = planet.color
            assert color.startswith("#")
            assert len(color) == 7
            # Check that characters after # are valid hex
            try:
                int(color[1:], 16)
            except ValueError:
                pytest.fail(f"{planet.name} color {color} is not valid hex")

    @pytest.mark.unit
    def test_planets_enum_unique_values(self) -> None:
        """Test that all planet enum values are unique."""
        values = [planet.value for planet in Planets]
        assert len(values) == len(set(values))

    @pytest.mark.unit
    def test_planets_enum_unique_names(self) -> None:
        """Test that all planet enum names are unique."""
        names = [planet.name for planet in Planets]
        assert len(names) == len(set(names))

    @pytest.mark.unit
    def test_planets_roundtrip_code_conversion(self) -> None:
        """Test that astronomical_code conversion works both ways."""
        for planet in Planets:
            if planet != Planets.EMPTY:
                code = planet.astronomical_code
                converted = Planets.from_astronomical_code(code)
                assert converted == planet

    @pytest.mark.unit
    def test_planets_enum_iteration(self) -> None:
        """Test that we can iterate over all planets."""
        planet_count = 0
        for planet in Planets:
            assert isinstance(planet, Planets)
            planet_count += 1

        assert planet_count == 11  # Total number of planets

    @pytest.mark.unit
    def test_planets_enum_comparison(self) -> None:
        """Test that planet enums can be compared."""
        assert Planets.SUN < Planets.MOON
        assert Planets.MARS > Planets.SUN
        assert Planets.RAHU > Planets.SATURN
        assert Planets.EMPTY < Planets.ASCENDANT

    @pytest.mark.unit
    def test_planets_enum_membership(self) -> None:
        """Test planet enum membership checks."""
        assert Planets.SUN in Planets
        assert Planets.MOON in Planets
        assert 1 in Planets._value2member_map_
        assert 99 not in Planets._value2member_map_


class TestNakshatrasEnum:
    """Test cases for Nakshatras enum."""

    @pytest.mark.unit
    def test_degrees_until_star_end(self) -> None:
        """Test degrees_until_star_end method calculates remaining degrees correctly."""
        # Test with a planet at 10 degrees in the first Nakshatra
        assert Nakshatras.degrees_until_star_end(302.383) == 0.3212750000000028

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("planet_longitude", "expected_pada"),
        [
            (0.0, 1),
            (3.3333333333333335, 2),
            (6.666666666666667, 3),
            (10.0, 4),
            (13.333333333333334, 1),
            (359.999, 4),
            (360.0, 1),
            (-1.0, 4),
        ],
    )
    def test_current_pada(self, planet_longitude: float, expected_pada: int) -> None:
        """Test current_pada returns a valid pada index from 1 to 4."""
        assert Nakshatras.current_pada(planet_longitude) == expected_pada
