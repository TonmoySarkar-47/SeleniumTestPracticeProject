from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Ensure you have a secret key for sessions

# Mock user data
users = {"admin": "admin"}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("feature"))
        else:
            error = "Invalid credentials, please try again."
            return render_template("login.html", error=error)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)  # Remove user from session on logout
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("feature"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Allow only admin to reset password
        if username == "admin":
            users[username] = password  # Update the password for the admin user
            success_message = "Password reset successful! You can now log in with your new password."
            return render_template("forgot_password.html", success_message=success_message)
        else:
            error = "Only 'admin' can reset the password."
            return render_template("forgot_password.html", error=error)

    return render_template("forgot_password.html")


@app.route("/feature", methods=["GET", "POST"])
def feature():
    if "user" not in session:
        return redirect(url_for("login"))

    transformed_text = None
    rating = None
    feedback = None

    if request.method == "POST":
        action = request.form.get("action")  # Safely get action value
        text = request.form.get("text")
        transformation = request.form.get("transformation")

        if action == "transform" and text:  # Handle text transformation
            if transformation == "uppercase":
                transformed_text = text.upper()
            elif transformation == "lowercase":
                transformed_text = text.lower()
            elif transformation == "reverse":
                transformed_text = text[::-1]
            session['given_text'] = text
            session['transformed_text'] = transformed_text

        elif action == "submit":  # Handle rating and feedback
            rating = request.form.get("rating")  # Safely get rating
            feedback = request.form.get("feedback")  # Safely get feedback

            # Store them in session
            session['rating'] = rating
            session['feedback'] = feedback

            return redirect(url_for("result"))

    return render_template("feature.html", transformed_text=session.get('transformed_text'))

@app.route("/result")
def result():
    given_text = session.get("given_text")
    transformed_text = session.get("transformed_text")
    rating = session.get("rating")
    feedback = session.get("feedback")
    session.pop('given_text', None)
    session.pop('transformed_text', None)
    session.pop('rating', None)
    session.pop('feedback', None)
    return render_template("result.html", given_text=given_text, transformed_text=transformed_text, rating=rating, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
