BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]


def parse_pnr(pnr):
    """
    Parses a 10-digit Indian Railways PNR into its starting zone digit
    and the remaining 9-digit ticket number.

    Returns (zone, number) if valid, otherwise None.
    """
    if not isinstance(pnr, str):
        return None
    pnr = pnr.strip()
    if len(pnr) != 10 or not pnr.isdigit():
        return None
    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    """
    Calculates total journey distance from comma-separated station milestone distances.

    Returns total distance (last station - first station) if valid, otherwise None.
    """
    if not isinstance(distances_csv, str):
        return None
    distances_csv = distances_csv.strip()
    if not distances_csv:
        return None
    parts = distances_csv.split(',')
    if len(parts) < 2:
        return None
    distances = []
    for part in parts:
        cleaned = part.strip()
        if not cleaned or not cleaned.isdigit():
            return None
        distances.append(int(cleaned))
    if distances[-1] < distances[0]:
        return None
    return distances[-1] - distances[0]


def berth_type(seat):
    """
    Determines coach and berth type (LB, MB, UB, SL, SU) for a given seat identifier
    in coach-seat format (e.g., 'S3-45').

    Returns (coach.upper(), berth_type) if valid, otherwise None.
    """
    if not isinstance(seat, str):
        return None
    seat = seat.strip()
    if '-' not in seat:
        return None
    parts = seat.split('-')
    if len(parts) != 2:
        return None
    coach = parts[0].strip()
    number_str = parts[1].strip()
    if not coach or not coach.isalnum():
        return None
    if not number_str or not number_str.isdigit():
        return None
    number = int(number_str)
    if number <= 0:
        return None
    return coach.upper(), BERTHS[number % 8]


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
