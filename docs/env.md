# Environment Variables

This project uses environment variables for credentials and configuration.
**Names are documented here; values are never committed.**

Copy the variable list to a `.env` file at the repo root and populate values.
`.env` is gitignored.

## Currently required

*None.* No data source added so far requires credentials.

## Reserved (will be populated as Phase 1 sources are added)

| Variable          | Used by                | Notes                                  |
|-------------------|------------------------|----------------------------------------|
| `NOAA_TOKEN`      | NOAA CDO API           | Free token, register at NOAA CDO site  |
| `FCC_API_KEY`     | FCC Form 477 endpoints | If REST API path is used               |

When a new env var is introduced, add a row above and reference it in the
fetcher module docstring.
