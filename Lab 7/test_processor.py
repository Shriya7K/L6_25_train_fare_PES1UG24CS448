import sys
from hypothesis import given, strategies as st
from processor import BERTHS, parse_pnr, journey_distance, berth_type


# ---------------------------------------------------------------------------
# Category 1: Fuzz / Robustness Tests (Arbitrary strings & None)
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
# Category 2: Domain Properties & Algebraic Invariants
# ---------------------------------------------------------------------------

@given(st.from_regex(r'^[0-9]{10}$', fullmatch=True))
def test_parse_pnr_valid_properties(pnr):
    """Property test: Verifies roundtrip decomposition and numeric invariants for valid 10-digit PNRs."""
    result = parse_pnr(pnr)
    assert result is not None
    zone, number = result
    assert zone == int(pnr[0])
    assert number == int(pnr[1:])
    assert 0 <= zone <= 9
    assert 0 <= number <= 999999999
    # Invariant: Reconstructed representation matches original string
    assert f"{zone}{number:09d}" == pnr


@given(
    pnr=st.from_regex(r'^[0-9]{10}$', fullmatch=True),
    ws_left=st.text(alphabet=" \t\r\n", min_size=0, max_size=4),
    ws_right=st.text(alphabet=" \t\r\n", min_size=0, max_size=4)
)
def test_parse_pnr_whitespace_invariance(pnr, ws_left, ws_right):
    """Property test: Leading and trailing whitespace does not affect PNR parsing results."""
    padded = f"{ws_left}{pnr}{ws_right}"
    assert parse_pnr(padded) == parse_pnr(pnr)


@given(st.lists(st.integers(min_value=0, max_value=50000), min_size=2, max_size=15).map(sorted))
def test_journey_distance_valid_properties(distances):
    """Property test: Distance equals endpoints difference, is non-negative, and invariant to intermediate milestones."""
    csv_str = ",".join(str(d) for d in distances)
    result = journey_distance(csv_str)
    assert result is not None
    expected_diff = distances[-1] - distances[0]
    assert result == expected_diff
    assert result >= 0
    # Invariant: Distance between terminal stations alone equals full multi-station distance
    direct_csv = f"{distances[0]},{distances[-1]}"
    assert journey_distance(direct_csv) == result


@given(
    d0=st.integers(min_value=0, max_value=10000),
    d1=st.integers(min_value=0, max_value=10000),
    d2=st.integers(min_value=0, max_value=10000)
)
def test_journey_distance_subjourney_additivity(d0, d1, d2):
    """Property test: Sum of contiguous subjourneys strictly equals the total journey distance."""
    s0, s1, s2 = sorted([d0, d1, d2])
    leg1 = journey_distance(f"{s0},{s1}")
    leg2 = journey_distance(f"{s1},{s2}")
    total = journey_distance(f"{s0},{s1},{s2}")
    assert leg1 is not None and leg2 is not None and total is not None
    assert leg1 + leg2 == total


@given(
    coach=st.sampled_from(["S1", "S2", "B1", "B2", "A1", "H1", "GEN1", "D1"]),
    seat_num=st.integers(min_value=1, max_value=500)
)
def test_berth_type_valid_properties(coach, seat_num):
    """Property test: Valid coach and seat map to valid berths, uppercase coach, and preserve periodicity."""
    seat_str = f"{coach}-{seat_num}"
    result = berth_type(seat_str)
    assert result is not None
    coach_res, berth_res = result
    assert coach_res == coach.upper()
    assert berth_res in BERTHS
    assert berth_res == BERTHS[seat_num % 8]
    # Periodicity invariant: Seat N and Seat N+8 always map to identical berth types
    next_compartment_seat = f"{coach}-{seat_num + 8}"
    next_result = berth_type(next_compartment_seat)
    assert next_result is not None
    assert next_result[1] == berth_res


# ---------------------------------------------------------------------------
# Category 3: Adversarial Tests: Unicode Digits, Long Strings, Separators & Types
# ---------------------------------------------------------------------------

@given(st.text(alphabet="²³¹⁰⁴⁵⁶⁷⁸⁹٠١٢٣٤٥٦٧٨٩०१२३४५६७८९", min_size=1, max_size=20))
def test_parse_pnr_unicode_digits_rejected(unicode_digits):
    """Adversarial test: Non-ASCII Unicode digits do not crash int() and are safely rejected."""
    assert parse_pnr(unicode_digits) is None


@given(st.integers(min_value=11, max_value=5000))
def test_parse_pnr_excessively_long_inputs(num_digits):
    """Adversarial test: Strings exceeding 10 digits (including >4300 digits) are safely rejected."""
    long_pnr = "9" * num_digits
    try:
        assert parse_pnr(long_pnr) is None
    except Exception as e:
        assert False, f"parse_pnr crashed on {num_digits}-digit string: {e}"


@given(st.integers(min_value=11, max_value=5000))
def test_journey_distance_excessive_lengths(num_digits):
    """Adversarial test: Station distance tokens exceeding length limit are safely rejected without conversion error."""
    long_csv = f"0,{'1' * num_digits}"
    try:
        assert journey_distance(long_csv) is None
    except Exception as e:
        assert False, f"journey_distance crashed on {num_digits}-digit token: {e}"


@given(st.text(alphabet="²³¹٠١२३", min_size=1, max_size=10))
def test_journey_distance_unicode_digits(unicode_val):
    """Adversarial test: Non-ASCII Unicode digits in distance CSV are safely rejected."""
    csv_str = f"0,{unicode_val}"
    assert journey_distance(csv_str) is None


@given(st.sampled_from([
    "", "1,,3", ",0,100", "0,100,", ",,", "one,two", "100", "300,100",
    "0, -10, 50", "0, 100, 200\x00", "0;100;200", "0 100 200"
]))
def test_journey_distance_malformed_inputs(malformed):
    """Adversarial test: Malformed CSV formats, negative distances, and descending order return None."""
    assert journey_distance(malformed) is None


@given(st.integers(min_value=7, max_value=5000))
def test_berth_type_excessively_long_seat_number(num_digits):
    """Adversarial test: Seat numbers with excessive digit count are safely rejected without conversion error."""
    seat_str = f"S1-{'9' * num_digits}"
    try:
        assert berth_type(seat_str) is None
    except Exception as e:
        assert False, f"berth_type crashed on {num_digits}-digit seat number: {e}"


@given(st.sampled_from([
    "", "S3", "S3--45", "S3-0", "S3--5", "S3-abc", "123", "-45", "S3-",
    "S-3-45", "S3-²", "S3- 45", "S@-10", "S_3-10", " -10"
]))
def test_berth_type_malformed_and_boundary_formats(invalid_seat):
    """Adversarial test: Non-positive seat numbers, missing hyphens, and malformed coaches return None."""
    assert berth_type(invalid_seat) is None


@given(st.one_of(
    st.integers(),
    st.floats(),
    st.booleans(),
    st.lists(st.text()),
    st.dictionaries(st.text(), st.integers())
))
def test_all_functions_invalid_types(val):
    """Adversarial test: Passing non-string unexpected types to all functions returns None safely."""
    assert parse_pnr(val) is None
    assert journey_distance(val) is None
    assert berth_type(val) is None
