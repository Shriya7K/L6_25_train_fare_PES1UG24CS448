# L6_L7_25_train_fare — Train Fare

Lab 7: Fuzz Testing for Input Validation Bugs

## Files

| File | Description |
|------|-------------|
| `processor.py` | Hardened train fare processor application with input validation |
| `test_processor.py` | Completed Hypothesis property-based fuzz tests |
| `train_fare.py` | Hardened train fare calculation module |
| `test_train_fare.py` | Completed Hypothesis property-based fuzz tests |
| `Lab 7 - Fuzzing for Input Validation Bugs.pdf` | Lab report documenting before-and-after execution and test evidence screenshots |

## Execution

### Run Application
```bash
python processor.py
```

### Run Fuzz Tests
```bash
python -m pytest test_processor.py -v
```
