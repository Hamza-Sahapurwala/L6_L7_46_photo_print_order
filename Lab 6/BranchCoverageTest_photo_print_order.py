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

# ---------- extra branch tests: extra_print_charge ----------
def test_member_8x10_gets_no_bonus():
    # included stays 10 -> extra 2
    assert extra_print_charge("8x10", 12, "matte", True) == 2 * 4

def test_member_5x7_bonus():
    assert extra_print_charge("5x7", 20, "matte", True) == 0
    assert extra_print_charge("5x7", 21, "matte", True) == 4

def test_zero_copies():
    assert extra_print_charge("4x6", 0, "matte", False) == 0

def test_exactly_at_included_limit():
    assert extra_print_charge("4x6", 20, "glossy", False) == 0

def test_extra_exactly_50_no_surcharge():
    assert extra_print_charge("4x6", 70, "matte", False) == 50 * 4

def test_extra_51_has_surcharge():
    assert extra_print_charge("4x6", 71, "matte", False) == 51 * 6

def test_canvas_extra_50_no_surcharge():
    assert extra_print_charge("4x6", 70, "canvas", False) == 50 * 7

def test_glossy_bulk_no_canvas_extra():
    assert extra_print_charge("4x6", 75, "glossy", False) == 55 * 9


# ---------- extra branch tests: order_valid ----------
def test_rush_too_many_copies():
    assert order_valid(10, 51, True) is False

def test_rush_ignores_file_size():
    assert order_valid(30, 10, True) is True

def test_file_exactly_25():
    assert order_valid(25, 10, False) is True

def test_copies_exactly_500():
    assert order_valid(10, 500, False) is True

def test_copies_501():
    assert order_valid(10, 501, False) is False


# ---------- extra branch tests: dispatch_status ----------
def test_framed_tight_boundary():
    assert dispatch_status(18, True, False) == "tight"

def test_framed_missed():
    assert dispatch_status(17, True, False) == "missed"

def test_unframed_on_time_boundary():
    assert dispatch_status(12, False, False) == "on_time"

def test_international_tight():
    assert dispatch_status(30, False, True) == "tight"

def test_international_missed():
    assert dispatch_status(29, False, True) == "missed"

def test_framed_international_on_time():
    assert dispatch_status(48, True, True) == "on_time"