import os
from datetime import date, datetime
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from supabase import create_client

# -------------------------
# LOAD ENVIRONMENT VARIABLES
# -------------------------

load_dotenv()

# -------------------------
# SUPABASE CONNECTION
# -------------------------

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(url, key)

# -------------------------
# FLASK APPLICATION
# -------------------------

app = Flask(__name__)


# -------------------------
# DASHBOARD
# -------------------------

@app.route("/")
def dashboard():

    # Get all payments from Supabase
    response = (
        supabase
        .table("payments")
        .select("*")
        .order("id", desc=True)
        .execute()
    )

    all_payments = response.data

    # -------------------------
    # TOTAL PAID - ALL WORKERS
    # -------------------------

    total_paid = sum(
        float(payment["amount"])
        for payment in all_payments
    )

    # -------------------------
    # TODAY'S PAYMENT
    # -------------------------

    today = date.today().isoformat()

    today_paid = sum(
        float(payment["amount"])
        for payment in all_payments
        if payment["payments_date"] == today
    )

    # -------------------------
    # TOTAL WORKERS
    # -------------------------

    workers = set(
        str(payment["worker_name"]).strip().lower()
        for payment in all_payments
        if payment["worker_name"]
    )

    total_workers = len(workers)

    # -------------------------
    # WORKER TOTALS
    # -------------------------

    worker_totals = {}

    for payment in all_payments:

        worker = payment["worker_name"]
        amount = float(payment["amount"])

        if worker in worker_totals:
            worker_totals[worker] += amount
        else:
            worker_totals[worker] = amount

    # -------------------------
    # SEARCH VALUES
    # -------------------------

    search_worker = request.args.get("worker", "").strip()

    search_date = request.args.get("date", "").strip()

    # -------------------------
    # CONVERT DATE
    # DD-MM-YYYY → YYYY-MM-DD
    # -------------------------

    database_date = ""

    if search_date:

        try:

            database_date = datetime.strptime(
                search_date,
                "%d-%m-%Y"
            ).date().isoformat()

        except ValueError:

            database_date = ""

    # -------------------------
    # FILTER PAYMENTS
    # -------------------------

    payments = all_payments

    # Worker filter
    if search_worker:

        payments = [
            payment
            for payment in payments
            if str(payment["worker_name"]).strip().lower()
            == search_worker.lower()
        ]

    # Date filter
    if database_date:

        payments = [
            payment
            for payment in payments
            if payment["payments_date"] == database_date
        ]

    # -------------------------
    # SEARCH RESULT TOTAL
    # -------------------------

    selected_date_total = sum(
        float(payment["amount"])
        for payment in payments
    )

    # -------------------------
    # SEND DATA TO DASHBOARD
    # -------------------------

    return render_template(
        "dashboard.html",
        payments=payments,
        total_paid=total_paid,
        today_paid=today_paid,
        total_workers=total_workers,
        worker_totals=worker_totals,
        search_worker=search_worker,
        search_date=search_date,
        selected_date_total=selected_date_total
    )


# -------------------------
# DELETE PAYMENT
# -------------------------

@app.route("/delete/<int:payment_id>", methods=["POST"])
def delete_payment(payment_id):

    (
        supabase
        .table("payments")
        .delete()
        .eq("id", payment_id)
        .execute()
    )

    return redirect("/")


# -------------------------
# RUN APPLICATION
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)