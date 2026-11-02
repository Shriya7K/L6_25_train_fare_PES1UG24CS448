# Software Engineering Lab 6 & Lab 7: Train Fare System — Code & Branch Coverage Analysis

**Student SRN**: PES1UG24CS448  
**Student Name**: Shriya K  
**Course**: Software Engineering (UE24CS252AA)  
**Institution**: PES University  

---

## 1. Project Overview
This repository contains the complete implementation, test suites, coverage reports, and documentation for **Lab 6 & Lab 7: Code and Branch Coverage Analysis**. The target application is an Indian Railway-style fare calculation system that computes ticket base fares by class and distance, applies passenger concessions, and determines Tatkal booking surcharges.

The primary objective of this lab is to demonstrate white-box testing methodologies by measuring, analyzing, and maximizing both **statement/line coverage** and **branch/decision coverage** using Python, `pytest`, and `coverage.py`, surpassing the minimum 90% university requirement to achieve **100% full coverage**.

---

## 2. Technologies Used
- **Programming Language**: Python 3.10+ (Executed on Python 3.14.8)
- **Testing Framework**: `pytest` 9.1.1
- **Coverage Analysis Engine**: `coverage.py` 7.17.0
- **Version Control**: Git & GitHub

---

## 3. Original Application Overview
The application under test is located at `Lab 6/train_fare.py`. It comprises three core functions:

1. `base_fare(travel_class, distance_km)`:
   - Maps classes to rates: Sleeper (`SL`: 1 INR/km), 3-Tier AC (`3A`: 2 INR/km), 2-Tier AC (`2A`: 3 INR/km), 1st AC (`1A`: 5 INR/km).
   - Validates class name and positive distance, raising `ValueError` on invalid inputs.
   - Enforces a minimum base fare floor of 50 INR.

2. `concession(age, gender, is_tatkal)`:
   - Calculates discount percentage based on passenger age, gender, and booking type.
   - Tatkal tickets receive 0% concession (`is_tatkal = True`).
   - Infants (`age < 5`): 100% concession.
   - Children (`5 <= age <= 12`): 50% concession.
   - Senior Citizens (`age >= 60`): 50% for females (`gender == "F"`), 40% for males and other genders.
   - Regular Adults (`13 <= age < 60`): 0% concession.

3. `tatkal_charge(travel_class, fare)`:
   - Calculates Tatkal surcharge: 10% of fare for Sleeper (`SL`), 30% for AC classes.
   - Clamps surcharge between a minimum of 100 INR and a maximum cap of 400 INR.

---

## 4. Installation & Environment Setup

### 4.1 Prerequisites
Ensure Python 3.10 or higher is installed and available in your environment.

### 4.2 Clone the Repository
```bash
git clone https://github.com/Shriya7K/L6_25_train_fare_PES1UG24CS448.git
cd L6_25_train_fare_PES1UG24CS448
```

### 4.3 Install Dependencies
Install the required testing packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 5. How to Execute the Application & Tests

Navigate to the `Lab 6` directory:
```bash
cd "Lab 6"
```

### 5.1 Run All Tests
```bash
pytest -v
```

### 5.2 Run Code Coverage Tests
To execute the statement coverage test suite and view the detailed coverage report:
```bash
coverage run -m pytest CodeCoverageTest_PES1UG24CS448_train_fare.py
coverage report -m
```

### 5.3 Run Branch Coverage Tests
To execute the branch coverage test suite and view branch-level evaluation:
```bash
coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS448_train_fare.py
coverage report -m
```

### 5.4 Run Comprehensive Coverage Across All Suites
```bash
coverage run --branch -m pytest
coverage report -m
```

---

## 6. Coverage Results Summary

| Metric | Target Requirement | Baseline Achieved | Final Achieved | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Code / Line Coverage** | $\ge 90\%$ | 45% | **100%** | **PASSED (EXCEEDED)** |
| **Branch Coverage** | $\ge 90\%$ | 40% | **100%** | **PASSED (EXCEEDED)** |
| **Statements Covered** | - | 14 / 31 | **31 / 31** | **100%** |
| **Branches Covered** | - | 7 / 22 | **22 / 22** | **100%** |
| **Total Test Cases** | - | 2 | **45** | **ALL PASSED** |

---

## 7. Test File Descriptions

| File Path | Description | Test Count |
| :--- | :--- | :---: |
| `Lab 6/test_train_fare.py` | Starter baseline test file provided in the assignment. | 2 |
| `Lab 6/CodeCoverageTest_PES1UG24CS448_train_fare.py` | Dedicated test suite for line/statement coverage testing all functions, valid/invalid inputs, minimum fare floor, exceptions, concession categories, and Tatkal bounds. | 16 |
| `Lab 6/BranchCoverageTest_PES1UG24CS448_train_fare.py` | Dedicated test suite for branch coverage testing every decision point and condition outcome (True and False paths) across boundaries. | 27 |

---

## 8. Screenshot Locations & Evidence

Authentic terminal screenshots showing real command executions and coverage reports are saved in the `evidence/` directory:

1. **Code Coverage Screenshot**:
   - Path: `evidence/code_coverage_result.png`
   - Content: Shows execution of `coverage run -m pytest CodeCoverageTest_PES1UG24CS448_train_fare.py` and `coverage report -m`, verifying 100% statement coverage.

2. **Branch Coverage Screenshot**:
   - Path: `evidence/branch_coverage_result.png`
   - Content: Shows execution of `coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS448_train_fare.py` and `coverage report -m`, verifying 100% branch coverage (22/22 branches).

---

## 9. Repository Structure

```
L6_L7_25_train_fare/
│
├── Lab 6/
│   ├── train_fare.py                                  # Original application under test
│   ├── test_train_fare.py                             # Baseline starter tests
│   ├── CodeCoverageTest_PES1UG24CS448_train_fare.py   # Code coverage test suite (100%)
│   ├── BranchCoverageTest_PES1UG24CS448_train_fare.py # Branch coverage test suite (100%)
│   ├── pytest.ini                                     # Pytest configuration for test discovery
│   └── README.md                                      # Lab 6 specific notes
│
├── evidence/
│   ├── code_coverage_result.png                       # Terminal output for code coverage
│   └── branch_coverage_result.png                     # Terminal output for branch coverage
│
├── COVERAGE_ANALYSIS.md                               # Detailed coverage analysis & concepts
├── PROJECT_ANALYSIS.md                                # Initial code analysis document
├── requirements.txt                                   # Python dependencies (pytest, coverage)
├── pytest.ini                                         # Global test runner configuration
├── .gitignore                                         # Git ignore specifications
└── README.md                                          # Complete project documentation
```
