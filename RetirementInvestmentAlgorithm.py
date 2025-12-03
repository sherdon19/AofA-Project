# Sherdonese Brown - 2301101
# Kaif Brown - 2304843

# Retirement Investment Optimization Tool

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


# ~~~~~~~User-Friendly CLI Interface~~~~~~~

def run_cli():
    print("**** AofA Financial Services Ltd ****\n")
    print("******** WELCOME TO THE RETIREMENT INVESTMENT TOOL ********")

    while True:
        print("\nChoose an option:")
        print("1. Fixed Growth Simulation")
        print("2. Variable Growth Simulation")
        print("3. Retirement Depletion Simulation")
        print("4. Optimal Withdrawal Calculation")
        print("5. Exit")

        choice = input("Enter a choice (1-5): ").strip()

        if choice == "1":
            p = float(input("Enter principal amount: "))
            r = float(input("Enter annual interest rate (e.g., 0.05 for 5%): "))
            y = int(input("Enter number of years: "))
            result = fixedInvestor(p, r, y)
            if result is not None:
                print("Final Balance after", y, "years is:", round(result, 2))

        elif choice == "2":
            p = float(input("Enter principal amount: "))
            n = int(input("Enter number of years: "))
            rates = []
            for i in range(n):
                rate = float(input("Enter rate for year " + str(i + 1) + ": "))
                rates.append(rate)
            result = variableInvestor(p, rates)
            if result is not None:
                print("Final Balance after", n, "years is:", round(result, 2))

        elif choice == "3":
            b = float(input("Enter starting retirement balance: "))
            e = float(input("Enter fixed annual withdrawal amount: "))
            r = float(input("Enter expected annual return rate (decimal): "))
            y = int(input("Enter maximum years to simulate: "))
            result = finallyRetired(b, e, r, max_years=y)
            print("Funds lasted", result, "years.")

        elif choice == "4":
            b = float(input("Enter starting retirement balance: "))
            r = float(input("Enter expected annual return rate (decimal): "))
            y = int(input("Enter target number of retirement years: "))
            result = maximumExpensed(b, r, y)
            print("Estimated maximum sustainable annual expense:", round(result, 2))

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


# Run the program
if __name__ == "__main__":
    run_cli()
