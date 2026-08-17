import csv
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

SCHEMAS = {
    "vehicles.csv": [
        "vehicle_id",
        "make",
        "model",
        "generation",
        "phase",
        "variant",
        "body",
        "engine",
        "engine_code",
        "fuel",
        "power_kw",
        "year_from",
        "year_to",
        "market",
        "notes",
    ],
    "ac_specs.csv": [
        "spec_id",
        "vehicle_id",
        "refrigerant",
        "charge_nominal_g",
        "charge_min_g",
        "charge_max_g",
        "tolerance_plus_g",
        "tolerance_minus_g",
        "oil_type",
        "oil_quantity_ml",
        "compressor",
        "system_variant",
        "status",
        "verified_at",
    ],
    "sources.csv": [
        "source_id",
        "source_type",
        "title",
        "reference",
        "license",
        "evidence_type",
        "evidence_reference",
        "contributor",
        "verification_date",
        "notes",
    ],
    "spec_sources.csv": [
        "spec_id",
        "source_id",
    ],
}

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

ALLOWED_SOURCE_TYPES = {
    "vehicle_label",
    "manufacturer_document",
    "open_dataset",
    "original_observation",
    "other",
}

ALLOWED_EVIDENCE_TYPES = {
    "photo",
    "document",
    "url",
    "none",
}


def error(message):
    print(f"[ERROR] {message}")


def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        error(f"Missing file: {path}")
        return None, False

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != SCHEMAS[filename]:
            error(
                f"{filename} has an invalid schema.\n"
                f"  Expected: {SCHEMAS[filename]}\n"
                f"  Found:    {reader.fieldnames}"
            )
            return [], False

        return list(reader), True
    return None


def check_unique(rows, field, filename):
    success = True
    seen = set()

    for line, row in enumerate(rows, start=2):
        value = row.get(field, "").strip()

        if not value:
            error(f"{filename}:{line}: '{field}' is required")
            success = False
            continue

        if value in seen:
            error(
                f"{filename}:{line}: duplicate {field} '{value}'"
            )
            success = False

        seen.add(value)

    return success


