# Copilot instructions

## Project commands

Run commands from the `week4\tdd-ostoskori` project root.

- Install/sync the declared environment: `uv sync`
- Run the full test suite: `uv run pytest -q`
- Run one test: `uv run pytest -q src/tests/ostoskori_test.py::TestOstoskori::test_ostoskorin_hinta_ja_tavaroiden_maara_alussa`
- Run a test module: `uv run pytest -q src/tests/ostoskori_test.py`

The project has no configured lint or format command. Python support is pinned to 3.14 by `.python-version` and `pyproject.toml`.

## Architecture

This is a small Finnish-language shopping-cart domain model developed with TDD:

- `src/tuote.py` defines `Tuote`, the product value/entity with a name, unit price, and currently unused stock field.
- `src/ostos.py` defines `Ostos`, one cart line. It owns a product and quantity, clamps quantity at zero, and calculates the line total.
- `src/ostoskori.py` defines `Ostoskori`, the aggregate responsible for cart contents, item counts, total price, adding/removing products, clearing, and exposing purchases. Several methods are still scaffolding for upcoming exercises.
- `src/tests/ostoskori_test.py` contains the pytest-discovered tests, written with `unittest.TestCase` and `setUp`.
- `src/index.py` is only a placeholder; there is no application entry point or CLI.

The modules are intentionally flat rather than packaged: source files import siblings directly (`from tuote import Tuote`), and tests import source modules by name. Preserve this layout and run pytest from the project root using the declared `uv` environment.

## Code conventions

- Keep the public domain API and Finnish method/class names consistent with the existing interfaces (`Tuote`, `Ostos`, `Ostoskori`, `hinta`, `nimi`, `lisaa_tuote`, etc.).
- Domain state uses underscore-prefixed instance attributes (`_nimi`, `_hinta`, `_lukumaara`, `_saldo`) with small accessor methods rather than properties.
- Prices and quantities are represented as integers; `Ostos` starts with quantity `1`, and quantity changes must never leave it below `0`.
- Add behavior through focused tests in `src/tests/ostoskori_test.py`; retain the existing `unittest.TestCase` style even though pytest runs the suite.
- Keep imports compatible with the flat `src` layout. Avoid introducing package-relative imports unless the project is deliberately converted to a package and all callers/tests are updated together.
- Code of `src/ostos.py` and `src/tuote.py` should not be changed
- Tests should not be edited unless explicitly asked.
- Always implement absolutely minimal code that makes the tests pass
