#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema>=4.22,<5"]
# ///
"""Validate JSONL against the live Open Library schema, failing closed."""

import argparse
import hashlib
import json
import sys
from functools import cache
from pathlib import Path
from urllib.request import urlopen

from jsonschema.validators import validator_for
from referencing import Registry, Resource

SCHEMA_URL = "https://raw.githubusercontent.com/internetarchive/openlibrary-client/master/olclient/schemata/import.schema.json"


def make_validator():
    # Cache only within this invocation; the next run fetches live schemas again.
    @cache
    def retrieve(uri):
        if not uri.startswith(SCHEMA_URL.rsplit("/", 1)[0] + "/"):
            raise ValueError(f"Unexpected schema reference: {uri}")
        with urlopen(uri, timeout=30) as response:
            raw = response.read()
        schema = json.loads(raw)
        validator_for(schema).check_schema(schema)
        print(f"Fetched {uri} (sha256:{hashlib.sha256(raw).hexdigest()})", file=sys.stderr)
        return Resource.from_contents(schema)

    resource = retrieve(SCHEMA_URL)
    registry = Registry(retrieve=retrieve).with_resource(SCHEMA_URL, resource)
    return validator_for(resource.contents)({"$ref": SCHEMA_URL}, registry=registry)


def reject_constant(value):
    raise ValueError(f"{value} is not valid JSON")


def validate_jsonl(text, validator):
    lines = text.splitlines()
    errors = []
    if not lines:
        return 0, ["Empty batch: supply at least one record"]
    for number, line in enumerate(lines, 1):
        try:
            record = json.loads(line, parse_constant=reject_constant)
        except ValueError as error:
            errors.append(f"line {number}: {error}")
            continue
        for error in validator.iter_errors(record):
            errors.append(f"line {number} {error.json_path}: {error.message}")
    return len(lines), errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="UTF-8 JSONL batch to validate")
    args = parser.parse_args()
    try:
        raw = args.file.read_bytes()
        validator = make_validator()
        count, errors = validate_jsonl(raw.decode("utf-8"), validator)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print(f"PASS: {count} record(s), full live JSON Schema validation including references")
        print(f"JSONL sha256:{hashlib.sha256(raw).hexdigest()}")
        return 0
    except Exception as error:
        print(f"FAIL: validation could not complete: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
