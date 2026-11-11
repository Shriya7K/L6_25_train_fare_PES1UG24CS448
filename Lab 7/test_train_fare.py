from hypothesis import given, strategies as st

from train_fare import BERTHS, berth_type, journey_distance, parse_pnr


UNICODE_NUMERIC_CHARS = (
    "\u00b2",
    "\u00b3",
    "\u00b9",
    "\u2070",
    "\u0660",
    "\u0665",
    "\u0966",
    "\uff10",
)

NON_DIGIT_EDGE_CHARS = UNICODE_NUMERIC_CHARS + (" ", "+", "-", "a", "/")

UNEXPECTED_TYPES = st.one_of(
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(),
    st.lists(st.integers(), max_size=5),
    st.dictionaries(st.text(max_size=5), st.integers(), max_size=3),
)


def _is_plain_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _assert_valid_or_none(result, validator):
    assert result is None or validator(result)


@given(st.text() | st.none())
def test_parse_pnr_no_crash(pnr):
    result = parse_pnr(pnr)
    _assert_valid_or_none(
        result,
        lambda pair: (
            isinstance(pair, tuple)
            and len(pair) == 2
            and _is_plain_int(pair[0])
            and _is_plain_int(pair[1])
            and 0 <= pair[0] <= 9
            and 0 <= pair[1] <= 999_999_999
        ),
    )


@given(UNEXPECTED_TYPES)
def test_parse_pnr_unexpected_types(value):
    assert parse_pnr(value) is None


@given(
    st.sampled_from(NON_DIGIT_EDGE_CHARS),
    st.text(alphabet="0123456789", min_size=9, max_size=9),
    st.integers(min_value=0, max_value=9),
)
def test_parse_pnr_rejects_unicode_signs_and_spaces(bad_ch, digits, pos):
    candidate = digits[:pos] + bad_ch + digits[pos:]
    assert parse_pnr(candidate) is None


@given(st.text(alphabet="0123456789", max_size=25).filter(lambda s: len(s) != 10))
def test_parse_pnr_rejects_invalid_lengths(pnr):
    assert parse_pnr(pnr) is None


@given(st.integers(min_value=4500, max_value=5500))
def test_parse_pnr_rejects_long_numeric_strings(length):
    assert parse_pnr("1" * length) is None


@given(
    st.text(alphabet="0123456789", min_size=10, max_size=10),
    st.text(alphabet=" \t\r\n", max_size=3),
    st.text(alphabet=" \t\r\n", max_size=3),
)
def test_parse_pnr_valid_roundtrip(pnr, left_ws, right_ws):
    result = parse_pnr(f"{left_ws}{pnr}{right_ws}")
    assert result == (int(pnr[0]), int(pnr[1:]))
    zone, serial = result
    assert f"{zone}{serial:09d}" == pnr


@given(st.text() | st.none())
def test_journey_distance_no_crash(distances_csv):
    result = journey_distance(distances_csv)
    _assert_valid_or_none(result, lambda val: _is_plain_int(val) and val >= 0)


@given(UNEXPECTED_TYPES)
def test_journey_distance_unexpected_types(value):
    assert journey_distance(value) is None


@given(
    st.lists(
        st.one_of(
            st.just(""),
            st.just(" "),
            st.just("-10"),
            st.just("+10"),
            st.just("1 2"),
            st.just("abc"),
            st.sampled_from(UNICODE_NUMERIC_CHARS),
        ),
        min_size=1,
        max_size=5,
    )
)
def test_journey_distance_rejects_malformed_and_unicode(tokens):
    assert journey_distance(",".join(tokens)) is None


@given(st.integers(min_value=4500, max_value=5500))
def test_journey_distance_rejects_long_numeric_strings(length):
    assert journey_distance(f"0,{'9' * length}") is None


@given(
    st.lists(st.integers(min_value=0, max_value=50_000), max_size=5).map(sorted),
    st.integers(min_value=0, max_value=50_000),
    st.integers(min_value=1, max_value=10_000),
)
def test_journey_distance_rejects_descending_distances(prefix, low, delta):
    high = low + delta
    if prefix:
        base = prefix[-1]
        seq = prefix + [base + high, base + low]
    else:
        seq = [high, low]
    assert journey_distance(",".join(str(x) for x in seq)) is None


@given(
    st.lists(st.integers(min_value=0, max_value=100_000), min_size=1, max_size=10).map(sorted),
    st.integers(min_value=1, max_value=1000),
)
def test_journey_distance_valid_properties(distances, shift):
    csv_value = ",".join(str(d) for d in distances)
    spaced_csv = " , ".join(str(d) for d in distances)
    expected = distances[-1] - distances[0]

    result = journey_distance(csv_value)
    assert result == expected
    assert journey_distance(f" {spaced_csv} ") == expected

    shifted_csv = ",".join(str(d + shift) for d in distances)
    assert journey_distance(shifted_csv) == result


@given(st.text() | st.none())
def test_berth_type_no_crash(seat):
    result = berth_type(seat)
    _assert_valid_or_none(
        result,
        lambda pair: (
            isinstance(pair, tuple)
            and len(pair) == 2
            and isinstance(pair[0], str)
            and len(pair[0]) >= 1
            and pair[0].isascii()
            and pair[0].isalnum()
            and pair[0] == pair[0].upper()
            and pair[1] in BERTHS
        ),
    )


@given(UNEXPECTED_TYPES)
def test_berth_type_unexpected_types(value):
    assert berth_type(value) is None


@given(
    st.one_of(
        st.just(""),
        st.just("S3"),
        st.just("S3-"),
        st.just("-45"),
        st.just("S3- 45"),
        st.just("S3 -45"),
        st.just("S 3-45"),
        st.just("S3-45-1"),
        st.just("@1-45"),
        st.sampled_from(UNICODE_NUMERIC_CHARS).map(lambda c: f"S3-{c}"),
        st.sampled_from(UNICODE_NUMERIC_CHARS).map(lambda c: f"{c}-45"),
    )
)
def test_berth_type_rejects_malformed_and_unicode(seat):
    assert berth_type(seat) is None


@given(st.integers(min_value=4500, max_value=5500))
def test_berth_type_rejects_long_seat_numbers(length):
    assert berth_type(f"S3-{'9' * length}") is None


@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", min_size=1, max_size=5),
    st.integers(min_value=-1000, max_value=0),
)
def test_berth_type_rejects_non_positive_seat(coach, seat_num):
    assert berth_type(f"{coach}-{seat_num}") is None


@given(
    st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        min_size=1,
        max_size=6,
    ),
    st.integers(min_value=1, max_value=500),
)
def test_berth_type_valid_and_cyclic(coach, seat_num):
    result = berth_type(f"{coach}-{seat_num}")
    assert result == (coach.upper(), BERTHS[seat_num % 8])
    assert berth_type(f"  {coach}-{seat_num}  ") == result
    assert berth_type(f"{coach}-{seat_num + 8}") == result
