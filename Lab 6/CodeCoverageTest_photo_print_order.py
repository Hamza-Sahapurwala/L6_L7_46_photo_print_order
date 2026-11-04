import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------
def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0

def test_unknown_size():
    with pytest.raises(ValueError):
        extra_print_charge("3x3", 5, "matte", False)

def test_negative_copies():
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)

def test_member_bonus_within_included():
    # included 20 + 5 = 25 -> no extra
    assert extra_print_charge("4x6", 25, "matte", True) == 0

def test_matte_extra():
    assert extra_print_charge("4x6", 25, "matte", False) == 5 * 4

def test_glossy_extra():
    assert extra_print_charge("4x6", 25, "glossy", False) == 5 * 7

def test_matte_bulk_surcharge():
    # extra 55 > 50 -> rate 4 + 2 = 6
    assert extra_print_charge("4x6", 75, "matte", False) == 55 * 6

def test_canvas_bulk_surcharge():
    # rate 7 + 2 + 5 = 14
    assert extra_print_charge("4x6", 75, "canvas", False) == 55 * 14


# ---------- order_valid ----------
def test_order_valid():
    assert order_valid(10, 100, False) is True

def test_rush_valid():
    assert order_valid(10, 50, True) is True

def test_file_too_large():
    assert order_valid(30, 10, False) is False


# ---------- dispatch_status ----------
def test_dispatch_on_time():
    assert dispatch_status(24, True, False) == "on_time"

def test_dispatch_tight():
    assert dispatch_status(6, False, False) == "tight"

def test_dispatch_missed():
    assert dispatch_status(5, False, False) == "missed"

def test_dispatch_international():
    assert dispatch_status(36, False, True) == "on_time"