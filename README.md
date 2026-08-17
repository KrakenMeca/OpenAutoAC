# ❄️ OpenAutoAC

**Open automotive air-conditioning refrigerant and compressor oil database.**

OpenAutoAC is an open-data project maintained by **KrakenMeca** with the goal of building a reliable, structured and traceable database of automotive air-conditioning specifications.

> ⚠️ **Project status: Early Development**
>
> The database structure and validation system are currently being developed.
> Data coverage is still very limited and should not yet be considered suitable for production use.

---

## 🎯 Project goals

Finding reliable automotive A/C specifications can be difficult. Information is often scattered across vehicle labels, manufacturer documentation, workshop information systems and proprietary databases.

OpenAutoAC aims to provide an open and community-maintained dataset containing:

* 🚗 Vehicle identification
* ❄️ Refrigerant type
* ⚖️ Refrigerant charge quantity
* ↔️ Refrigerant charge tolerance
* 🛢️ Compressor oil specification
* 🧪 Compressor oil quantity
* ⚙️ Compressor information
* 📚 Traceable data sources
* ✅ Verification status

The project focuses on **data provenance and reliability**, not simply database size.

---

## 📂 Database structure

OpenAutoAC currently uses CSV as its canonical source format.

```text
data/
├── vehicles.csv
├── ac_specs.csv
├── sources.csv
└── spec_sources.csv
```

### `vehicles.csv`

Contains vehicle identification information.

```text
vehicle_id
make
model
generation
variant
engine
engine_code
power_kw
year_from
year_to
```

### `ac_specs.csv`

Contains air-conditioning specifications associated with a vehicle.

```text
spec_id
vehicle_id
refrigerant
charge_nominal_g
tolerance_plus_g
tolerance_minus_g
oil_type
oil_quantity_ml
compressor
system_variant
status
verified_at
```

### `sources.csv`

Records the provenance of contributed information.

Evidence is **optional**, but provenance is required.

A source can include evidence such as:

* a vehicle refrigerant label photograph;
* a document;
* an openly accessible reference URL;
* or no preserved evidence when the information comes from an original observation.

### `spec_sources.csv`

Creates the relationship between an A/C specification and one or more independent sources.

```text
AC specification
      │
      ├── Source A
      ├── Source B
      └── Source C
```

This allows the same specification to be independently confirmed by multiple contributors.

---

## 🔎 Data status

Specifications can currently use the following statuses:

### `pending`

The information has been submitted but has not yet received sufficient verification.

### `verified`

The information has been reviewed against sufficiently strong supporting evidence.

### `community_verified`

Multiple independent contributions support the same specification.

### `disputed`

Reliable sources or observations disagree.

### `deprecated`

The record is retained for historical purposes but should no longer be considered current.

Verification rules are still being developed and may evolve as the project grows.

---

## 📚 Data provenance

Every OpenAutoAC specification must be traceable to at least one declared source.

Evidence itself is not mandatory.

For example, a professional technician may contribute an observation without having photographed the vehicle label. Such information may enter the database as `pending` and later be confirmed by additional independent sources.

OpenAutoAC values **traceability over unverifiable bulk data**.

---

## 🚫 Proprietary databases

Do **not** contribute information copied, scraped, exported or systematically reconstructed from proprietary databases unless redistribution has been explicitly authorized.

This includes, but is not limited to:

* Autodata
* TecRMI / TecAlliance
* HaynesPro
* MAHLE
* HELLA
* proprietary manufacturer databases
* other commercial automotive technical-information services

Public accessibility of information does not automatically grant redistribution rights.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`DATA-LICENSE.md`](DATA-LICENSE.md) before contributing.

---

## 🧪 Automatic validation

OpenAutoAC includes an automated data validator.

Run locally with:

```bash
python3 scripts/validate.py
```

The validator currently checks:

* CSV schemas;
* unique identifiers;
* vehicle references;
* source references;
* refrigerant types;
* numeric quantities;
* production-year consistency;
* verification dates;
* specification/source relationships;
* duplicate relationships.

Validation is also automatically executed through GitHub Actions for pushes and pull requests targeting the `main` branch.

---

## 🤝 Contributing

Community contributions are welcome.

Before submitting data, please read:

[`CONTRIBUTING.md`](CONTRIBUTING.md)

Contributors must declare the provenance of submitted information and confirm that they have the right to contribute it.

Do not guess missing technical values.

If information is unknown, leave the corresponding optional field empty.

---

## 🔐 Privacy

Do not submit personally identifiable or vehicle-identifying information that is unnecessary for the database.

Photographic evidence should have information such as the following removed or obscured when applicable:

* VIN;
* registration plate;
* owner information;
* workshop customer information.

---

## 📜 License

The OpenAutoAC database is distributed under the **Open Database License (ODbL) 1.0**.

Individual database contents are distributed according to the terms described in [`DATA-LICENSE.md`](DATA-LICENSE.md).

Third-party documents and source material referenced by OpenAutoAC remain subject to their respective licenses and rights.

---

## 🐙 Maintainer

OpenAutoAC is maintained by **KrakenMeca**.

The project was initially created to support open and traceable automotive air-conditioning technical data and can be used by workshop tools, educational projects, applications and other compatible projects.

---

## ⚠️ Disclaimer

OpenAutoAC is a community-maintained technical database.

Automotive air-conditioning systems operate under pressure and refrigerants are subject to specific handling and environmental regulations.

Database information may contain errors, omissions or outdated values.

Always verify critical specifications against appropriate technical information before servicing a vehicle.
