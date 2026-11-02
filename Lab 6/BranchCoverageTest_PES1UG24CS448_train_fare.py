"""
Branch Coverage Test Suite for Train Fare Application
Student SRN: PES1UG24CS448
Assignment: Lab 6 / Lab 7 - Software Engineering
Module Under Test: train_fare.py

This test suite comprehensively exercises every decision branch (True/False)
in `train_fare.py` to achieve 100% Branch Coverage.
"""

import pytest
from train_fare import base_fare, concession, tatkal_charge


# ============================================================================
# 1. Base Fare Branch Coverage Tests
# ============================================================================

class TestBaseFareBranches:
    """
    Branch Analysis for `base_fare(travel_class, distance_km)`:
    - Decision 1: `travel_class not in RATE_PER_KM`
        - Branch 1A (True): Unknown class -> raises ValueError("unknown class")
        - Branch 1B (False): Known class -> proceeds to Decision 2
    - Decision 2: `distance_km <= 0`
        - Branch 2A (True): Distance <= 0 -> raises ValueError("invalid distance")
        - Branch 2B (False): Distance > 0 -> proceeds to compute fare
    - Decision 3: `fare < 50`
        - Branch 3A (True): Fare < 50 -> clamped to 50
        - Branch 3B (False): Fare >= 50 -> retains calculated fare
    """

    def test_branch_unknown_class_true(self):
        """Branch 1A (True): Invalid travel class."""
        with pytest.raises(ValueError, match="unknown class"):
            base_fare("NON_EXISTENT", 100)

        with pytest.raises(ValueError, match="unknown class"):
            base_fare("", 100)

        with pytest.raises(ValueError, match="unknown class"):
            base_fare("3E", 100)

    def test_branch_unknown_class_false_all_classes(self):
        """Branch 1B (False): Valid travel class (all 4 valid classes tested)."""
        assert base_fare("SL", 100) == 100
        assert base_fare("3A", 100) == 200
        assert base_fare("2A", 100) == 300
        assert base_fare("1A", 100) == 500

    def test_branch_invalid_distance_true_zero(self):
        """Branch 2A (True - Zero): Distance == 0."""
        with pytest.raises(ValueError, match="invalid distance"):
            base_fare("SL", 0)

    def test_branch_invalid_distance_true_negative(self):
        """Branch 2A (True - Negative): Distance < 0."""
        with pytest.raises(ValueError, match="invalid distance"):
            base_fare("SL", -1)

        with pytest.raises(ValueError, match="invalid distance"):
            base_fare("1A", -100.5)

    def test_branch_distance_valid_false(self):
        """Branch 2B (False): Distance > 0."""
        assert base_fare("SL", 80) == 80

    def test_branch_fare_below_minimum_true(self):
        """Branch 3A (True): fare < 50 triggers minimum floor."""
        # 1 * 10 = 10 < 50 -> 50
        assert base_fare("SL", 10) == 50
        # 2 * 20 = 40 < 50 -> 50
        assert base_fare("3A", 20) == 50
        # 5 * 5 = 25 < 50 -> 50
        assert base_fare("1A", 5) == 50

    def test_branch_fare_below_minimum_false_boundary_50(self):
        """Branch 3B (False - Exact Boundary): fare == 50 (not < 50)."""
        # 1 * 50 = 50 -> not < 50 -> 50
        assert base_fare("SL", 50) == 50
        # 2 * 25 = 50 -> not < 50 -> 50
        assert base_fare("3A", 25) == 50

    def test_branch_fare_below_minimum_false_above_50(self):
        """Branch 3B (False - Above): fare > 50."""
        # 1 * 51 = 51 -> 51
        assert base_fare("SL", 51) == 51
        # 3 * 100 = 300 -> 300
        assert base_fare("2A", 100) == 300


# ============================================================================
# 2. Concession Branch Coverage Tests
# ============================================================================

