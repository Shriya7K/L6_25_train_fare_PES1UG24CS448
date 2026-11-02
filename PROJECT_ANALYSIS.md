# Initial Project Analysis: Train Fare System (Lab 6 & Lab 7)

## 1. Project Overview
The Train Fare System is a Python module developed for Indian Railway-style fare calculation. It computes:
- Base fares based on travel class rates per kilometer and distance, with a minimum fare guarantee.
- Passenger concessions based on age, gender, and ticket booking type (regular vs. Tatkal).
- Tatkal booking surcharge calculation with class-specific percentage rules and minimum/maximum charge capping.

The project is structured under the PES University Software Engineering Lab curriculum (Lab 6 & Lab 7) focusing on white-box testing, statement coverage (code coverage), and branch/decision coverage using `pytest` and `coverage.py`.

---

## 2. Existing Folder Structure
```
L6_L7_25_train_fare/
│
├── .gitignore
├── requirements.txt
├── PROJECT_ANALYSIS.md
└── Lab 6/
    ├── README.md
    ├── train_fare.py          # Application logic under test
    └── test_train_fare.py     # Starter baseline test suite
```

---

## 3. Application Functionality & Specification

The source file `Lab 6/train_fare.py` defines a rate lookup table and three core functions:

### 3.1 Rate Mapping
```python
RATE_PER_KM = {"SL": 1, "3A": 2, "2A": 3, "1A": 5}
```
- Sleeper (`SL`): 1 INR/km
- AC 3 Tier (`3A`): 2 INR/km
- AC 2 Tier (`2A`): 3 INR/km
- AC First Class (`1A`): 5 INR/km

---

## 4. Important Functions and Purpose

### 4.1 `base_fare(travel_class, distance_km)`
- **Purpose**: Computes the baseline ticket cost for a specific class and distance traveled.
- **Validations**:
  - Validates `travel_class` against `RATE_PER_KM`. Raises `ValueError("unknown class")` if invalid.
  - Validates `distance_km > 0`. Raises `ValueError("invalid distance")` if distance is <= 0.
- **Minimum Fare Floor**: If calculated fare is below 50, it is rounded up to the minimum fare of 50.
- **Return Value**: An integer or float representing the computed fare.

### 4.2 `concession(age, gender, is_tatkal)`
- **Purpose**: Determines the discount percentage (0 to 100%) entitled to a passenger.
- **Rules**:
  - If `is_tatkal` is `True`, no concession is allowed; returns `0` immediately.
  - Children under 5 (`age < 5`): Free travel, returns `100` (100% concession).
  - Children between 5 and 12 (`5 <= age <= 12`): Half fare, returns `50` (50% concession).
  - Senior citizens (`age >= 60`):
    - Female passengers (`gender == "F"`): Returns `50` (50% concession).
    - Male and other passengers: Returns `40` (40% concession).
  - Regular adult passengers (`13 <= age < 60`): Returns `0` (no concession).

### 4.3 `tatkal_charge(travel_class, fare)`
- **Purpose**: Calculates additional Tatkal premium charges based on travel class and base fare.
- **Rules**:
  - Sleeper (`travel_class == "SL"`): Rate is 10% of fare (`fare // 10`).
  - AC classes (`travel_class != "SL"`): Rate is 30% of fare (`fare * 3 // 10`).
  - Cap limits:
    - Maximum Tatkal charge: 400 (`charge > 400` capped to 400).
    - Minimum Tatkal charge: 100 (`charge < 100` capped to 100).
- **Return Value**: Integer Tatkal charge between 100 and 400.

---

## 5. Conditional Statements and Decision Branches

| Function | Line(s) | Decision Point / Condition | True Outcome | False Outcome |
| :--- | :--- | :--- | :--- | :--- |
| `base_fare` | 5 | `travel_class not in RATE_PER_KM` | Raises `ValueError("unknown class")` | Proceeds to distance check |
| `base_fare` | 7 | `distance_km <= 0` | Raises `ValueError("invalid distance")` | Proceeds to calculate fare |
| `base_fare` | 10 | `fare < 50` | `fare = 50` (capped to floor) | Returns unmodified `fare` |
| `concession` | 16 | `is_tatkal` | Returns `0` | Proceeds to age evaluation |
| `concession` | 18 | `age < 5` | Returns `100` | Evaluates next condition |
| `concession` | 20 | `age <= 12` | Returns `50` | Evaluates next condition |
| `concession` | 22 | `age >= 60` | Evaluates gender condition | Returns `0` (adult 13-59) |
| `concession` | 23 | `gender == "F"` | Returns `50` | Returns `40` |
| `tatkal_charge` | 30 | `travel_class == "SL"` | `charge = fare // 10` | `charge = fare * 3 // 10` |
| `tatkal_charge` | 34 | `charge > 400` | `charge = 400` (upper cap) | Evaluates lower cap check |
| `tatkal_charge` | 36 | `charge < 100` | `charge = 100` (lower cap) | Returns raw `charge` |

