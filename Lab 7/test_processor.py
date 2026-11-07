from hypothesis import given, strategies as st
from processor import BERTHS, parse_pnr, journey_distance, berth_type


# ---------------------------------------------------------------------------
# Fuzz Tests: No-crash properties with random text and None inputs
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_pnr_no_crash(s):
    """Fuzz testing parse_pnr with arbitrary strings or None to ensure no uncaught crashes."""
    try:
        parse_pnr(s)
    except Exception as e:
        assert False, f"parse_pnr crashed with: {e}"


@given(st.text() | st.none())
def test_journey_distance_no_crash(s):
    """Fuzz testing journey_distance with arbitrary strings or None to ensure no uncaught crashes."""
    try:
        journey_distance(s)
    except Exception as e:
        assert False, f"journey_distance crashed with: {e}"


@given(st.text() | st.none())
def test_berth_type_no_crash(s):
    """Fuzz testing berth_type with arbitrary strings or None to ensure no uncaught crashes."""
    try:
        berth_type(s)
    except Exception as e:
        assert False, f"berth_type crashed with: {e}"


# ---------------------------------------------------------------------------
# Property Tests: Valid inputs satisfy intended domain properties
# ---------------------------------------------------------------------------

@given(st.from_regex(r'^[0-9]{10}$', fullmatch=True))
def test_parse_pnr_valid(pnr):
    """Test parse_pnr correctly parses valid 10-digit PNR strings."""
    result = parse_pnr(pnr)
    assert result is not None
    zone, number = result
    assert zone == int(pnr[0])
    assert number == int(pnr[1:])
    assert 0 <= zone <= 9


@given(st.lists(st.integers(min_value=0, max_value=5000), min_size=2, max_size=10).map(sorted))
def test_journey_distance_valid(distances):
    """Test journey_distance correctly computes the distance for valid ascending station distances."""
    csv_str = ",".join(str(d) for d in distances)
    result = journey_distance(csv_str)
    assert result is not None
    assert result == distances[-1] - distances[0]
    assert result >= 0


@given(
    coach=st.sampled_from(["S1", "S2", "B1", "B2", "A1", "H1"]),
    seat_num=st.integers(min_value=1, max_value=120)
)
def test_berth_type_valid(coach, seat_num):
    """Test berth_type correctly identifies berth category and uppercase coach for valid seats."""
    seat_str = f"{coach}-{seat_num}"
    result = berth_type(seat_str)
    assert result is not None
    coach_res, berth_res = result
    assert coach_res == coach.upper()
    assert berth_res in BERTHS
    assert berth_res == BERTHS[seat_num % 8]


# ---------------------------------------------------------------------------
# Edge Case and Type Validation Tests
# ---------------------------------------------------------------------------

@given(st.one_of(st.integers(), st.floats(), st.booleans(), st.lists(st.integers())))
def test_parse_pnr_invalid_types(val):
    """Test parse_pnr handles non-string and invalid types safely without crashing."""
    try:
        result = parse_pnr(val)
        assert result is None
    except Exception as e:
        assert False, f"parse_pnr crashed on invalid type {type(val)}: {e}"


@given(st.sampled_from(["", "1,,3", "one,two", "100", ",,", "0, -10, 50"]))
def test_journey_distance_malformed_csv(malformed):
    """Test journey_distance safely handles malformed CSVs, empty elements, and negative values."""
    try:
        result = journey_distance(malformed)
        assert result is None
    except Exception as e:
        assert False, f"journey_distance crashed on malformed CSV '{malformed}': {e}"


@given(st.sampled_from(["", "S3", "S3--45", "S3-0", "S3--5", "S3-abc", "123", "-45", "S3-"]))
def test_berth_type_invalid_formats(invalid_seat):
    """Test berth_type safely handles malformed seat identifiers without crashing."""
    try:
        result = berth_type(invalid_seat)
        assert result is None
    except Exception as e:
        assert False, f"berth_type crashed on invalid format '{invalid_seat}': {e}"
