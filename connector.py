import os
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

from backend.auth import UserAccount
from backend.customers import Customers
from backend.booking import Booking
from backend.parcel import Parcel
from backend.reports import Reports
from backend.checkin import OnlineCheckIn
from backend.tickets import Tickets
from backend.messages import Messages

app = Flask(
    __name__,
    template_folder="Frontent",
    static_folder="Frontent",
    static_url_path="/static",
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)


FORM_NAMES = {
    "login", "register", "customer", "Flight Booking", "Parcel Sending",
    "Ticket Checking", "Report Issue", "Get Newsletter", "Contact",
    "Online CheckIn",
}


def show_result(message, back_url=None, success=True, status=200):
    return render_template(
        "result.html", message=message, back_url=back_url or url_for("home"),
        success=success
    ), status


def render_form(form_name, error=None, status=200):
    return render_template("customer_index.html", form_name=form_name, error=error), status


def clean(name):
    return request.form.get(name, "").strip()


@app.route("/")
def home():
    return render_template("main_index.html")


@app.route("/forms/<form_name>")
def show_form(form_name):
    if form_name not in FORM_NAMES:
        return show_result("That form could not be found.", url_for("home"), False, 404)
    return render_form(form_name)


# Compatibility route for older links.
@app.route("/customer_index/login")
def legacy_login_form():
    return redirect(url_for("show_form", form_name="login"))


@app.route("/signin")
def signin():
    return render_template("signIn.html")


@app.route("/customer")
def customer():
    if "login_id" not in session:
        return redirect(url_for("show_form", form_name="login"))
    if session.get("role") != "customer":
        return show_result("Access denied: this page is for customers only.",
                           url_for("home"), False, 403)
    return render_template("cards.html")


@app.route("/employee")
def employee():
    if "login_id" not in session:
        return redirect(url_for("show_form", form_name="login"))
    if session.get("role") != "employee":
        return show_result("Access denied: employees only.",
                           url_for("home"), False, 403)
    return render_template("employee_index.html")


@app.route("/admin")
def admin():
    if "login_id" not in session:
        return redirect(url_for("show_form", form_name="login"))
    if session.get("role") != "admin":
        return show_result("Access denied: administrators only.",
                           url_for("home"), False, 403)
    return render_template("admin.html")


@app.route("/customer-registration")
def customer_registration():
    return render_form("customer")


@app.route("/login", methods=["POST"])
def login():
    username_or_email = clean("email")
    password = request.form.get("password", "")

    if not username_or_email or not password:
        return render_form("login", "Enter your username/email and password.", 400)

    try:
        user = UserAccount.authenticate(username_or_email, password)
    except mysql.connector.Error:
        app.logger.exception("Login database error")
        return render_form("login", "Unable to verify login. Check the database connection.", 500)

    if not user:
        return render_form("login", "Incorrect username/email or password.", 401)

    session.clear()
    session["login_id"] = user["Login_ID"]
    session["username"] = user["Username"]
    session["role"] = user["User_Role"]

    destinations = {
        "admin": "admin",
        "employee": "employee",
        "customer": "customer",
    }
    return redirect(url_for(destinations[user["User_Role"]]))


@app.route("/register-account", methods=["POST"])
def register_account():
    username = clean("username")
    email = clean("email")
    password = request.form.get("password", "")

    if not username or not email or not password:
        return render_form("register", "Complete all account fields.", 400)
    if len(password) < 6:
        return render_form("register", "Use a password of at least 6 characters.", 400)

    try:
        UserAccount.create(username, email, password, role="customer")
        return show_result(
            "Your customer login account was created successfully. You can now sign in.",
            url_for("show_form", form_name="login")
        )
    except mysql.connector.IntegrityError:
        return render_form("register", "That username or email is already registered.", 409)
    except mysql.connector.Error:
        app.logger.exception("Account registration database error")
        return render_form("register", "Unable to create account. Check the database connection.", 500)


@app.route("/register", methods=["POST"])
def register_customer():
    full_name = clean("full_name")
    passport_number = clean("passport_number")
    id_number = clean("id_number")
    email = clean("email")
    contact = clean("contact")

    if not all([full_name, passport_number, id_number, email, contact]):
        return render_form("customer", "Complete all customer details.", 400)

    try:
        customer_record = Customers(full_name, passport_number, id_number, email, contact)
        customer_record.save()
        return show_result(
            "Customer details saved successfully.",
            url_for("customer_registration")
        )
    except ValueError:
        return render_form("customer", "ID Number must be a whole number.", 400)
    except mysql.connector.IntegrityError:
        return render_form("customer", "That ID Number already exists in customer details.", 409)
    except mysql.connector.Error:
        app.logger.exception("Customer details database error")
        return render_form("customer", "Unable to save customer details. Check the database connection and table columns.", 500)