Total Decision Points: **11**
Total Binary Branches: **22**

---

## 6. Baseline Coverage Analysis
Initial execution using `test_train_fare.py` (which only contains 2 tests: `test_sleeper_fare` and `test_adult_no_concession`):
- **Statements**: 31 total in `train_fare.py`
- **Missing Statements**: 17 (Lines 6, 8, 11, 17, 19, 21, 23-25, 30-38)
- **Line Coverage**: 45%
- **Branch Coverage**: 40% (7 partial branches, remaining untouched)
- Untested areas:
  - Error handling for invalid class and negative/zero distance.
  - Base fare minimum capping below 50.
  - Tatkal concession bypass.
  - Child and senior citizen concession brackets.
  - Entire `tatkal_charge` function (all classes and clamping boundaries).

---

## 7. Potential Edge Cases & Boundary Values

1. **`base_fare`**:
   - Boundary distances: `0`, `-1`, `-0.01`, `1`, `49`, `50`, `51`.
   - Low distance triggering floor fare: `distance_km = 10` in `SL` (1 * 10 = 10 -> 50).
   - Exact threshold distance: `distance_km = 50` in `SL` (1 * 50 = 50 -> 50).
   - Higher distance: `distance_km = 100` in `SL` (100 -> 100).
   - Unknown classes: `"3E"`, `"General"`, `""`, `None`, `"AC"`.
   - Valid classes: `"SL"`, `"3A"`, `"2A"`, `"1A"`.

2. **`concession`**:
   - `is_tatkal = True` with age `3` (should be 0 despite age < 5).
   - `is_tatkal = True` with age `65` (should be 0 despite age >= 60).
   - Age boundaries:
     - `age = 4`: Infant (100%).
     - `age = 5`: Child lower boundary (50%).
     - `age = 12`: Child upper boundary (50%).
     - `age = 13`: Adult lower boundary (0%).
     - `age = 59`: Adult upper boundary (0%).
     - `age = 60`: Senior citizen lower boundary (50% for `F`, 40% for `M`).
     - `age = 80`: Senior citizen (50% for `F`, 40% for `M`).
     - Gender variations: `"F"` vs `"M"`, `"Other"`.

3. **`tatkal_charge`**:
   - Sleeper (`SL`):
     - `fare = 500`: `500 // 10 = 50 < 100` -> capped to `100`.
     - `fare = 1000`: `1000 // 10 = 100` -> exactly `100`.
     - `fare = 2500`: `2500 // 10 = 250` -> in range `250`.
     - `fare = 4000`: `4000 // 10 = 400` -> exactly `400`.
     - `fare = 5000`: `5000 // 10 = 500 > 400` -> capped to `400`.
   - Non-Sleeper (`3A`, `2A`, `1A`):
     - `fare = 200`: `200 * 3 // 10 = 60 < 100` -> capped to `100`.
     - `fare = 334`: `334 * 3 // 10 = 100` -> exactly `100`.
     - `fare = 1000`: `1000 * 3 // 10 = 300` -> in range `300`.
     - `fare = 1334`: `1334 * 3 // 10 = 400` -> exactly `400`.
     - `fare = 2000`: `2000 * 3 // 10 = 600 > 400` -> capped to `400`.

---

## 8. Dependencies and Setup Requirements
- Python 3.10+ (Current environment: Python 3.14.8)
- `pytest` (Testing framework)
- `coverage` (Coverage instrumentation engine)
- Execution Commands:
  - Statement Coverage: `coverage run -m pytest` followed by `coverage report -m`
  - Branch Coverage: `coverage run --branch -m pytest` followed by `coverage report -m`
