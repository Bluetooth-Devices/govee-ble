# CLAUDE.md

Guidance for Claude Code (and other AI agents) working in this repository.

## What this library does

`govee-ble` parses BLE advertisement payloads from Govee sensors (thermometers,
hygrometers, motion/door/vibration sensors, presence sensors, BBQ probes, air
quality monitors, etc.) and exposes the readings as `SensorUpdate` objects from
`sensor-state-data`. It is consumed by Home Assistant's `govee_ble` integration.

The library is **stateless across packets** beyond the per-device accumulator
that `bluetooth-sensor-state-data.BluetoothData` provides. It does not poll, it
does not connect — it only decodes raw advertisement bytes.

## Layout

```
src/govee_ble/
├── __init__.py        # Public re-exports (GoveeBluetoothDeviceData, SensorType, …)
└── parser.py          # All decoding logic + GoveeBluetoothDeviceData class
tests/
└── test_parser.py     # Single fixture-driven test file (~5800 lines)
```

Everything device-specific lives in `parser.py::GoveeBluetoothDeviceData._process_mfr_data`.
Each model is a branch keyed off `(msg_length, local_name | mgr_id | service_uuid)`.
When adding a model, follow the existing pattern — don't refactor the dispatch
into a registry just to be tidy; the linear branches are intentionally easy to
diff against device captures.

## Commands

```bash
poetry install                    # install (incl. dev deps)
poetry run pytest                 # run tests with coverage
poetry run pytest tests/test_parser.py::test_h5075 -v   # single test
poetry run pre-commit run -a      # full lint pass (ruff, mypy, flake8, codespell, …)
```

`make` is not used here — Poetry + pre-commit only.

## Conventions

- **Python 3.10+** (`from __future__ import annotations` everywhere).
  `pyupgrade --py310-plus` runs in pre-commit.
- **Line length: 88** (ruff default). `.flake8` allows 120 but ruff-format
  rewrites to 88, so write to 88. Long log/error strings that ruff leaves alone
  are the only exception.
- **Type hints required** on all non-test code (`disallow_untyped_defs = true`
  in mypy strict config). Tests are exempt.
- **Conventional Commits** are enforced by commitlint in CI and by commitizen
  in pre-commit. Use `feat:`, `fix:`, `chore:`, `test:`, `docs:`, `refactor:`.
  The `release` job on `main` runs python-semantic-release — a `feat:` bumps
  minor, a `fix:` bumps patch, and any merge to `main` may publish to PyPI.
  Be deliberate about commit prefixes.
- **Branch naming for AI agents**: always `koan/<short-description>`. Never
  push to `main`, never merge.

## Testing rules

- Tests live in one file (`tests/test_parser.py`). When adding a model, add a
  test next to the closest existing one — keep tests grouped by model.
- Use real captured advertisement bytes wherever possible. The test file is
  largely "feed these bytes, assert this `SensorUpdate`" — mirror that style.
- `BluetoothServiceInfo` is the input type. Construct it with the same kwargs
  the existing tests use; don't invent helpers for one-off cases.
- Coverage is reported on every PR via codecov. New parser branches without
  tests will fail `codecov/patch`.

## CI gates a PR must pass

1. `pre-commit.ci` — ruff, ruff-format, flake8, mypy, codespell, pyupgrade,
   prettier, commitizen, plus the standard pre-commit-hooks.
2. `Lint Commit Messages` — commitlint, conventional commits.
3. `test (3.10 / 3.11 / 3.12 / 3.13 / 3.14, ubuntu-latest)` — full pytest.
4. `codecov/patch` and `codecov/project` — coverage thresholds.

If pre-commit autofixes are needed, the `pre-commit.ci` bot pushes them as
`chore(pre-commit.ci): auto fixes` — don't fight that, just rebase.

## Adding support for a new Govee model

1. Capture raw advertisement bytes (BLE sniffer or HA debug log).
2. Add a branch in `_process_mfr_data` matched by `msg_length` plus
   `local_name`/`mgr_id`/service UUID, following the closest existing model.
3. If it has buttons / motion / sleepy power profile, add an entry to
   `_MODEL_DB` in `parser.py` with the right `SensorType`.
4. Add a fixture-driven test in `tests/test_parser.py`. Include both a
   "valid reading" and an "out-of-range/error flag" case if the device
   reports an error bit.
5. Run `poetry run pytest -k <model>` then `poetry run pre-commit run -a`.

## Things not to do

- Don't introduce stateful logic in the parser without an explicit reason —
  the library is consumed by Home Assistant and the parser is expected to be
  pure per-packet. State that filters or smooths readings belongs upstream.
- Don't refactor the model dispatch into a registry/decorator pattern. The
  linear `if msg_length == X` branches are deliberately easy to grep and to
  diff against new device captures.
- Don't touch `CHANGELOG.md` by hand — semantic-release owns it.
- Don't bump the version in `pyproject.toml` or `__init__.py` — semantic-release
  owns those too (see `[tool.semantic_release]`).
