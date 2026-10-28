"""
app.py - A minimal Flask REST API.

Endpoints:
    GET  /hello  -> returns a JSON greeting (optional ?name= query parameter)
    POST /sum    -> receives {"numbers": [1, 2, 3]} and returns their sum

Run with:  python app.py   (server starts on http://127.0.0.1:5000)
"""

from flask import Flask, jsonify, request

# Create the Flask application object.
app = Flask(__name__)


# Helper function: True if value is an int or float (but not True/False).
def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# ---------------- Route 1: GET /hello ----------------
@app.route("/hello", methods=["GET"])
def hello():
    """Return a greeting. Uses ?name=... if given, otherwise 'World'."""
    # request.args holds the query string parameters as a dictionary.
    name = request.args.get("name", "").strip()

    # if/else control flow: fall back to a default when no name is supplied.
    if name:
        message = f"Hello, {name}!"
    else:
        message = "Hello, World!"

    # jsonify turns a Python dictionary into a JSON response.
    return jsonify({"message": message}), 200


# ---------------- Route 2: POST /sum ----------------
@app.route("/sum", methods=["POST"])
def sum_numbers():
    """Add up a list of numbers sent as JSON: {"numbers": [1, 2, 3]}."""
    # silent=True returns None instead of crashing if the body isn't valid JSON.
    data = request.get_json(silent=True)

    # Error handling (step 5): return 400 for bad input.
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    if "numbers" not in data:
        return jsonify({"error": "Missing required field: 'numbers'."}), 400

    numbers = data["numbers"]

    if not isinstance(numbers, list):
        return jsonify({"error": "'numbers' must be a list."}), 400

    # List comprehension: collect any items that aren't numbers.
    invalid_items = [item for item in numbers if not is_number(item)]
    if invalid_items:
        return jsonify({
            "error": "All items in 'numbers' must be numeric.",
            "invalid_items": invalid_items,
        }), 400

    # Input is valid: the built-in sum() adds every value in the list.
    total = sum(numbers)
    return jsonify({"numbers": numbers, "count": len(numbers), "sum": total}), 200


# ---------------- JSON error pages ----------------
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request."}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found."}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed for this endpoint."}), 405


# Entry point: lets the app run with the single command `python app.py`.
if
