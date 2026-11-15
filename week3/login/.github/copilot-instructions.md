# Copilot instructions

## Project overview

This is a small Flask login and registration application for the Ohtu course. Run commands from `week3/login`.

- `src/index.py` is the development entry point; it imports the Flask app from `src/app.py` and serves it on `0.0.0.0:5001`.
- `src/app.py` owns the HTTP routes and rendering. GET routes render templates, while POST handlers delegate authentication or registration to the service and use Flask flash messages plus redirects for errors.
- `src/services/user_service.py` contains validation and authentication rules. It receives a repository dependency, with the module-level `user_service` using the module-level `user_repository`.
- `src/repositories/user_repository.py` stores `User` objects in memory. There is no database or persistence between process runs; `/tests/reset` clears this state for acceptance tests.
- `src/templates/` contains Jinja templates. `layout.html` is the shared base template; the other pages extend it.
- `src/tests/` contains Robot Framework browser acceptance tests. `resource.robot` defines browser setup, URLs, and shared keywords. `AppLibrary.py` provides HTTP helpers used by the suites.

## Commands

Dependencies are managed with `uv` using `pyproject.toml` and `uv.lock`.

### Run the application

```powershell
uv run python src/index.py
```

The application is then available at `http://localhost:5001`.

### Run browser tests

Run the complete acceptance-test suite:

```powershell
uv run robot --variable HEADLESS:true src/tests
```

Run one suite:

```powershell
uv run robot --variable HEADLESS:true src/tests/login.robot
```

Run one test case by name:

```powershell
uv run robot --variable HEADLESS:true --test "Login With Correct Credentials" src/tests/login.robot
```

The Flask server must be running on port 5001 before running Robot tests. If the Browser library has not been initialized in the environment, initialize its browser dependencies once with:

```powershell
uv run rfbrowser init
```

There is no build or lint command configured in `pyproject.toml`.

## Repository-specific conventions

- Keep application imports and test paths aligned with the current `src` layout. The entry point is run as `python src/index.py`, while the app imports top-level packages such as `repositories` and `services`.
- Preserve the service/repository split: route handlers should handle HTTP concerns, `UserService` should handle validation/authentication, and `UserRepository` should handle user storage.
- Acceptance tests assume a clean in-memory repository. Use `POST /tests/reset` through the existing `Reset Application` keyword rather than adding ad hoc cleanup in individual tests.
- Browser tests use the shared keywords in `resource.robot`, the `${HEADLESS}` variable, and the fixed server URL `localhost:5001`. Prefer extending those shared resources over duplicating setup.
- User-facing validation and authentication errors are surfaced through `flash()` and asserted from the rendered login or registration page. Keep error text stable when changing validation behavior.
- The repository currently uses module-level `user_repository` and `user_service` instances; tests and route code rely on that shared state.
