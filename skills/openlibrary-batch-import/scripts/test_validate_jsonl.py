# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema>=4.22,<5"]
# ///
"""Run with uv run test_validate_jsonl.py; uses the real live schema."""

import json
from unittest.mock import patch
from urllib.error import URLError

from validate_jsonl import make_validator, validate_jsonl

record = {
    "title": "Nine Rupees an Hour",
    "subtitle": "Disappearing Livelihoods of Tamil Nadu",
    "authors": [{"name": "Aparna Karthikeyan"}],
    "publishers": ["Context"],
    "publish_date": "2019-10-10",
    "languages": ["eng"],
    "physical_format": "Paperback",
    "number_of_pages": 288,
    "isbn_10": ["9388754506"],
    "isbn_13": ["9789388754507"],
    "source_records": ["amazon:9388754506"],
    "identifiers": {"amazon": ["9388754506"]},
    "links": [{"url": "https://www.amazon.in/dp/9388754506", "title": "Amazon paperback edition"}],
}
validator = make_validator()
valid = json.dumps(record)
assert validate_jsonl(valid + "\n", validator) == (1, [])
assert validate_jsonl(valid + "\n" + valid, validator) == (2, [])
for field, value in [
    ("languages", ["English"]),
    ("isbn_13", ["123"]),
    ("authors", ["Aparna Karthikeyan"]),
    ("links", [{"url": "https://example.com"}]),
    ("identifiers", {"amazon": "9388754506"}),
    ("unexpected", True),
]:
    invalid = dict(record, **{field: value})
    assert validate_jsonl(json.dumps(invalid), validator)[1], field
missing = dict(record)
del missing["publishers"]
assert validate_jsonl(json.dumps(missing), validator)[1]
for text in ["", "\n", "{}", "[]", "{", valid + "\n\n", valid.replace("288", "NaN")]:
    assert validate_jsonl(text, validator)[1], repr(text)
count, errors = validate_jsonl(valid + "\n{}", validator)
assert count == 2 and errors and all("line 2" in error for error in errors)
with patch("validate_jsonl.urlopen", side_effect=URLError("offline")):
    try:
        make_validator()
    except URLError:
        pass
    else:
        raise AssertionError("Network failure must not fall back to a cached schema")
print("PASS: valid batches, nested references, required fields, malformed JSONL, line reporting, and network failure")
