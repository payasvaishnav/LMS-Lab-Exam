# LMS lab verification

Verified locally on 2026-11-02 with Docker Desktop, Python 3.13, pytest 9.2,
Selenium 4.52, and headless Chrome.

## d) Docker

`docker build -t lms-lab:latest .` completed successfully.

`docker run -d --name lms-lab -p 127.0.0.1:8080:5000 lms-lab:latest`
started container `0a9f9dd92fe8`.

```text
docker port lms-lab
5000/tcp -> 127.0.0.1:8080

docker inspect --format '{{.State.Status}} / {{.State.Health.Status}}' lms-lab
running / healthy
```

An HTTP request made inside the container to `/health` returned
`{"status":"ok"}`. `docker ps` confirmed the container and mapped port;
`docker logs` was also inspected with no errors reported.

## e) Fine tests and f) Selenium login tests

Executed `python -m pytest -v` against the running Docker app:

```text
tests/test_fine.py: 10 passed
tests/test_login.py::test_successful_login PASSED
tests/test_login.py::test_invalid_credentials PASSED
12 passed in 43.09s
```

The browser tests exercised the real HTTP login form through port 8080,
including dashboard redirection, the welcome message, and the invalid-login alert.
