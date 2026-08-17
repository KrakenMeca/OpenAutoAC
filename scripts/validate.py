import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

ALLOWED_REFRIGERANTS = {
    "R134a",
    "R1234yf",
    "R744",
}

ALLOWED_STATUSES = {
    "pending",
    "verified",
    "community_verified",
    "disputed",
    "deprecated",
}


def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        print(f"[ERROR] Missing file: {path}")
        sys.exit(1)

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
    return None


def check_unique(rows, field, filename):
    seen = set()

    for line_number, row in enumerate(rows, start=2):
        value = row.get(field, "").strip()

        if not value:
            continue

        if value in seen:
            print(
                f"[ERROR] Duplicate {field} '{value}' "
                f"in {filename}, line {line_number}"
            )
            return False

        seen.add(value)

    return True


def is_number(value):
    if value is None or value.strip() == "":
        return True

    try:
        float(value)
        return True
    except ValueError:
        return False


def main():
    success = True

    vehicles = load_csv("vehicles.csv")
    specs = load_csv("ac_specs.csv")
    sources = load_csv("sources.csv")
    spec_sources = load_csv("spec_sources.csv")

    if not check_unique(vehicles, "vehicle_id", "vehicles.csv"):
        success = False

    if not check_unique(specs, "spec_id", "ac_specs.csv"):
        success = False

    if not check_unique(sources, "source_id", "sources.csv"):
        success = False

    vehicle_ids = {
        row["vehicle_id"].strip()
        for row in vehicles
        if row.get("vehicle_id", "").strip()
    }

    spec_ids = {
        row["spec_id"].strip()
        for row in specs
        if row.get("spec_id", "").strip()
    }

    source_ids = {
        row["source_id"].strip()
        for row in sources
        if row.get("source_id", "").strip()
    }

    for line_number, row in enumerate(specs, start=2):
        spec_id = row.get("spec_id", "").strip()
        vehicle_id = row.get("vehicle_id", "").strip()

        if vehicle_id and vehicle_id not in vehicle_ids:
            print(
                f"[ERROR] Spec '{spec_id}' references unknown "
                f"vehicle_id '{vehicle_id}'"
            )
            success = False

        refrigerant = row.get("refrigerant", "").strip()

        if refrigerant and refrigerant not in ALLOWED_REFRIGERANTS:
            print(
                f"[ERROR] Unsupported refrigerant '{refrigerant}' "
                f"in ac_specs.csv line {line_number}"
            )
            success = False

        status = row.get("status", "").strip()

        if status and status not in ALLOWED_STATUSES:
            print(
                f"[ERROR] Invalid status '{status}' "
                f"in ac_specs.csv line {line_number}"
            )
            success = False

        numeric_fields = [
            "charge_nominal_g",
            "tolerance_plus_g",
            "tolerance_minus_g",
            "oil_quantity_ml",
        ]

        for field in numeric_fields:
            if not is_number(row.get(field, "")):
                print(
                    f"[ERROR] '{field}' must be numeric "
                    f"in ac_specs.csv line {line_number}"
                )
                success = False

    links_seen = set()

    for line_number, row in enumerate(spec_sources, start=2):
        spec_id = row.get("spec_id", "").strip()
        source_id = row.get("source_id", "").strip()

        if spec_id not in spec_ids:
            print(
                f"[ERROR] spec_sources.csv line {line_number}: "
                f"unknown spec_id '{spec_id}'"
            )
            success = False

        if source_id not in source_ids:
            print(
                f"[ERROR] spec_sources.csv line {line_number}: "
                f"unknown source_id '{source_id}'"
            )
            success = False

        link = (spec_id, source_id)

        if link in links_seen:
            print(
                f"[ERROR] Duplicate spec/source link "
                f"'{spec_id}' -> '{source_id}'"
            )
            success = False

        links_seen.add(link)

    for spec_id in spec_ids:
        linked_sources = [
            source_id
            for linked_spec_id, source_id in links_seen
            if linked_spec_id == spec_id
        ]

        if not linked_sources:
            print(
                f"[ERROR] Spec '{spec_id}' has no declared source"
            )
            success = False

    if success:
        print("OpenAutoAC validation passed.")
        sys.exit(0)

    print("OpenAutoAC validation failed.")
    sys.exit(1)


if __name__ == "__main__":
    main()