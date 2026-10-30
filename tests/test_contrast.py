"""U-09：對比計算要符合 WCAG 2.x 公式。"""
import pytest

from app.contrast import contrast_ratio


def test_u09_black_on_white_is_21():
    assert contrast_ratio("#000000", "#ffffff") == pytest.approx(21.0)


def test_u09_order_does_not_matter():
    assert contrast_ratio("#777777", "#ffffff") == contrast_ratio("#ffffff", "#777777")


def test_u09_known_grey_value():
    # #777777 on white is the textbook "just below 4.5:1" case.
    assert contrast_ratio("#777777", "#ffffff") == pytest.approx(4.48, abs=0.01)


def test_u09_short_hex_is_accepted():
    assert contrast_ratio("#000", "#fff") == pytest.approx(21.0)


def test_u09_rejects_bad_hex():
    with pytest.raises(ValueError):
        contrast_ratio("red", "#fff")
