"""
Code Coverage Test Suite for Train Fare Application
Student SRN: PES1UG24CS448
Assignment: Lab 6 / Lab 7 - Software Engineering
Module Under Test: train_fare.py
"""

import pytest
from train_fare import base_fare, concession, tatkal_charge, RATE_PER_KM


# ============================================================================
# 1. Base Fare Statement & Code Coverage Tests
# ============================================================================

def test_base_fare_valid_classes_nominal():
    """Verify base fare calculations across all valid travel classes."""
    assert base_fare("SL", 100) == 100  # Rate: 1 -> 100
    assert base_fare("3A", 100) == 200  # Rate: 2 -> 200
    assert base_fare("2A", 100) == 300  # Rate: 3 -> 300
    assert base_fare("1A", 100) == 500  # Rate: 5 -> 500


def test_base_fare_minimum_fare_cap():
    """Verify line coverage for minimum fare clamping to 50 INR."""
    assert base_fare("SL", 20) == 50   # 1 * 20 = 20 < 50 -> capped to 50
    assert base_fare("3A", 15) == 50   # 2 * 15 = 30 < 50 -> capped to 50


def test_base_fare_invalid_class_raises_exception():
    """Verify exception handling when an unknown travel class is provided."""
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("INVALID_CLASS", 100)

    with pytest.raises(ValueError, match="unknown class"):
        base_fare("", 100)


def test_base_fare_invalid_distance_raises_exception():
    """Verify exception handling when distance is zero or negative."""
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)

    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", -50)


# ============================================================================
# 2. Concession Statement & Code Coverage Tests
# ============================================================================

def test_concession_tatkal_ticket():
    """Verify that Tatkal tickets yield zero concession regardless of passenger profile."""
    assert concession(25, "M", True) == 0
    assert concession(4, "F", True) == 0
    assert concession(68, "F", True) == 0


def test_concession_infant_passenger():
    """Verify 100% concession for infants below 5 years old."""
    assert concession(0, "M", False) == 100
    assert concession(4, "F", False) == 100


def test_concession_child_passenger():
    """Verify 50% concession for children between 5 and 12 years old."""
    assert concession(5, "M", False) == 50
    assert concession(10, "F", False) == 50
    assert concession(12, "M", False) == 50


def test_concession_senior_female_passenger():
    """Verify 50% concession for female senior citizens (age >= 60)."""
    assert concession(60, "F", False) == 50
    assert concession(75, "F", False) == 50


def test_concession_senior_male_passenger():
    """Verify 40% concession for male/other senior citizens (age >= 60)."""
    assert concession(60, "M", False) == 40
    assert concession(80, "M", False) == 40
    assert concession(65, "Other", False) == 40


def test_concession_adult_passenger():
    """Verify 0% concession for regular adults between 13 and 59."""
    assert concession(13, "M", False) == 0
    assert concession(30, "F", False) == 0
    assert concession(59, "M", False) == 0


# ============================================================================
# 3. Tatkal Charge Statement & Code Coverage Tests
# ============================================================================

def test_tatkal_charge_sleeper_min_cap():
    """Verify Tatkal charge lower bound (100 INR) for Sleeper class."""
    # 500 // 10 = 50 < 100 -> capped to 100
    assert tatkal_charge("SL", 500) == 100


def test_tatkal_charge_sleeper_nominal():
    """Verify nominal Tatkal charge calculation for Sleeper class."""
    # 2500 // 10 = 250 (between 100 and 400)
    assert tatkal_charge("SL", 2500) == 250


def test_tatkal_charge_sleeper_max_cap():
    """Verify Tatkal charge upper bound (400 INR) for Sleeper class."""
    # 5000 // 10 = 500 > 400 -> capped to 400
    assert tatkal_charge("SL", 5000) == 400


def test_tatkal_charge_ac_min_cap():
    """Verify Tatkal charge lower bound (100 INR) for AC classes."""
    # 200 * 3 // 10 = 60 < 100 -> capped to 100
    assert tatkal_charge("3A", 200) == 100


def test_tatkal_charge_ac_nominal():
    """Verify nominal Tatkal charge calculation for AC classes."""
    # 1000 * 3 // 10 = 300 (between 100 and 400)
    assert tatkal_charge("2A", 1000) == 300


def test_tatkal_charge_ac_max_cap():
    """Verify Tatkal charge upper bound (400 INR) for AC classes."""
    # 2000 * 3 // 10 = 600 > 400 -> capped to 400
    assert tatkal_charge("1A", 2000) == 400
