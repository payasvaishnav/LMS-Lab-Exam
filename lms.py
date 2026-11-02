"""Small library CLI. Run python lms.py --help for commands."""
import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("library.json")


def new_library():
    return {"books": [
        {"id": 1, "title": "Clean Code", "author": "Robert Martin", "member_id": None},
        {"id": 2, "title": "Python Crash Course", "author": "Eric", "member_id": None},
        {"id": 3, "title": "The Pragmatic Programmer", "author": "Andrew ", "member_id": None},
    ], "members": []}


def register_member(data, name):
    name = name.strip()
    if not name:
        raise ValueError("Member name cannot be empty")
    member = {"id": max((m["id"] for m in data["members"]), default=0) + 1, "name": name}
    data["members"].append(member)
    return member


def issue_book(data, book_id, member_id):
    if not any(m["id"] == member_id for m in data["members"]):
        raise ValueError("Member not found")
    book = find_book(data, book_id)

    if book["member_id"] is not None:
        raise ValueError("Book is already issued")
    book["member_id"] = member_id
    return book


def find_book(data, book_id):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    raise ValueError("Book not found")


def search_books(data, query):
    query = query.strip().casefold()
    if not query:
        raise ValueError("Search query cannot be empty")
    return [book for book in data["books"]
            if query in book["title"].casefold() or query in book["author"].casefold()]


def return_book(data, book_id):
    book = find_book(data, book_id)
    if book["member_id"] is None:
        raise ValueError("Book is not issued")
    book["member_id"] = None
    return book


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("books", help="List books")
    commands.add_parser("search", help="Search books by title or author").add_argument("query")
    commands.add_parser("members", help="List registered members")
    commands.add_parser("register", help="Register member").add_argument("name")
    issue = commands.add_parser("issue", help="Issue an available book")
    issue.add_argument("book_id", type=int)
    issue.add_argument("member_id", type=int)
    commands.add_parser("return", help="Return a book").add_argument("book_id", type=int)
    args = parser.parse_args()
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else new_library()
        if args.command == "books":
            result = data["books"]
        elif args.command == "search":
            result = search_books(data, args.query)
        elif args.command == "members":
            result = data["members"]
        elif args.command == "register":
            result = register_member(data, args.name)
        elif args.command == "issue":
            result = issue_book(data, args.book_id, args.member_id)
        else:
            result = return_book(data, args.book_id)
        if args.command in {"register", "issue", "return"}:
            DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
