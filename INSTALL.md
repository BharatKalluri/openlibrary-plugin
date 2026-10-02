# Install

## Recommended: skills CLI

```sh
npx skills add BharatKalluri/openlibrary-skills
```

Follow the installer prompts to choose your agent and installation options. The command installs into the current project by default. For availability across projects, add `--global`:

```sh
npx skills add BharatKalluri/openlibrary-skills --global
```

You need Node.js/npm to run `npx`, internet access, and [uv](https://docs.astral.sh/uv/getting-started/installation/) for the Python validator. The validator declares its dependencies and requires Python 3.10+.

## Use the skill

Invoke `$openlibrary-batch-import` in Codex or `/openlibrary-batch-import` in Claude Code, followed by your book links. The agent can also select the skill when your request matches its description. Start a new session if it does not appear.

Example request:

> Prepare an Open Library import batch for these book links. Research the exact editions, validate the final JSONL, and show me a readable table before I submit it.

Validation fetches the official schema and its references live on every run. Network or validation failures block delivery. Local validation does not guarantee Open Library acceptance, and the skill does not submit imports automatically.

## ChatGPT desktop UI

ChatGPT supports installing skills bundled as plugins through the Plugins Directory. This repository currently distributes a standalone skill, not a plugin, so it is not yet available for direct installation through that UI. Use the recommended CLI method for local Codex installation.

See the [skills CLI](https://github.com/vercel-labs/skills), [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills), and [Claude Code skills documentation](https://code.claude.com/docs/en/skills). For desktop UI distribution, see [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins).
