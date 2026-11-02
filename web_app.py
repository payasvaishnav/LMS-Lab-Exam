"""Local lab login demonstration. Demo credentials: admin / library123."""
import hmac
import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for

from lms import new_library, search_books

app = Flask(__name__)
app.secret_key = os.environ.get("LMS_SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        expected_user = os.environ.get("LMS_USERNAME", "admin")
        expected_password = os.environ.get("LMS_PASSWORD", "library123")
        if (hmac.compare_digest(username.encode(), expected_user.encode())
                and hmac.compare_digest(password.encode(), expected_password.encode())):
            session.clear()
            session["username"] = username
            return redirect(url_for("dashboard"))
        error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.get("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    query = request.args.get("q", "").strip()
    data = new_library()
    books = search_books(data, query) if query else data["books"]
    return render_template("dashboard.html", username=session["username"], books=books, query=query)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
