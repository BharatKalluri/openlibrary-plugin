#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema>=4.22,<5"]
# ///
"""Check live portable manifest schema and shared plugin/skill paths."""
import json
from pathlib import Path
from urllib.request import urlopen
from jsonschema.validators import validator_for

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "plugin.json").read_text())
with urlopen(manifest["$schema"], timeout=30) as response:
    schema = json.load(response)
validator = validator_for(schema)
validator.check_schema(schema)
validator(schema).validate(manifest)
claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
assert (claude["name"], claude["version"]) == (manifest["name"], manifest["version"])
for path in (".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"):
    catalog = json.loads((root / path).read_text())
    assert len(catalog["plugins"]) == 1
    entry = catalog["plugins"][0]
    assert entry["name"] == manifest["name"]
    source = entry["source"]
    relative = source if isinstance(source, str) else source["path"]
    assert relative.startswith("./")
    assert (root / relative).resolve() == root
skill = root / "skills/openlibrary-batch-import"
for path in ("SKILL.md", "scripts/validate_jsonl.py", "scripts/test_validate_jsonl.py"):
    assert (skill / path).is_file(), path
print("PASS: live portable manifest schema; both catalogs resolve the same skill and scripts")
