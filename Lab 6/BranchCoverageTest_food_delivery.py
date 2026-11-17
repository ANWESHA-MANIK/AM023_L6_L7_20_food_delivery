
import pytest
from food_delivery import (
    delivery_charge,
    apply_coupon,
    estimated_time
)


# Delivery charge: test all decision branches

def test_distance_zero():
    with pytest.raises(ValueError):
        delivery_charge(0, 200, False)


def test_distance_negative():
    with pytest.raises(ValueError):
        delivery_charge(-1, 200, False)


def test_distance_above_limit():
    with pytest.raises(ValueError):
        delivery_charge(16, 200, False)


def test_valid_distance():
    assert delivery_charge(2, 200, False) == 20


def test_free_delivery_condition():
    assert delivery_charge(5, 500, False) == 0


def test_nearby_distance_condition():
    assert delivery_charge(3, 200, False) == 20


def test_medium_distance_condition():
    assert delivery_charge(8, 200, False) == 40


def test_far_distance_condition():
    assert delivery_charge(10, 200, False) == 60


def test_rain_condition_true():
    assert delivery_charge(2, 200, True) == 50


def test_rain_condition_false():
    assert delivery_charge(2, 200, False) == 20


# Coupon: test all decision branches

def test_coupon_none():
    assert apply_coupon(300, None, False) == 300


def test_coupon_invalid():
    with pytest.raises(ValueError):
        apply_coupon(300, "BADCODE", True)


def test_welcome_first_order():
    assert apply_coupon(300, "WELCOME", True) == 200


def test_welcome_not_first_order():
    with pytest.raises(ValueError):
        apply_coupon(300, "WELCOME", False)


def test_order_below_200():
    assert apply_coupon(150, "SAVE50", False) == 150


def test_order_equal_200():
    assert apply_coupon(200, "SAVE50", False) == 150


def test_order_above_200():
    assert apply_coupon(300, "SAVE50", False) == 250


# Estimated time: test all combinations

def test_no_peak_no_busy():
    assert estimated_time(2, False, False) == 23


def test_peak_only():
    assert estimated_time(2, True, False) == 33


def test_busy_only():
    assert estimated_time(2, False, True) == 38


def test_peak_and_busy():
    assert estimated_time(2, True, True) == 53