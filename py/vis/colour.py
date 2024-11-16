"""Enum of singular colours and colour schemes"""

from enum import Enum
from enum import unique


@unique
class Colour(Enum):
    AccentBlue = "#0148A4"
    AccentGrey = "#F1F1F1"
    AccentYellow = "#FFB800"
    MasterbrandBlack = "#0A0A0A"
    MasterbrandCharcoal = "#424242"
    MasterbrandOchre = "#E64626"
    MasterbrandWhite = "#FFFFFF"
    SecondaryBeige = "#FDCA90"
    SecondaryBlue = "#4E98D3"
    SecondaryDarkGreen = "#007E3B"
    SecondaryDarkSeafoam = "#00A485"
    SecondaryIvory = "#F8EFDD"
    SecondaryLemon = "#FBF38D"
    SecondaryLightBlue = "#91BDE5"
    SecondaryLightGreen = "#BDDC96"
    SecondaryLightPink = "#F8B9CC"
    SecondaryLightSeafoam = "#68C6B6"
    SecondaryLilac = "#B896C6"
    SecondaryMaroon = "#7A2000"
    SecondaryOrange = "#F9A134"
    SecondaryPeach = "#F79C72"
    SecondaryPink = "#D6519D"
    SecondaryPurple = "#7F3F98"
    RainbowRed = "#D81E31"
    RainbowDarkBlue = "#1B639D"
    RainbowBlack = "#000000"
    RainbowGreen = "#008000"
    RainbowLightBlue = "#02A9E2"
    RainbowYellow = "#FBC20D"
    RainbowGrey = "#595959"

    def __repr__(self):
        return repr(self.value)


@unique
class ColourScheme(Enum):
    """Colour schemes for visualisation. Format: Key | Number of colours

    <https://github.com/Sydney-Informatics-Hub/usydColours> & Rainbow is from GraphGood.m
    """

    Rainbow = (
        Colour.RainbowRed.value,
        Colour.RainbowDarkBlue.value,
        Colour.RainbowBlack.value,
        Colour.RainbowGreen.value,
        Colour.RainbowLightBlue.value,
        Colour.RainbowYellow.value,
        Colour.RainbowGrey.value,
    )
    Primary = (
        Colour.MasterbrandCharcoal.value,
        Colour.MasterbrandOchre.value,
        Colour.AccentBlue.value,
        Colour.AccentYellow.value,
        Colour.AccentGrey.value,
    )
    Extended = (
        Colour.MasterbrandCharcoal.value,
        Colour.MasterbrandOchre.value,
        Colour.AccentBlue.value,
        Colour.AccentYellow.value,
        Colour.SecondaryDarkGreen.value,
        Colour.SecondaryBlue.value,
        Colour.SecondaryPeach.value,
        Colour.SecondaryBeige.value,
        Colour.SecondaryLemon.value,
        Colour.SecondaryLightGreen.value,
        Colour.SecondaryDarkSeafoam.value,
        Colour.SecondaryLightSeafoam.value,
        Colour.SecondaryLightBlue.value,
        Colour.SecondaryLilac.value,
        Colour.SecondaryPurple.value,
        Colour.SecondaryPink.value,
        Colour.SecondaryLightPink.value,
        Colour.SecondaryOrange.value,
        Colour.SecondaryMaroon.value,
        Colour.MasterbrandBlack.value,
        Colour.AccentGrey.value,
    )
    Secondary = (
        Colour.MasterbrandOchre.value,
        Colour.SecondaryBlue.value,
        Colour.AccentYellow.value,
        Colour.SecondaryDarkSeafoam.value,
        Colour.SecondaryLilac.value,
    )
    Pastel = (
        Colour.SecondaryLemon.value,
        Colour.SecondaryPeach.value,
        Colour.SecondaryLightPink.value,
        Colour.SecondaryLilac.value,
        Colour.SecondaryLightBlue.value,
        Colour.SecondaryLightSeafoam.value,
        Colour.SecondaryLightGreen.value,
    )
    Complementary_ReGr = (
        Colour.MasterbrandOchre.value,
        Colour.SecondaryPeach.value,
        Colour.SecondaryMaroon.value,
        Colour.SecondaryDarkSeafoam.value,
        Colour.SecondaryLightSeafoam.value,
    )
    Complementary_ReBl = (
        Colour.MasterbrandOchre.value,
        Colour.SecondaryPeach.value,
        Colour.SecondaryBeige.value,
        Colour.AccentBlue.value,
        Colour.SecondaryBlue.value,
        Colour.SecondaryLightBlue.value,
    )
    Bright = (
        Colour.MasterbrandOchre.value,
        Colour.SecondaryDarkGreen.value,
        Colour.SecondaryLightGreen.value,
        Colour.SecondaryLightBlue.value,
        Colour.SecondaryBlue.value,
        Colour.SecondaryOrange.value,
        Colour.AccentYellow.value,
    )
    Muted = (
        Colour.SecondaryLightBlue.value,
        Colour.SecondaryLemon.value,
        Colour.SecondaryPeach.value,
    )
    TrafficLight = (
        Colour.SecondaryDarkSeafoam.value,
        Colour.SecondaryLemon.value,
        Colour.MasterbrandOchre.value,
    )
    Heatmap = (
        Colour.SecondaryDarkSeafoam.value,
        Colour.MasterbrandWhite.value,
        Colour.MasterbrandOchre.value,
    )
    FlameTree = (
        Colour.SecondaryLemon.value,
        Colour.SecondaryOrange.value,
        Colour.MasterbrandOchre.value,
        Colour.SecondaryMaroon.value,
    )
    Jacaranda = (
        Colour.SecondaryLightPink.value,
        Colour.SecondaryLilac.value,
        Colour.SecondaryBlue.value,
        Colour.AccentBlue.value,
    )
    Harbour = (
        Colour.SecondaryLightGreen.value,
        Colour.SecondaryLightSeafoam.value,
        Colour.SecondaryBlue.value,
        Colour.AccentBlue.value,
    )
    Sandstone = (
        Colour.SecondaryIvory.value,
        Colour.SecondaryBeige.value,
        Colour.SecondaryMaroon.value,
        Colour.MasterbrandCharcoal.value,
    )
    Ochre = (
        Colour.SecondaryIvory.value,
        Colour.SecondaryBeige.value,
        Colour.SecondaryPeach.value,
        Colour.MasterbrandOchre.value,
    )
    Greyscale = (Colour.MasterbrandCharcoal.value, Colour.AccentGrey.value)
    BlGrYe = (
        Colour.AccentBlue.value,
        Colour.SecondaryLightGreen.value,
        Colour.SecondaryLemon.value,
    )
    BlOr = (
        Colour.AccentBlue.value,
        Colour.SecondaryOrange.value,
        Colour.SecondaryLemon.value,
    )
    DivergingBlueRed = (
        Colour.SecondaryMaroon.value,
        Colour.MasterbrandOchre.value,
        Colour.SecondaryPeach.value,
        Colour.MasterbrandWhite.value,
        Colour.SecondaryLightBlue.value,
        Colour.SecondaryBlue.value,
        Colour.AccentBlue.value,
    )
    DivergingBlueOrange = (
        Colour.SecondaryOrange.value,
        Colour.MasterbrandWhite.value,
        Colour.AccentBlue.value,
    )
