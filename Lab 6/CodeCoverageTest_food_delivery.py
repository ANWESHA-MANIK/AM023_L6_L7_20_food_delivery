
import pytest
from food_delivery import (
    delivery_charge,
    apply_coupon,
    estimated_time
)


# Delivery charge tests

def test_nearby_small_order():
    assert delivery_charge(2, 200, False) == 20


def test_free_delivery():
    assert delivery_charge(5, 500, False) == 0


def test_rainy_delivery():
    assert delivery_charge(2, 200, True) == 50


def test_medium_distance():
    assert delivery_charge(5, 200, False) == 40


def test_long_distance():
    assert delivery_charge(10, 200, False) == 60


def test_rainy_free_delivery():
    assert delivery_charge(5, 500, True) == 30


def test_invalid_zero_distance():
    with pytest.raises(ValueError):
        delivery_charge(0, 200, False)


def test_invalid_negative_distance():
    with pytest.raises(ValueError):
        delivery_charge(-2, 200, False)


def test_invalid_long_distance():
    with pytest.raises(ValueError):
        delivery_charge(16, 200, False)


# Coupon tests

def test_no_coupon():
    assert apply_coupon(300, None, False) == 300


def test_invalid_coupon():
    with pytest.raises(ValueError):
        apply_coupon(300, "INVALID", True)


def test_welcome_coupon_first_order():
    assert apply_coupon(300, "WELCOME", True) == 200


def test_welcome_coupon_not_first_order():
    with pytest.raises(ValueError):
        apply_coupon(300, "WELCOME", False)


def test_order_below_coupon_limit():
    assert apply_coupon(150, "SAVE50", False) == 150


def test_save50_coupon():
    assert apply_coupon(300, "SAVE50", False) == 250


def test_coupon_at_minimum_order_value():
    assert apply_coupon(200, "SAVE50", False) == 150


# Estimated delivery time tests

def test_normal_delivery_time():
    assert estimated_time(2, False, False) == 23


def test_peak_hour_delivery():
    assert estimated_time(2, True, False) == 33


def test_busy_restaurant():
    assert estimated_time(2, False, True) == 38


def test_peak_and_busy_restaurant():
    assert estimated_time(2, True, True) == 53
