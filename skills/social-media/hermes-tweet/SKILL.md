---
name: hermes-tweet
description: "Use when Hermes Agent needs the Hermes Tweet plugin for X/Twitter search, social listening, account reads, or approval-gated account actions."
version: 1.0.0
author: Xquik-dev
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [hermes]
metadata:
  hermes:
    tags: [hermes-agent, twitter, x, social-media, plugin]
audience: user
---

# Hermes Tweet

Use Hermes Tweet when the user asks for native Hermes Agent access to X/Twitter
workflows, social listening, account reads, trend checks, monitors, publishing,
replies, likes, reposts, DMs, or media operations.

Use `xurl` instead when the user explicitly wants the X developer CLI. Use
Hermes Tweet when the task should stay inside Hermes plugin tools.

## Install

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

If the plugin is installed but hidden, enable it:

```bash
hermes plugins enable hermes-tweet
```

## Configure

Set `XQUIK_API_KEY` only in the Hermes runtime environment or `~/.hermes/.env`.
Do not paste keys into prompts, logs, issues, or pull requests.

Keep actions off for research sessions:

```bash
export HERMES_TWEET_ENABLE_ACTIONS=false
```

Set `HERMES_TWEET_ENABLE_ACTIONS=true` only for sessions where the user has
asked for account-changing work.

## Tool Order

1. Call `tweet_explore` first to find the catalog endpoint.
2. Use `tweet_read` for read-only paths such as search, profiles, trends,
   monitors, media metadata, and account context.
3. Use `tweet_action` only after showing the exact endpoint and payload for a
   user-approved write, private read, monitor change, media upload, draw, or
   webhook operation.

## Verification

```bash
hermes tools list
hermes -z "Use tweet_explore to find account status routes. Do not call tweet_action." --toolsets hermes-tweet
```

Expected safe state:

- `tweet_explore` is available without an API key.
- `tweet_read` appears after `XQUIK_API_KEY` is configured.
- `tweet_action` stays hidden or disabled unless actions are explicitly enabled.

Source: https://github.com/Xquik-dev/hermes-tweet
