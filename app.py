from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

# Sample data
transactions = [
    {"id": 1, "date": "2023-12-01", "amount": 5000},
    {"id": 2, "date": "2023-12-02", "amount": 40560},
    {"id": 3, "date": "2023-12-03", "amount": 45689},
    {"id": 4, "date": "2024-10-04", "amount": 12348}
]

# Home page
@app.route("/")
def home_page():
    return render_template("index.html")

# Read operation
@app.route("/transactions")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        try:
            date = request.form["date"]
            amount = float(request.form["amount"])
        except ValueError:
            return "Invalid amount"

        transaction = {
            "id": len(transactions) + 1,
            "date": date,
            "amount": amount
        }
        transactions.append(transaction)

        return redirect(url_for("get_transactions"))

    return render_template("form.html")


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    try:
        if request.method == "POST":
            date = request.form.get("date", transactions[-1]["date"])
            if date is None:
                return "Date is required"
            try:
                amount = float(request.form["amount"])
            except ValueError:
                return "Invalid amount"

            for transaction in transactions:
                if transaction["id"] == transaction_id:
                    transaction["date"] = date
                    transaction["amount"] = amount
                    break

            return redirect(url_for("get_transactions"))
    except TypeError:
        print("Please refresh the page and input an integer")
        return redirect(url_for("get_transactions"))

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)

    return {"message": "Transaction not found. Enter a correct ID"}, 404


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    global transactions
    transactions = [transaction for transaction in transactions if transaction["id"] != transaction_id]
    return redirect(url_for("get_transactions"))

 #Search Operation
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_amount = float(request.form["min_amount"])
        max_amount = float(request.form["max_amount"])
        
        filtered_transactions = [transaction for transaction in transactions if min_amount <= transaction["amount"] <= max_amount]
        if not filtered_transactions:
            return "No transactions were found"
        
        return render_template("transactions.html", transactions = filtered_transactions)
    
    # If it is a GET request
    return render_template("search.html")
                   

# Total Balance Operation
@app.route("/balance")
def total_balance():
    total = sum(transaction["amount"] for transaction in transactions)
    return f"Total Balance: {total}"
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
