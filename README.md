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

Requires Python 3.10+. No web server, database setup, or third-party packages.

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

To run it on GitHub, create an empty GitHub repository, then use its URL:

```sh
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
git push -u origin feature/book-search
```

Open the repository's **Actions** tab, select **Run Python script**, and open
the latest run to see its execution status and step logs. No GitHub remote
was configured when this exercise was prepared, so no hosted run is recorded yet.