def parse_number(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_vehicles(rows):
    success = check_unique(rows, "vehicle_id", "vehicles.csv")

    for line, row in enumerate(rows, start=2):

        if not row["make"].strip():
            error(f"vehicles.csv:{line}: make is required")
            success = False

        if not row["model"].strip():
            error(f"vehicles.csv:{line}: model is required")
            success = False

        year_from = row["year_from"].strip()
        year_to = row["year_to"].strip()

        if year_from:
            if not year_from.isdigit():
                error(f"vehicles.csv:{line}: invalid year_from")
                success = False
            elif not 1886 <= int(year_from) <= 2100:
                error(f"vehicles.csv:{line}: unrealistic year_from")
                success = False

        if year_to:
            if not year_to.isdigit():
                error(f"vehicles.csv:{line}: invalid year_to")
                success = False
            elif not 1886 <= int(year_to) <= 2100:
                error(f"vehicles.csv:{line}: unrealistic year_to")
                success = False

        if year_from and year_to:
            if year_from.isdigit() and year_to.isdigit():
                if int(year_from) > int(year_to):
                    error(
                        f"vehicles.csv:{line}: "
                        "year_from cannot be greater than year_to"
                    )
                    success = False

        power = row["power_kw"].strip()

        if power:
            value = parse_number(power)

            if value is None or value <= 0:
                error(f"vehicles.csv:{line}: invalid power_kw")
                success = False

    return success


def validate_specs(rows, vehicle_ids):
    success = check_unique(rows, "spec_id", "ac_specs.csv")

    for line, row in enumerate(rows, start=2):

        vehicle_id = row["vehicle_id"].strip()

        if not vehicle_id:
            error(f"ac_specs.csv:{line}: vehicle_id is required")
            success = False
        elif vehicle_id not in vehicle_ids:
            error(
                f"ac_specs.csv:{line}: "
                f"unknown vehicle_id '{vehicle_id}'"
            )
            success = False

        refrigerant = row["refrigerant"].strip()

        if not refrigerant:
            error(f"ac_specs.csv:{line}: refrigerant is required")
            success = False
        elif refrigerant not in ALLOWED_REFRIGERANTS:
            error(
                f"ac_specs.csv:{line}: "
                f"unsupported refrigerant '{refrigerant}'"
            )
            success = False

            # Refrigerant charge validation
        nominal_raw = row["charge_nominal_g"].strip()
        min_raw = row["charge_min_g"].strip()
        max_raw = row["charge_max_g"].strip()

        # Do not mix nominal representation with min/max range representation
        if nominal_raw and (min_raw or max_raw):
            error(
                f"ac_specs.csv:{line}: "
                "use either charge_nominal_g or charge_min_g/charge_max_g, not both"
            )
            success = False

        nominal = parse_number(nominal_raw) if nominal_raw else None
        charge_min = parse_number(min_raw) if min_raw else None
        charge_max = parse_number(max_raw) if max_raw else None

        # At least a nominal charge OR a min/max range is required
        if not nominal_raw and not min_raw and not max_raw:
            error(
                f"ac_specs.csv:{line}: "
                "a refrigerant charge must be specified"
            )
            success = False

        # Validate nominal charge when present
        if nominal_raw:
            if nominal is None or nominal <= 0:
                error(
                    f"ac_specs.csv:{line}: "
                    "charge_nominal_g must be greater than 0"
                )
                success = False

        # Min and max must always be provided together
        if bool(min_raw) != bool(max_raw):
            error(
                f"ac_specs.csv:{line}: "
                "charge_min_g and charge_max_g must be provided together"
            )
            success = False

        # Validate range
        if min_raw and max_raw:
            if charge_min is None or charge_min <= 0:
                error(
                    f"ac_specs.csv:{line}: "
                    "charge_min_g must be greater than 0"
                )
                success = False

            if charge_max is None or charge_max <= 0:
                error(
                    f"ac_specs.csv:{line}: "
                    "charge_max_g must be greater than 0"
                )
                success = False

            if (
                    charge_min is not None
                    and charge_max is not None
                    and charge_min > charge_max
            ):
                error(
                    f"ac_specs.csv:{line}: "
                    "charge_min_g cannot be greater than charge_max_g"
                )
                success = False

        for field in ("tolerance_plus_g", "tolerance_minus_g"):
            raw = row[field].strip()

            if raw:
                value = parse_number(raw)

                if value is None or value < 0:
                    error(
                        f"ac_specs.csv:{line}: "
                        f"{field} must be zero or greater"
                    )
                    success = False

        oil = row["oil_quantity_ml"].strip()

        if oil:
            value = parse_number(oil)

            if value is None or value < 0:
                error(
                    f"ac_specs.csv:{line}: "
                    "oil_quantity_ml must be zero or greater"
                )
                success = False

        status = row["status"].strip()

        if status not in ALLOWED_STATUSES:
            error(
                f"ac_specs.csv:{line}: invalid status '{status}'"
            )
            success = False

        linked_evidence_check = status in {
            "verified",
            "community_verified",
        }

        verified_at = row["verified_at"].strip()

        if verified_at and not valid_date(verified_at):
            error(
                f"ac_specs.csv:{line}: "
                "verified_at must use YYYY-MM-DD"
            )
            success = False

    return success


def validate_sources(rows):
    success = check_unique(rows, "source_id", "sources.csv")

    for line, row in enumerate(rows, start=2):

        source_type = row["source_type"].strip()

        if source_type not in ALLOWED_SOURCE_TYPES:
            error(
                f"sources.csv:{line}: "
                f"invalid source_type '{source_type}'"
            )
            success = False

        evidence_type = row["evidence_type"].strip()

        if evidence_type not in ALLOWED_EVIDENCE_TYPES:
            error(
                f"sources.csv:{line}: "
                f"invalid evidence_type '{evidence_type}'"
            )
            success = False

        evidence_reference = row["evidence_reference"].strip()

        if evidence_type != "none" and not evidence_reference:
            error(
                f"sources.csv:{line}: "
                "evidence_reference is required when evidence_type is not 'none'"
            )
            success = False

        date = row["verification_date"].strip()

        if date and not valid_date(date):
            error(
                f"sources.csv:{line}: "
                "verification_date must use YYYY-MM-DD"
            )
            success = False

    return success


def validate_links(rows, spec_ids, source_ids):
    success = True
    links = set()
    linked_specs = set()

    for line, row in enumerate(rows, start=2):

        spec_id = row["spec_id"].strip()
        source_id = row["source_id"].strip()

        if spec_id not in spec_ids:
            error(
                f"spec_sources.csv:{line}: "
                f"unknown spec_id '{spec_id}'"
            )
            success = False

        if source_id not in source_ids:
            error(
                f"spec_sources.csv:{line}: "
                f"unknown source_id '{source_id}'"
            )
            success = False

        link = (spec_id, source_id)

        if link in links:
            error(
                f"spec_sources.csv:{line}: "
                f"duplicate link {spec_id} -> {source_id}"
            )
            success = False

        links.add(link)

        if spec_id:
            linked_specs.add(spec_id)

    for spec_id in spec_ids:
        if spec_id not in linked_specs:
            error(f"Specification '{spec_id}' has no source")
            success = False

    return success


def main():
    success = True
    datasets = {}

    for filename in SCHEMAS:
        rows, valid = load_csv(filename)
        datasets[filename] = rows or []

        if not valid:
            success = False

    if not success:
        print("OpenAutoAC validation failed.")
        sys.exit(1)

    vehicles = datasets["vehicles.csv"]
    specs = datasets["ac_specs.csv"]
    sources = datasets["sources.csv"]
    links = datasets["spec_sources.csv"]

    if not validate_vehicles(vehicles):
        success = False

    vehicle_ids = {
        row["vehicle_id"].strip()
        for row in vehicles
        if row["vehicle_id"].strip()
    }

    if not validate_specs(specs, vehicle_ids):
        success = False

    if not validate_sources(sources):
        success = False

    spec_ids = {
        row["spec_id"].strip()
        for row in specs
        if row["spec_id"].strip()
    }

    source_ids = {
        row["source_id"].strip()
        for row in sources
        if row["source_id"].strip()
    }

    if not validate_links(links, spec_ids, source_ids):
        success = False

    if success:
        print("OpenAutoAC validation passed.")
        print(
            f"{len(vehicles)} vehicles, "
            f"{len(specs)} AC specifications, "
            f"{len(sources)} sources."
        )
        sys.exit(0)

    print("OpenAutoAC validation failed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
