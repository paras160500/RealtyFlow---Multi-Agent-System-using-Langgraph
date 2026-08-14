from datetime import datetime
from langchain.tools import tool

# ═══════════════════════════════════════════════════════════════════════════════════════════
#                                For supervisor Agent 
# ═══════════════════════════════════════════════════════════════════════════════════════════
@tool
def calculate_mortgage_affordability(
    monthly_income: float,
    interest_rate: float,
    loan_years: int = 30
) -> dict:
    """
        Calculate maximum affordable mortgage and monthly payment.
        Args:
            monthly_income(float) : Monthly gross income
            interest_rate(float) : Annual interest rate
            loan_years(int) : Duration of the loan
        Returns:
            dict
    """

    if monthly_income <= 0:
        raise ValueError("Monthly income must be greater than 0.")

    if interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if loan_years <= 0:
        raise ValueError("Loan duration must be greater than 0.")

    # 30% of income rule for monthly payment
    max_monthly_payment = monthly_income * 0.3

    monthly_rate = (interest_rate / 100) / 12
    num_payments = loan_years * 12

    # Calculate max loan amount
    if monthly_rate == 0:
        max_loan = max_monthly_payment * num_payments
    else:
        max_loan = max_monthly_payment * (
            (1 - (1 + monthly_rate) ** -num_payments)
            / monthly_rate
        )

    result = {
        "max_loan_amount": round(max_loan, 2),
        "max_monthly_payment": round(max_monthly_payment, 2),
        "loan_term_years": loan_years
    }

    print(
        f" -> Max Loan : ${result['max_loan_amount']} "
        f"(${result['max_monthly_payment']}/month)"
    )

    return result


# ═══════════════════════════════════════════════════════════════════════════════════════════
#                                For transaction history Agent 
# ═══════════════════════════════════════════════════════════════════════════════════════════

@tool
def calculate_price_per_sqft(
    total_price: float,
    size_sqft: float
) -> dict:
    """
        Calculate price per squre foot for property valuation
        Args:
            total_price(float) : Price of the property
            size_sqft(float) : Size of the property
        Returns:
            dict
    """

    if total_price <= 0:
        raise ValueError("Total property price must be greater than 0.")

    if size_sqft <= 0:
        raise ValueError("Property size must be greater than 0.")

    price_per_sqft = total_price / size_sqft

    tier = (
        "Premium" if price_per_sqft > 2500
        else "High-End"
        if price_per_sqft > 1800
        else "Mid-Range"
        if price_per_sqft > 1200
        else "Affordable"
    )

    result = {
        "price_per_sqft": round(price_per_sqft, 2),
        "tier": tier
    }

    print(
        f" -> ${result['price_per_sqft']}/sqft ({tier})"
    )

    return result


# ═══════════════════════════════════════════════════════════════════════════════════════════
#                                For property profile Agent 
# ═══════════════════════════════════════════════════════════════════════════════════════════

@tool
def calculate_remaining_lease(
    lease_start_year: int,
    lease_duration: int = 99,
    lease_start_month: int = 1
) -> dict:
    """
        Calculate remaining lease years for leasehold properties.
        Args:
            lease_start_year(int) : Starting year of the lease
            lease_duration(int) : Duration of the lease in years
            lease_start_month(int) : Starting month of the lease (1-12)
        Returns:
            dict
    """

    if lease_start_year <= 0:
        raise ValueError("Lease start year must be valid.")

    if lease_duration <= 0:
        raise ValueError("Lease duration must be greater than 0.")

    if lease_start_month < 1 or lease_start_month > 12:
        raise ValueError("Lease start month must be between 1 and 12.")

    current_date = datetime.now()

    start_date = datetime(
        lease_start_year,
        lease_start_month,
        1
    )

    end_year = lease_start_year + lease_duration

    # Calculate remaining lease approximately in months
    total_months = (
        (end_year - current_date.year) * 12
        + (lease_start_month - current_date.month)
    )

    remaining_years = max(0, total_months / 12)

    status = (
        "Excellent" if remaining_years > 80
        else "Good" if remaining_years > 60
        else "Fair" if remaining_years > 40
        else "Short"
    )

    result = {
        "remaining_years": round(remaining_years, 1),
        "status": status,
        "lease_start_year": lease_start_year,
        "lease_start_month": lease_start_month,
        "lease_duration_years": lease_duration,
        "lease_expiry_year": end_year
    }

    print(
        f" -> {result['remaining_years']} years remaining "
        f"({status})"
    )

    return result