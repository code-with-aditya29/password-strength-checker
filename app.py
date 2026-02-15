# Import Flask class and required functions
from flask import Flask, render_template, request

# re = Regular Expression library (used to check patterns like uppercase, numbers etc.)
import re

# math library is used for entropy calculation (log2 function)
import math


# Create Flask application object
app = Flask(__name__)


# ---------------------------------------------------------
# FUNCTION 1: Calculate Entropy
# ---------------------------------------------------------
def calculate_entropy(password):
    """
    This function calculates how unpredictable (random) the password is.
    Higher entropy = harder to crack using brute force attack.
    """

    # This variable stores total character set size
    charset = 0

    # Check if password contains lowercase letters
    if re.search(r"[a-z]", password):
        charset += 26  # 26 lowercase letters

    # Check if password contains uppercase letters
    if re.search(r"[A-Z]", password):
        charset += 26  # 26 uppercase letters

    # Check if password contains digits
    if re.search(r"[0-9]", password):
        charset += 10  # 10 digits (0-9)

    # Check if password contains special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32  # Approximate special characters count

    # If no valid characters found
    if charset == 0:
        return 0

    # Entropy Formula:
    # entropy = length of password × log2(character set size)
    entropy = len(password) * math.log2(charset)

    # Round to 2 decimal places
    return round(entropy, 2)


# ---------------------------------------------------------
# FUNCTION 2: Classify Strength
# ---------------------------------------------------------
def check_strength(password):
    """
    This function calls entropy function
    and decides if password is Weak / Moderate / Strong
    """

    # Calculate entropy first
    entropy = calculate_entropy(password)

    # Basic classification logic
    if entropy < 28:
        return "Weak", entropy
    elif entropy < 60:
        return "Moderate", entropy
    else:
        return "Strong", entropy


# ---------------------------------------------------------
# ROUTE: Home Page
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    # Default values before user submits form
    strength = None
    entropy = None

    # If user submits form (POST request)
    if request.method == "POST":

        # Get password from HTML form
        password = request.form["password"]

        # Check its strength
        strength, entropy = check_strength(password)

    # Send result back to HTML page
    return render_template("index.html", strength=strength, entropy=entropy)


# ---------------------------------------------------------
# Run Flask App
# ---------------------------------------------------------
if __name__ == "__main__":
    # debug=True means auto-reload on changes
    app.run(debug=True)
