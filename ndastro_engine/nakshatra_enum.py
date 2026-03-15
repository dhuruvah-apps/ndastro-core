"""Module is to hold start enums."""

from enum import Enum
from typing import Literal, TypeAlias, cast

from ndastro_engine.planet_enum import Planets

NakshatraCode: TypeAlias = Literal[
    "ASW",
    "BHA",
    "KAA",
    "ROG",
    "MIR",
    "THI",
    "PUN",
    "POO",
    "AAY",
    "MAG",
    "PRM",
    "UTH",
    "AST",
    "CHI",
    "SUV",
    "VIS",
    "ANU",
    "KET",
    "MOO",
    "PDM",
    "UTD",
    "TVO",
    "AVI",
    "SHA",
    "PRI",
    "UTI",
    "REV",
]


class Nakshatras(Enum):
    """Enum to hold stars."""

    ASWINNI = 1
    BHARANI = 2
    KAARTHIKAI = 3
    ROGHINI = 4
    MIRUGASIRISAM = 5
    THIRUVAATHIRAI = 6
    PUNARPOOSAM = 7
    POOSAM = 8
    AAYILYAM = 9
    MAGAM = 10
    POORAM = 11
    UTHTHIRAM = 12
    ASTHTHAM = 13
    CHITHTHIRAI = 14
    SUVAATHI = 15
    VISAAGAM = 16
    ANUSHAM = 17
    KETTAI = 18
    MOOLAM = 19
    POORAADAM = 20
    UTHTHIRAADAM = 21
    THIRUVONAM = 22
    AVITTAM = 23
    SHATHAYAM = 24
    POORATTAATHI = 25
    UTHTHIRATTAATHI = 26
    REVATHI = 27

    def __str__(self) -> str:
        """Return the display name of the star.

        Returns:
            str: The display name of the star.

        """
        return self.name

    @property
    def owner(self) -> Planets:
        """Return the owner (planet) of the star.

        Returns:
            str: The name of the planet that owns the star.

        """
        owners = {
            1: "kethu",
            2: "venus",
            3: "sun",
            4: "moon",
            5: "mars barycenter",
            6: "rahu",
            7: "jupiter barycenter",
            8: "saturn barycenter",
            9: "mercury",
            10: "kethu",
            11: "venus",
            12: "sun",
            13: "moon",
            14: "mars barycenter",
            15: "rahu",
            16: "jupiter barycenter",
            17: "saturn barycenter",
            18: "mercury",
            19: "kethu",
            20: "venus",
            21: "sun",
            22: "moon",
            23: "mars barycenter",
            24: "rahu",
            25: "jupiter barycenter",
            26: "saturn barycenter",
            27: "mercury",
        }

        return Planets.from_astronomical_code(owners[self.value])

    @property
    def code(self) -> NakshatraCode:
        """Return the astronomical code of the star.

        Returns:
            NakshatraCode: The astronomical code of the star.

        """
        nakshatra_codes = {
            Nakshatras.ASWINNI: "ASW",
            Nakshatras.BHARANI: "BHA",
            Nakshatras.KAARTHIKAI: "KAA",
            Nakshatras.ROGHINI: "ROG",
            Nakshatras.MIRUGASIRISAM: "MIR",
            Nakshatras.THIRUVAATHIRAI: "THI",
            Nakshatras.PUNARPOOSAM: "PUN",
            Nakshatras.POOSAM: "POO",
            Nakshatras.AAYILYAM: "AAY",
            Nakshatras.MAGAM: "MAG",
            Nakshatras.POORAM: "PRM",
            Nakshatras.UTHTHIRAM: "UTH",
            Nakshatras.ASTHTHAM: "AST",
            Nakshatras.CHITHTHIRAI: "CHI",
            Nakshatras.SUVAATHI: "SUV",
            Nakshatras.VISAAGAM: "VIS",
            Nakshatras.ANUSHAM: "ANU",
            Nakshatras.KETTAI: "KET",
            Nakshatras.MOOLAM: "MOO",
            Nakshatras.POORAADAM: "PDM",
            Nakshatras.UTHTHIRAADAM: "UTD",
            Nakshatras.THIRUVONAM: "TVO",
            Nakshatras.AVITTAM: "AVI",
            Nakshatras.SHATHAYAM: "SHA",
            Nakshatras.POORATTAATHI: "PRI",
            Nakshatras.UTHTHIRATTAATHI: "UTI",
            Nakshatras.REVATHI: "REV",
        }

        return cast("NakshatraCode", nakshatra_codes[self])

    @staticmethod
    def from_code(code: NakshatraCode) -> "Nakshatras":
        """Convert a Nakshatra code to its corresponding enum member.

        Args:
            code (NakshatraCode): The Nakshatra code.

        Returns:
            Nakshatras: The corresponding enum member.

        """
        code_to_nakshatra = {
            "ASW": Nakshatras.ASWINNI,
            "BHA": Nakshatras.BHARANI,
            "KAA": Nakshatras.KAARTHIKAI,
            "ROG": Nakshatras.ROGHINI,
            "MIR": Nakshatras.MIRUGASIRISAM,
            "THI": Nakshatras.THIRUVAATHIRAI,
            "PUN": Nakshatras.PUNARPOOSAM,
            "POO": Nakshatras.POOSAM,
            "AAY": Nakshatras.AAYILYAM,
            "MAG": Nakshatras.MAGAM,
            "PRM": Nakshatras.POORAM,
            "UTH": Nakshatras.UTHTHIRAM,
            "AST": Nakshatras.ASTHTHAM,
            "CHI": Nakshatras.CHITHTHIRAI,
            "SUV": Nakshatras.SUVAATHI,
            "VIS": Nakshatras.VISAAGAM,
            "ANU": Nakshatras.ANUSHAM,
            "KET": Nakshatras.KETTAI,
            "MOO": Nakshatras.MOOLAM,
            "PDM": Nakshatras.POORAADAM,
            "UTD": Nakshatras.UTHTHIRAADAM,
            "TVO": Nakshatras.THIRUVONAM,
            "AVI": Nakshatras.AVITTAM,
            "SHA": Nakshatras.SHATHAYAM,
            "PRI": Nakshatras.POORATTAATHI,
            "UTI": Nakshatras.UTHTHIRATTAATHI,
            "REV": Nakshatras.REVATHI,
        }

        return code_to_nakshatra[code]

    @staticmethod
    def to_string(num: int) -> str:
        """Convert star number to display name of the star.

        Args:
            num (int): the star number

        Returns:
            str: return the star name

        """
        return Nakshatras(num).name

    @staticmethod
    def to_list() -> list[str]:
        """Convert enum to list of enum item name.

        Returns:
            list[str]: list of enum item name

        """
        return [el.name for el in Nakshatras]
