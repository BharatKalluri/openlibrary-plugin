---
name: openlibrary-batch-import
description: Research book editions and prepare fully validated JSONL for the Open Library batch import UI. Use when adding books through batch imports or converting bibliographic sources into import records.
---

# Open Library batch imports

Prepare edition-specific JSONL for https://openlibrary.org/import/batch/new.

## Research

- Read the live [import guide](https://openlibrary.org/developers/imports) and [import schema](https://github.com/internetarchive/openlibrary-client/blob/master/olclient/schemata/import.schema.json).
- Read the supplied book pages, including embedded bibliographic metadata when visible text is incomplete. If access fails, say so and request source HTML or use another identifiable source; never claim to have read a blocked page.
- Identify the exact edition: title/subtitle, authors, publisher, publication date, format, language, pages, and identifiers. Keep Kindle, paperback, hardcover, translations, and reissues separate. Never borrow a paperback ISBN for an ebook or attach an ebook's Goodreads ID to a paperback.
- Check Open Library for an existing edition by title/author and identifiers. Report search results without treating absence from search as proof of absence.
- Omit uncertain optional metadata. Preserve provenance in `source_records` and source URLs in `links`, following the live schema. The first source record also identifies the queued item.

## Build a batch

Encourage users to collect many editions into one batch rather than submit one item at a time. Accumulate researched records in the same working JSONL file across the requested work, and offer to include other books they want to contribute. Honor a request for a single book without delaying it or expanding the scope on your own.

## Mandatory validation before sharing

1. Save the complete candidate batch as a UTF-8 `.jsonl` file, one JSON object per physical line. No enclosing array, Markdown fences, or blank lines.
2. Locate this installed skill’s directory and run its bundled Python validator on that exact file. For local environments with `uv`:

   ```sh
   uv run <skill-directory>/scripts/validate_jsonl.py /absolute/path/books.jsonl
   ```

   Replace `<skill-directory>` with this installed skill's absolute directory, including when installed inside a plugin. The script declares its `jsonschema>=4.22,<5` dependency for `uv` and requires Python 3.10+. If the execution environment already supplies compatible `jsonschema` and `referencing` packages, use the same script directly:

   ```sh
   python3 <skill-directory>/scripts/validate_jsonl.py /absolute/path/books.jsonl
   ```

   Check the actual execution environment: desktop Chat may run code remotely. Use the host's supported dependency setup when necessary; do not ask a nontechnical user to run shell commands on their computer to fix a remote environment. If Python, dependencies, or network access are unavailable, explain the limitation and withhold import JSON. The script fetches the live official schema and follows external references on every invocation. Nothing is validated against a bundled schema snapshot.
3. Require exit code 0 before sharing any import JSON, JSONL attachment, or copy/paste block. If fetching or validation fails, fix the issue and rerun. Do not substitute a required-field check, manual inspection, or a cached schema for full validation.
4. Validate every record. Any edit after validation invalidates the result: rerun on the final file. If pasting JSONL in chat, reproduce the validated file exactly.

Schema validation checks shape and types, not bibliographic truth, ISBN checksums, or every server policy. Verify edition facts against sources and check ISBN checksums/consistency when present. Do not claim live acceptance from local validation.

## Review and deliver

Thoroughly review every record against its sources before it goes to the import pipeline: check edition identity, identifiers, dates, publisher, language, format, page count, duplicate records, and any conflicting evidence. Resolve conflicts or omit uncertain optional fields; do not submit records with unresolved required metadata.

Alongside the validated file or its exact JSONL, provide a human-readable table generated from the final validated records. Include one row per edition with title, author, publisher, date, format, language, pages, ISBNs/other identifiers, and source links. Use an em dash for missing optional values; do not fill gaps with guesses. State the validation result and flag any remaining optional omissions for review.

Explain that ordinary account submissions wait for review. Preparing an import does not authorize submitting it; submit only when the user asks, after the reviewed final file passes validation again if it changed.
