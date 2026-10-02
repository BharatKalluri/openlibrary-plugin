# Install

## Claude Desktop

On a paid Claude plan with plugins enabled:

1. Open **Customize → Plugins**.
2. Select **Add → Add marketplace → Add from a repository**.
3. Enter `BharatKalluri/openlibrary-skills` and add the marketplace.
4. Open **Open Library** and add the plugin.
5. Start a new conversation and provide your book links.

These steps follow [Claude’s repository installation guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude). Organization settings may restrict installation. Skills need code execution enabled.

The package is ready for this installation route; end-to-end validation in Claude Desktop Chat and Cowork has not yet been tested. Installation alone does not establish that a particular environment can execute Python or fetch the live schema. If it cannot validate, the skill must explain the limitation and withhold import JSON.

## Recommended for technical users: skills CLI

```sh
npx skills add BharatKalluri/openlibrary-skills
```

Follow the prompts to choose your agent. Installs apply to the current project by default; add `--global` for availability across projects. You need Node.js/npm, internet access, and Python 3.10+ with [uv](https://docs.astral.sh/uv/getting-started/installation/) or compatible Python dependencies already available.

Use `$openlibrary-batch-import` in Codex or `/openlibrary-batch-import` in Claude Code. Start a new session if the skill does not appear. Install either the standalone skill or plugin for a given agent to avoid duplicate workflows.

## Claude Code plugin

As an alternative to the skills CLI:

```text
/plugin marketplace add BharatKalluri/openlibrary-skills
/plugin install openlibrary-skills@openlibrary-skills
```

Use `/openlibrary-skills:openlibrary-batch-import` or ask naturally for an Open Library batch.

## Codex plugin

Register the marketplace:

```sh
codex plugin marketplace add BharatKalluri/openlibrary-skills
```

Open the Plugins Directory, choose **Open Library**, and install the plugin. Alternatively, with a CLI supporting plugin installation:

```sh
codex plugin add openlibrary-skills@openlibrary-skills
```

Start a new session. Local marketplace setup follows [OpenAI’s packaging guide](https://developers.openai.com/plugins/build/plugins).

## ChatGPT desktop

The repository includes an OpenAI-compatible plugin package. Local marketplaces support testing in supported Work/Codex surfaces, but this plugin is **not published in ChatGPT’s public Plugins Directory**. Public installation requires separate submission and approval; see [OpenAI’s submission guide](https://developers.openai.com/plugins/guides/submit-claude-plugin). Ordinary Chat and Work execution have not yet been tested.

## Use it

> Prepare an Open Library import batch for these book links. Research the exact editions, validate the final JSONL, and show me a readable table before I submit it.

The agent runs the bundled Python validator. It fetches the official schema and its references live on every run. With `uv` it manages the declared dependencies; an environment already providing compatible packages can run the script directly with `python3`. No cached-schema fallback is allowed.

Local validation does not guarantee Open Library acceptance. Review the edition table before submission. The skill does not submit imports automatically.

## Verification status

- Passed: Claude plugin and marketplace validation, live portable manifest schema validation, skills CLI discovery and temporary project installation, Codex marketplace registration and plugin installation, and live-schema validator checks from both installed copies.
- Pending: fresh conversational sessions in Codex, Claude Desktop Chat, Claude Cowork, and ChatGPT Work/Chat. No desktop UI screenshots or public-directory approval are claimed.

## Package checks

From a checkout:

```sh
uv run scripts/test_packaging.py
uv run skills/openlibrary-batch-import/scripts/test_validate_jsonl.py
npx skills add . --list
```

Release ZIPs contain both manifests and the same skill files used by the skills CLI. They can be used to prepare a skills-only OpenAI submission; a GitHub release is not a public-directory approval.
