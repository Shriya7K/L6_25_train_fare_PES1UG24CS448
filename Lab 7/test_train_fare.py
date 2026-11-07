from hypothesis import given, strategies as st
from train_fare import parse_pnr, journey_distance, berth_type

@given(st.text() | st.none())
def test_parse_pnr_no_crash(s):

@given(st.text() | st.none())
def test_journey_distance_no_crash(s):

@given(st.text() | st.none())
def test_berth_type_no_crash(s):
