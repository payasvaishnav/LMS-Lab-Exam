# Library Management System — Lab MVP

A minimal Python CLI with three seeded books, member registration, and issue/return.
Data is saved in `library.json` (ignored by Git). Intended for one local user.

```sh
python -m pip install -r requirements.txt
python lms.py books
python lms.py search "python"
python lms.py register "Asha"
python lms.py issue 1 1
python lms.py return 1
python lms.py members
```

Requires Python 3.10+. The CLI uses the standard library; the web login demo uses Flask and Waitress.

## Git branch exercise

The initial project was committed on `main`. Book search was added and committed
on `feature/book-search`, then merged into `main` with a merge commit.
Display the commit history with:

```sh
git log --oneline --graph --decorate --all
```

## GitHub Actions

`.github/workflows/python-script.yml` runs on every push to `main` and can also
be started manually from the Actions tab. It sets up Python 3.13, installs
`requirements.txt`, and runs `python lms.py search "python"`. The final step
always displays the job status in the logs and the run summary.

This project is connected to https://github.com/payasvaishnav/LMS-Lab-Exam.
Push changes to run the workflow:

```sh
git push -u origin main
git push -u origin feature/book-search
```

Open the repository's **Actions** tab, select **Run Python script**, and open
the latest run to see its execution status and step logs.

## d) Docker build, run, and status

The image runs the web login and seeded book-search demo on container port 5000.
The existing CLI remains available with `docker exec lms-lab python lms.py books`.
The web demo uses an in-memory seed catalog; CLI changes are stored separately.

```sh
docker build -t lms-lab:latest .
docker run -d --name lms-lab -p 127.0.0.1:8080:5000 lms-lab:latest
docker images lms-lab
docker ps --filter name=lms-lab
docker inspect --format '{{.State.Status}} / {{.State.Health.Status}}' lms-lab
docker port lms-lab
docker logs lms-lab
docker exec lms-lab python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health').read().decode())"
```

Open http://localhost:8080. Lab credentials: `admin` / `library123`.
These are demonstration credentials, configurable with the container environment
variables `LMS_USERNAME` and `LMS_PASSWORD`; `LMS_SECRET_KEY` configures sessions.
Stop the container after the demonstration with `docker stop lms-lab`.

## e) Fine calculation and parametrized pytest cases

`lms.calculate_fine(overdue_days)` charges Rs 5 per whole overdue day with no
grace period or cap. Zero days gives zero fine; one day is the first charged
boundary. Negative days raise `ValueError`; non-integers (including booleans)
raise `TypeError`.

```sh
python -m pip install -r requirements-dev.txt
python -m pytest tests/test_fine.py -v
```

The 10 parametrized cases use assertions and `pytest.raises` to cover zero,
valid inputs, both sides of the zero/one boundary, negatives, and invalid types.

## f) Selenium login automation

Keep the Docker container running, install the development dependencies above,
and run with Chrome installed:

```sh
python -m pytest tests/test_login.py -v
```

The two tests use ID, name, and CSS locators plus `WebDriverWait` with explicit
visibility, clickability, and URL conditions. They assert the successful welcome
message and the exact invalid-credentials message. Each test uses a fresh
headless browser and always closes it. Selenium Manager obtains the driver.
Set `LMS_BROWSER=edge` to use Edge, or `LMS_BASE_URL` for a different server URL.
Tests use `LMS_USERNAME` and `LMS_PASSWORD` if demo credentials are overridden.

Run all 12 cases against the running container with `python -m pytest -v`.