@app.route("/book-flight", methods=["POST"])
def book_flight():
    passport = clean("passport_number")
    departure = clean("departure_date")
    return_date = clean("return_date")
    passengers = clean("passengers")
    destination = clean("destination")
    travel_class = clean("travel_class")

    if not all([passport, departure, passengers, destination, travel_class]):
        return render_form("Flight Booking", "Complete all required booking fields.", 400)
    if travel_class not in {"economy", "bussiness", "first"}:
        return render_form("Flight Booking", "Choose a valid travel class.", 400)
    try:
        if int(passengers) < 1:
            raise ValueError
        if return_date and return_date < departure:
            return render_form("Flight Booking", "Return date cannot be before departure date.", 400)
        booking = Booking(passport, departure, return_date, passengers, destination, travel_class)
        booking.save()
        return show_result("Flight booking request saved successfully.",
                           url_for("customer"))
    except ValueError:
        return render_form("Flight Booking", "Passengers must be a positive whole number.", 400)
    except mysql.connector.Error:
        app.logger.exception("Flight booking database error")
        return render_form("Flight Booking", "Unable to save booking. Check the Flight_Booking table.", 500)


@app.route("/send-parcel", methods=["POST"])
def send_parcel():
    fields = [clean("sender_name"), clean("recipient_name"), clean("description"),
              clean("weight"), clean("destination")]
    if not all(fields):
        return render_form("Parcel Sending", "Complete all parcel fields.", 400)
    try:
        if float(fields[3]) <= 0:
            raise ValueError
        Parcel(*fields).save()
        return show_result("Parcel details saved successfully.", url_for("customer"))
    except ValueError:
        return render_form("Parcel Sending", "Weight must be a positive number.", 400)
    except mysql.connector.Error:
        app.logger.exception("Parcel database error")
        return render_form("Parcel Sending", "Unable to save parcel. Check the Parcel_Sending table.", 500)


@app.route("/check-ticket", methods=["POST"])
def check_ticket():
    passport = clean("passport_number")
    ticket_number = clean("ticket_number")
    if not passport or not ticket_number:
        return render_form("Ticket Checking", "Enter the passport number and ticket number.", 400)
    try:
        ticket = Tickets.find_by_passport_and_number(passport, ticket_number)
        if ticket:
            return show_result(
                f"Ticket found. Flight date: {ticket['Flight_Date']}; Amount: {ticket['Amount']}.",
                url_for("customer")
            )
        return render_form("Ticket Checking", "No matching ticket was found.", 404)
    except mysql.connector.Error:
        app.logger.exception("Ticket lookup database error")
        return render_form("Ticket Checking", "Unable to check ticket. Check the Tickets table.", 500)


@app.route("/report-issue", methods=["POST"])
def report_issue():
    full_name = clean("full_name")
    id_number = clean("id_number")
    issue = clean("issue")
    if not full_name or not issue:
        return render_form("Report Issue", "Enter your name and describe the issue.", 400)
    try:
        Reports(full_name, id_number, issue).save()
        return show_result("Your report was submitted successfully.", url_for("customer"))
    except ValueError:
        return render_form("Report Issue", "ID Number must be a whole number or left blank.", 400)
    except mysql.connector.Error:
        app.logger.exception("Report database error")
        return render_form("Report Issue", "Unable to save report. Check the Reports table.", 500)


@app.route("/online-checkin", methods=["POST"])
def online_checkin():
    passport = clean("passport_number")
    full_name = clean("full_name")
    ticket_number = clean("ticket_number")
    checked_as = clean("checked_as")
    if not all([passport, full_name, ticket_number, checked_as]):
        return render_form("Online CheckIn", "Complete all check-in fields.", 400)
    if checked_as not in {"canceled", "reschedule", "coming"}:
        return render_form("Online CheckIn", "Choose a valid check-in status.", 400)
    try:
        OnlineCheckIn(passport, full_name, ticket_number, checked_as).save()
        return show_result("Your check-in status was recorded successfully.", url_for("customer"))
    except mysql.connector.Error:
        app.logger.exception("Online check-in database error")
        return render_form("Online CheckIn", "Unable to save check-in details. Check the Online_CheckIn table.", 500)


@app.route("/newsletter", methods=["POST"])
def newsletter():
    email = clean("email")
    if not email:
        return render_form("Get Newsletter", "Enter your email address.", 400)
    try:
        Messages.subscribe(email)
        return show_result("You have subscribed to the newsletter.", url_for("customer"))
    except mysql.connector.IntegrityError:
        return render_form("Get Newsletter", "That email is already subscribed.", 409)
    except mysql.connector.Error:
        app.logger.exception("Newsletter database error")
        return render_form("Get Newsletter", "Unable to save subscription. Check the Newsletter_Subscribers table.", 500)


@app.route("/contact", methods=["POST"])
def contact():
    name, email, message = clean("full_name"), clean("email"), clean("message")
    if not all([name, email, message]):
        return render_form("Contact", "Complete all contact fields.", 400)
    try:
        Messages.contact(name, email, message)
        return show_result("Your message was sent successfully.", url_for("home"))
    except mysql.connector.Error:
        app.logger.exception("Contact message database error")
        return render_form("Contact", "Unable to save your message. Check the Contact_Messages table.", 500)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
