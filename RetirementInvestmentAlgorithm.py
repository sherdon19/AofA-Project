# Sherdonese Brown - 2301101
# Kaif Brown - 
# Retirement Investment Optimization Tool

from flask import Flask, request, jsonify

app = Flask(__name__)

# Function 1: Fixed Growth Simulation
def fixedInvestor(principal, rate, years):
    # Check for invalid inputs.
    if principal < 0:
        print("Error: Principal must be non-negative.")
        return None
    if years < 0:
        print("Error: Years must be non-negative.")
        return None

    # Starting with the initial principal
    balance = principal
    # Loop through each year
    for year in range(1, years + 1):
        # Update balance by multiplying with (1 + rate)
        balance = balance * (1 + rate)
        # Show progress for each year
        print("Year", year, "Balance:", round(balance, 2))
    # Return the final balance after all years
    return balance


# Function 2: Variable Growth Simulation
def variableInvestor(principal, rateList):
    # Check for invalid inputs
    if principal < 0:
        print("Error: Principal must be non-negative.")
        return None
    if not isinstance(rateList, list) or len(rateList) == 0:
        print("Error: rateList must be a non-empty list of rates.")
        return None

    # Start with the initial principal
    balance = principal
    # Loop through each rate in the list
    for i in range(len(rateList)):
        rate = rateList[i]
        # Update balance with the current year's rate
        balance = balance * (1 + rate)
        # Show progress for each year
        print("Year", i + 1, "Rate:", rate, "Balance:", round(balance, 2))
    # Return the final balance after all rates applied
    return balance


# Function 3: Retirement Expense Simulation
def finallyRetired(balance, expense, rate, max_years=200, withdraw_first=True):
    years = 0
    current = balance

    while years < max_years and current > 0.0:
        if withdraw_first:
            # Withdraw at the start of the year
            current -= expense
            if current <= 0.0:
                break
            # Then apply growth
            current *= (1.0 + rate)
        else:
            # Grow at the start of the year
            current *= (1.0 + rate)
            # Then withdraw
            current -= expense
            if current <= 0.0:
                break
        years += 1

    return years


# Function 4: Optimal Withdrawal Calculation
def maximumExpensed(balance, rate, max_years, tolerance=0.01, max_iterations=100):
    low = 0.0
    high = balance
    best = 0.0

    for _ in range(max_iterations):
        if high - low <= tolerance:
            break

        mid = (low + high) / 2.0
        years_last = finallyRetired(balance, mid, rate, max_years, withdraw_first=True)

        # If the money lasts at least max_years, then mid is too small,
        # so we can try a larger withdrawal.
        if years_last >= max_years:
            best = mid
            low = mid
        else:
            # The money runs out too early, so mid is too large.
            high = mid

    return best
    
# --- Flask Routes ---
@app.route("/fixed")
def fixed_route():
    principal = float(request.args.get("principal", 1000))
    rate = float(request.args.get("rate", 0.05))
    years = int(request.args.get("years", 10))
    result = fixedInvestor(principal, rate, years)
    return jsonify({"final_balance": round(result, 2)})

@app.route("/variable")
def variable_route():
    principal = float(request.args.get("principal", 1000))
    rates = request.args.getlist("rate", type=float)
    result = variableInvestor(principal, rates)
    return jsonify({"final_balance": round(result, 2)})

@app.route("/retired")
def retired_route():
    balance = float(request.args.get("balance", 100000))
    expense = float(request.args.get("expense", 10000))
    rate = float(request.args.get("rate", 0.03))
    years = int(request.args.get("years", 30))
    result = finallyRetired(balance, expense, rate, years)
    return jsonify({"years_lasted": result})

@app.route("/optimal")
def optimal_route():
    balance = float(request.args.get("balance", 100000))
    rate = float(request.args.get("rate", 0.03))
    years = int(request.args.get("years", 30))
    result = maximumExpensed(balance, rate, years)
    return jsonify({"optimal_expense": round(result, 2)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
