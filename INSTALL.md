# Install

This skill runs locally in Codex or Claude Code. It needs internet access and [uv](https://docs.astral.sh/uv/getting-started/installation/), which manages the Python dependency used by the validator.

## Ask your agent to install it

Paste this into Codex or Claude Code:

> Install the openlibrary-batch-import skill from https://github.com/BharatKalluri/openlibrary-skills, under skills/openlibrary-batch-import. Install the complete folder, including scripts, into your personal skills directory: ~/.agents/skills for Codex or ~/.claude/skills for Claude Code. Check that uv and Python 3.10+ are available, run scripts/test_validate_jsonl.py with uv, and verify that the skill is discoverable. Do not overwrite an existing installation without checking it first.

In Codex, you can also ask `$skill-installer` to install the skill from that repository and path.

## Install manually

Clone the repository into a directory of your choice:

```sh
git clone https://github.com/BharatKalluri/openlibrary-skills.git
cd openlibrary-skills
```

For Codex:

```sh
mkdir -p ~/.agents/skills
cp -R -n skills/openlibrary-batch-import ~/.agents/skills/
```

For Claude Code:

```sh
mkdir -p ~/.claude/skills
cp -R -n skills/openlibrary-batch-import ~/.claude/skills/
```

These commands are for macOS/Linux. If the destination already exists, inspect it before updating it. Copy the complete folder to the equivalent destination on Windows.

Run the checks from the cloned repository:

```sh
uv run skills/openlibrary-batch-import/scripts/test_validate_jsonl.py
```

Start a new agent session if the skill does not appear. Invoke `$openlibrary-batch-import` in Codex or `/openlibrary-batch-import` in Claude Code, followed by your book links. The agent can also select the skill when your request matches its description.

Example request:

> Prepare an Open Library import batch for these book links. Research the exact editions, validate the final JSONL, and show me a readable table before I submit it.

Validation fetches the official schema and its references live on every run. Network or validation failures block delivery. Local validation does not guarantee Open Library acceptance, and the skill does not submit imports automatically.

See the official [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills documentation](https://code.claude.com/docs/en/skills) for installation locations and discovery behavior.
