# Library Management System — Lab MVP

A minimal Python CLI with three seeded books, member registration, and issue/return.
Data is saved in `library.json` (ignored by Git). Intended for one local user.

```sh
python -m pip install -r requirements.txt
python lms.py books
python lms.py register "Asha"
python lms.py issue 1 1
python lms.py return 1
python lms.py members
```

Requires Python 3.10+. No web server, database setup, or third-party packages.