class TestConcessionBranches:
    """
    Branch Analysis for `concession(age, gender, is_tatkal)`:
    - Decision 4: `if is_tatkal:`
        - Branch 4A (True): Tatkal booking -> return 0
        - Branch 4B (False): Non-tatkal -> proceed to age checks
    - Decision 5: `if age < 5:`
        - Branch 5A (True): Infant (<5) -> return 100
        - Branch 5B (False): age >= 5 -> evaluate Decision 6
    - Decision 6: `elif age <= 12:`
        - Branch 6A (True): Child (5 to 12) -> return 50
        - Branch 6B (False): age > 12 -> evaluate Decision 7
    - Decision 7: `elif age >= 60:`
        - Branch 7A (True): Senior (>= 60) -> evaluate Decision 8
        - Branch 7B (False): Regular adult (13 to 59) -> return 0
    - Decision 8: `if gender == "F":`
        - Branch 8A (True): Female senior -> return 50
        - Branch 8B (False): Non-female senior -> return 40
    """

    def test_branch_is_tatkal_true(self):
        """Branch 4A (True): Tatkal bookings always get 0% concession."""
        assert concession(2, "F", True) == 0    # Infant under Tatkal
        assert concession(10, "M", True) == 0   # Child under Tatkal
        assert concession(30, "F", True) == 0   # Adult under Tatkal
        assert concession(65, "F", True) == 0   # Senior female under Tatkal
        assert concession(70, "M", True) == 0   # Senior male under Tatkal

    def test_branch_is_tatkal_false_infant_true(self):
        """Branch 4B (False) & Branch 5A (True): Non-Tatkal infant age < 5."""
        assert concession(0, "M", False) == 100  # Lower boundary
        assert concession(2, "F", False) == 100  # Mid value
        assert concession(4, "M", False) == 100  # Boundary just below 5

    def test_branch_age_child_true_boundary_5(self):
        """Branch 5B (False) & Branch 6A (True): Lower boundary age == 5."""
        assert concession(5, "M", False) == 50

    def test_branch_age_child_true_nominal_and_upper_boundary(self):
        """Branch 6A (True): Child nominal (8) and upper boundary (12)."""
        assert concession(8, "F", False) == 50
        assert concession(12, "M", False) == 50

    def test_branch_age_child_false_regular_adult(self):
        """Branch 6B (False) & Branch 7B (False): Adult between 13 and 59."""
        assert concession(13, "M", False) == 0  # Lower adult boundary
        assert concession(35, "F", False) == 0  # Nominal adult
        assert concession(59, "M", False) == 0  # Upper adult boundary

    def test_branch_age_senior_true_female_true_boundary_60(self):
        """Branch 7A (True) & Branch 8A (True): Senior female boundary age == 60."""
        assert concession(60, "F", False) == 50

    def test_branch_age_senior_true_female_true_nominal_75(self):
        """Branch 7A (True) & Branch 8A (True): Senior female nominal age == 75."""
        assert concession(75, "F", False) == 50

    def test_branch_age_senior_true_female_false_male(self):
        """Branch 7A (True) & Branch 8B (False): Senior male boundary 60 and nominal 70."""
        assert concession(60, "M", False) == 40
        assert concession(70, "M", False) == 40

    def test_branch_age_senior_true_female_false_other_gender(self):
        """Branch 7A (True) & Branch 8B (False): Senior non-female non-male."""
        assert concession(65, "Other", False) == 40
        assert concession(65, "", False) == 40


# ============================================================================
# 3. Tatkal Charge Branch Coverage Tests
# ============================================================================

