# claude-plugins

Claude Code plugins and skills by Stavros Thalassinos. One marketplace, one folder per plugin.

## Add the marketplace

Inside Claude Code:

```
/plugin marketplace add stavthal/claude-plugins
```

## Plugins

| Plugin | Install | What it does |
| --- | --- | --- |
| [relay](plugins/relay) | `/plugin install relay@stavthal` | Sonnet leads, Haiku scouts read in parallel, Opus advises. A hook calls for the advisor when an error repeats. |

## Add a plugin

1. Put it in `plugins/<name>/` with its own `.claude-plugin/plugin.json`.
2. Add one entry to `.claude-plugin/marketplace.json` with `"source": "./plugins/<name>"`.
3. Add one row to the table above.
4. Run `claude plugin validate .` and `claude plugin validate plugins/<name>`.
