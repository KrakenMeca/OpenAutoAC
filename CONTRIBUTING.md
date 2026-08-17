# Contributing to OpenAutoAC

Thank you for helping build OpenAutoAC, an open database of automotive air-conditioning specifications.

Data accuracy and provenance are essential. Incorrect refrigerant information can lead to improper servicing of a vehicle, so every contribution must be traceable to an acceptable source.

## What you can contribute

Contributions may include:

* new vehicles;
* refrigerant type;
* refrigerant charge quantity;
* charge tolerance;
* compressor oil type;
* compressor oil quantity;
* compressor information;
* corrections to existing records;
* additional verification of existing records.

## Accepted sources

Preferred sources include:

### Vehicle labels

Information read directly from an air-conditioning or refrigerant label fitted to the vehicle.

A photograph may be provided as supporting evidence.

Before submitting a photograph, personal or vehicle-identifying information such as the VIN or registration number must be removed or obscured.

### Original measurements or observations

Information independently collected by a contributor during legitimate vehicle servicing, where the contributor has the right to share the resulting factual information.

### Openly licensed sources

Information from datasets or documentation whose license explicitly permits redistribution under terms compatible with OpenAutoAC.

The original source and license must be provided.

### Manufacturer information

Manufacturer documentation may only be used when its applicable terms permit the relevant information to be redistributed.

Access to repair information does not automatically imply a right to republish it.

## Prohibited sources

Do not submit data copied, scraped, exported, transcribed in bulk or systematically reconstructed from proprietary databases without explicit permission to redistribute it.

This includes, but is not limited to:

* Autodata
* TecRMI / TecAlliance
* HaynesPro
* MAHLE
* HELLA
* proprietary manufacturer databases
* other commercial technical-information databases

Changing the format, translating the information or manually copying individual records does not by itself establish redistribution rights.

## Required information

Each contribution should identify, where available:

* manufacturer;
* model;
* generation;
* production year or year range;
* engine/variant;
* refrigerant type;
* refrigerant quantity;
* tolerance;
* compressor oil type;
* compressor oil quantity;
* source type;
* date of verification.

Do not guess missing values.

Unknown information should remain empty.

## Source declaration

Every contribution must include a source declaration.

Example:

```yaml
source_type: vehicle_label
description: Air-conditioning label under bonnet
evidence_available: true
verification_date: 2026-08-17
```

## Contributor declaration

By submitting a contribution, you confirm that:

* you have the right to contribute the submitted information;
* the information was not obtained through unauthorized extraction of a protected database;
* the source declaration is truthful;
* the contribution may be distributed according to the licensing terms of OpenAutoAC.

## Verification

Submitted data may initially be marked as:

`pending`

After review, records may become:

`verified`

or:

`community_verified`

Conflicting or questionable information may be marked:

`disputed`

Records that are no longer applicable may be marked:

`deprecated`

Maintainers may request additional evidence before accepting a contribution.

## Accuracy

Never estimate refrigerant quantities.

For example, if a label states:

`R1234yf — 430 ± 15 g`

submit those values exactly.

Do not convert this into an assumed range unless the OpenAutoAC schema explicitly performs that conversion.

## Corrections

Corrections are welcome.

When correcting an existing value, provide the source supporting the new value and explain why the existing record appears incorrect.

Where reliable sources disagree, both pieces of evidence should be preserved for review rather than silently replacing one value with another.

## Licensing

By contributing database content to OpenAutoAC, you agree that your contribution may be distributed under the licensing terms described in `DATA-LICENSE.md`.

Thank you for helping create a reliable, traceable and openly accessible automotive air-conditioning database.