class TestTatkalChargeBranches:
    """
    Branch Analysis for `tatkal_charge(travel_class, fare)`:
    - Decision 9: `if travel_class == "SL":`
        - Branch 9A (True): Sleeper class -> charge = fare // 10
        - Branch 9B (False): Non-Sleeper class -> charge = fare * 3 // 10
    - Decision 10: `if charge > 400:`
        - Branch 10A (True): charge > 400 -> charge = 400
        - Branch 10B (False): charge <= 400 -> evaluate Decision 11
    - Decision 11: `elif charge < 100:`
        - Branch 11A (True): charge < 100 -> charge = 100
        - Branch 11B (False): charge >= 100 (in [100, 400]) -> returns charge
    """

    def test_branch_sl_min_charge_clamped(self):
        """Branch 9A (True), Branch 10B (False), Branch 11A (True): SL charge < 100."""
        # fare = 500 -> 500 // 10 = 50 < 100 -> capped to 100
        assert tatkal_charge("SL", 500) == 100
        # fare = 990 -> 990 // 10 = 99 < 100 -> capped to 100
        assert tatkal_charge("SL", 990) == 100

    def test_branch_sl_min_charge_boundary_100(self):
        """Branch 9A (True), Branch 10B (False), Branch 11B (False): SL charge == 100."""
        # fare = 1000 -> 1000 // 10 = 100 -> not < 100 -> returns 100
        assert tatkal_charge("SL", 1000) == 100

    def test_branch_sl_nominal_charge(self):
        """Branch 9A (True), Branch 10B (False), Branch 11B (False): SL charge nominal."""
        # fare = 2500 -> 2500 // 10 = 250
        assert tatkal_charge("SL", 2500) == 250

    def test_branch_sl_max_charge_boundary_400(self):
        """Branch 9A (True), Branch 10B (False), Branch 11B (False): SL charge == 400."""
        # fare = 4000 -> 4000 // 10 = 400 -> not > 400 -> returns 400
        assert tatkal_charge("SL", 4000) == 400

    def test_branch_sl_max_charge_clamped(self):
        """Branch 9A (True), Branch 10A (True): SL charge > 400 capped to 400."""
        # fare = 4010 -> 4010 // 10 = 401 > 400 -> capped to 400
        assert tatkal_charge("SL", 4010) == 400
        # fare = 6000 -> 6000 // 10 = 600 > 400 -> capped to 400
        assert tatkal_charge("SL", 6000) == 400

    def test_branch_ac_min_charge_clamped(self):
        """Branch 9B (False), Branch 10B (False), Branch 11A (True): AC charge < 100."""
        # fare = 200 -> 200 * 3 // 10 = 60 < 100 -> capped to 100
        assert tatkal_charge("3A", 200) == 100
        # fare = 330 -> 330 * 3 // 10 = 99 < 100 -> capped to 100
        assert tatkal_charge("2A", 330) == 100

    def test_branch_ac_min_charge_boundary_100(self):
        """Branch 9B (False), Branch 10B (False), Branch 11B (False): AC charge == 100."""
        # fare = 334 -> 334 * 3 // 10 = 100 -> not < 100 -> returns 100
        assert tatkal_charge("3A", 334) == 100

    def test_branch_ac_nominal_charge(self):
        """Branch 9B (False), Branch 10B (False), Branch 11B (False): AC charge nominal."""
        # fare = 1000 -> 1000 * 3 // 10 = 300
        assert tatkal_charge("2A", 1000) == 300

    def test_branch_ac_max_charge_boundary_400(self):
        """Branch 9B (False), Branch 10B (False), Branch 11B (False): AC charge == 400."""
        # fare = 1334 -> 1334 * 3 // 10 = 400 -> not > 400 -> returns 400
        assert tatkal_charge("1A", 1334) == 400

    def test_branch_ac_max_charge_clamped(self):
        """Branch 9B (False), Branch 10A (True): AC charge > 400 capped to 400."""
        # fare = 1340 -> 1340 * 3 // 10 = 402 > 400 -> capped to 400
        assert tatkal_charge("1A", 1340) == 400
        # fare = 2500 -> 2500 * 3 // 10 = 750 > 400 -> capped to 400
        assert tatkal_charge("3A", 2500) == 400
