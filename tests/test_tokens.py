"""U-10 色票、U-11 字體清單的驗證規則（FR-11、FR-12）。"""
import copy

import pytest

from app.tokens import ROLES, validate_fonts, validate_palette

GOOD = {
    "id": "sample-night",
    "name": "範例夜色",
    "kind": "dark",
    "colors": {
        "bg": "#0b0f17",
        "surface": "#1c2333",
        "ink": "#f7f3ea",
        "muted": "#9aa3b2",
        "accent": "#e8b04b",
        "accent2": "#f2c879",
        "deep": "#05070c",
    },
}


def test_u10_good_palette_has_no_errors():
    assert validate_palette(GOOD) == []


def test_u10_palette_needs_exactly_seven_roles():
    assert len(ROLES) == 7
    p = copy.deepcopy(GOOD)
    del p["colors"]["deep"]
    assert any("deep" in e for e in validate_palette(p))


def test_u10_unknown_role_is_rejected():
    p = copy.deepcopy(GOOD)
    p["colors"]["sparkle"] = "#ffffff"
    assert any("sparkle" in e for e in validate_palette(p))


def test_u10_low_text_contrast_is_rejected():
    p = copy.deepcopy(GOOD)
    p["colors"]["ink"] = "#2a3040"
    assert any("ink/bg" in e for e in validate_palette(p))


def test_u10_low_muted_contrast_is_rejected():
    p = copy.deepcopy(GOOD)
    p["colors"]["muted"] = "#3a4050"
    assert any("muted/bg" in e for e in validate_palette(p))


def font(i, license="OFL-1.1"):
    return {"id": f"font-{i}", "family": f"Font {i}", "license": license, "weights": [400]}


def test_u11_ten_open_fonts_pass():
    assert validate_fonts([font(i) for i in range(10)]) == []


def test_u11_fewer_than_ten_fonts_fail():
    assert any("10" in e for e in validate_fonts([font(i) for i in range(9)]))


def test_u11_font_without_allowed_license_fails():
    fonts = [font(i) for i in range(10)]
    fonts[3] = font(3, license="Proprietary")
    assert any("font-3" in e for e in validate_fonts(fonts))


def test_u11_duplicate_font_ids_fail():
    fonts = [font(i) for i in range(10)]
    fonts[9]["id"] = "font-0"
    assert any("font-0" in e for e in validate_fonts(fonts))


@pytest.mark.parametrize("lic", ["OFL-1.1", "Apache-2.0", "TW-OGDL-1.0"])
def test_u11_allowed_licenses(lic):
    assert validate_fonts([font(i, lic) for i in range(10)]) == []
