BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]

PNR_LENGTH = 10
MAX_DISTANCE_DIGITS = 10
MAX_STATIONS = 1000
MAX_COACH_LENGTH = 10
MAX_SEAT_DIGITS = 6


def _is_ascii_digits(value):
    """Return True if value is a non-empty string of ASCII digits '0'-'9'."""
    # Restrict to ASCII '0'-'9' so Unicode numerals (e.g. superscripts or
    # Arabic-Indic digits) are rejected before calling int().
    return bool(value) and all("0" <= ch <= "9" for ch in value)


def parse_pnr(pnr):
    """Parse a 10-digit PNR string into (zone, number), or None if invalid."""
    if not isinstance(pnr, str):
        return None
    cleaned = pnr.strip()
    if len(cleaned) != PNR_LENGTH or not _is_ascii_digits(cleaned):
        return None
    return int(cleaned[0]), int(cleaned[1:])


def journey_distance(distances_csv):
    """Return total distance from non-decreasing CSV station distances, or None."""
    if not isinstance(distances_csv, str):
        return None
    cleaned = distances_csv.strip()
    if not cleaned:
        return None
    parts = cleaned.split(",")
    if len(parts) > MAX_STATIONS:
        return None

    distances = []
    for raw_part in parts:
        token = raw_part.strip()
        # Reject long digit runs before int() reaches Python's 4300-digit limit.
        if not token or len(token) > MAX_DISTANCE_DIGITS or not _is_ascii_digits(token):
            return None
        value = int(token)
        if distances and value < distances[-1]:
            return None
        distances.append(value)

    return distances[-1] - distances[0]


def berth_type(seat):
    """Return (COACH, BERTH) for a '<coach>-<seat>' string, or None if invalid."""
    if not isinstance(seat, str):
        return None
    cleaned = seat.strip()
    if not cleaned:
        return None
    parts = cleaned.split("-")
    if len(parts) != 2:
        return None

    # Keep internal whitespace unstripped so malformed inputs like 'S3- 45' fail.
    coach, number_str = parts
    if not coach or len(coach) > MAX_COACH_LENGTH or not (coach.isascii() and coach.isalnum()):
        return None
    if len(number_str) > MAX_SEAT_DIGITS or not _is_ascii_digits(number_str):
        return None

    seat_number = int(number_str)
    if seat_number <= 0:
        return None
    return coach.upper(), BERTHS[seat_number % len(BERTHS)]


def main():
    print("==== Running parse_pnr ====")
    user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
    result = parse_pnr(user_input)
    print("Zone and Number:", result)

    print("\n==== Running journey_distance ====")
    user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
    result = journey_distance(user_input)
    print("Total Distance:", result)

    print("\n==== Running berth_type ====")
    user_input = input("Enter coach and seat (e.g. S3-45): ")
    result = berth_type(user_input)
    print("Coach and Berth:", result)


if __name__ == "__main__":
    main()
