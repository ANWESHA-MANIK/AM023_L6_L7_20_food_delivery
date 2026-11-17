
import pytest
from hypothesis import given, strategies as st
from food_delivery import parse_order, delivery_eta, coupon_discount


# Valid order fuzz testing

@given(
    st.lists(
        st.tuples(
            st.text(
                alphabet="abcdefghijklmnopqrstuvwxyz",
                min_size=1,
                max_size=10
            ),
            st.integers(min_value=1, max_value=100)
        ),
        min_size=1,
        max_size=10
    )
)
def test_parse_order_valid(items):
    csv = ",".join(f"{name}:{qty}" for name, qty in items)
    result = parse_order(csv)

    assert isinstance(result, dict)
    assert all(qty > 0 for qty in result.values())


# Invalid order fuzz testing

@given(st.one_of(st.none(), st.integers(), st.floats()))
def test_parse_order_invalid_type(value):
    with pytest.raises(ValueError):
        parse_order(value)


@given(st.text())
def test_parse_order_malformed(value):
    try:
        result = parse_order(value)
        assert isinstance(result, dict)
        assert all(qty > 0 for qty in result.values())
    except ValueError:
        pass


# Delivery ETA fuzz testing

@given(
    st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_delivery_eta_valid(distance):
    result = delivery_eta(distance)
    assert result == int(15 + distance * 4)


@given(st.one_of(st.text(), st.none()))
def test_delivery_eta_invalid(value):
    with pytest.raises(ValueError):
        delivery_eta(value)


@given(st.sampled_from(["nan", "inf", "-inf", "-1", "-100"]))
def test_delivery_eta_invalid_numbers(value):
    with pytest.raises(ValueError):
        delivery_eta(value)


# Coupon fuzz testing

@given(st.integers(min_value=0, max_value=100000))
def test_coupon_discount_valid(amount):
    assert coupon_discount(f"SAVE{amount}") == amount


@given(st.text())
def test_coupon_discount_invalid(value):
    if not value.strip().upper().startswith("SAVE"):
        with pytest.raises(ValueError):
            coupon_discount(value)


@given(st.one_of(st.none(), st.integers(), st.floats()))
def test_coupon_discount_invalid_type(value):
    with pytest.raises(ValueError):
        coupon_discount(value)


def test_coupon_discount_malformed():
    for code in ["SAVE", "SAVE-50", "SAVEABC", "SAVE50XYZ", ""]:
        with pytest.raises(ValueError):
            coupon_discount(code)
