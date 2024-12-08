# Author: Dev Not F Leaving (https://x.com/devnotfleavin)
# License: MIT License - See LICENSE file for details.

import numpy as np
import matplotlib.pyplot as plt

def simulate_meme_coin_portfolio(
    num_memes=50,
    capital_per_meme=0.01,
    initial_capital=10,  # Initial capital in $SOL
    short_failure_rate=0.9,  # Probability of failure after 6 hours
    long_failure_rate=0.7,  # Probability of failure after 1 month
    success_multiplier=20,  # Success multiplier for successful memes
    time_horizon_hours=6 * 30 * 24  # Time horizon in hours (6 months)
):
    """
    Simulate meme coin portfolio over time.

    Parameters:
        num_memes (int): Number of meme coins bought daily.
        capital_per_meme (float): Capital invested per meme coin.
        initial_capital (float): Initial capital available in $SOL.
        short_failure_rate (float): Failure rate after 6 hours.
        long_failure_rate (float): Failure rate after 1 month.
        success_multiplier (float): Multiplier for successful coins (this assumes passing stage 1 with a 10x bakes int, therefore 20 here means 200x from initial investment).
        time_horizon_hours (int): Total simulation time in hours.

    Returns:
        dict: Results over time including cash on hand, AUM, and expected values.
    """
    # Time-related variables
    hours_per_day = 24
    short_failure_time = 6  # Time in hours
    long_failure_time = 30 * hours_per_day  # Time in hours

    # State tracking
    cash_on_hand = np.zeros(time_horizon_hours)
    aum = np.zeros(time_horizon_hours)
    expected_value = np.zeros(time_horizon_hours)
    cash_on_hand[0] = initial_capital

    # Portfolio state
    portfolio = []  # Each entry is [time_of_purchase, value, status: "pending", "failed", or "success"]

    # Expected value calculations
    ev_short_success = capital_per_meme * 10 * (1 - short_failure_rate)
    ev_success = ev_short_success * success_multiplier * (1 - long_failure_rate)
    ev_per_meme = (ev_short_success + ev_success) * (1 - short_failure_rate)

    for t in range(time_horizon_hours):
        # Update cash on hand
        if t > 0:
            cash_on_hand[t] = cash_on_hand[t - 1]

        # Buy a meme coin every 24 hours
        if t % hours_per_day == 0 and cash_on_hand[t] >= capital_per_meme:
            cash_on_hand[t] -= capital_per_meme
            portfolio.append([t, capital_per_meme, "pending"])

        

        # Check portfolio for failures and successes
        for meme in portfolio:
            time_since_purchase = t - meme[0]

            if meme[2] == "pending":
                if time_since_purchase >= short_failure_time and np.random.rand() < short_failure_rate:
                    meme[2] = "failed"
                elif time_since_purchase >= short_failure_time and meme[2] == "pending":
                    meme[1] *= 10  # 10x value increase
                    meme[2] = "short_success"
            
            if meme[2] == "short_success" and time_since_purchase >= long_failure_time:
                    if np.random.rand() < long_failure_rate:
                        meme[2] = "failed"
                    else:
                        meme[2] = "success"
                        cash_on_hand[t] += meme[1] * success_multiplier  # Sell for 150x

        # Update AUM
        aum[t] = np.sum([
            meme[1] if meme[2] in ["pending", "short_success"] else 0
            for meme in portfolio
        ])

        # Calculate expected value at time t
        num_active_memes = sum(1 for meme in portfolio if meme[2] == "pending")
        expected_value[t] = num_active_memes * ev_per_meme

    return {
        "Cash on Hand": cash_on_hand,
        "AUM": aum,
        "Time Horizon": np.arange(time_horizon_hours),
        "Expected Value": expected_value,
        "Expected Value per Meme": ev_per_meme
    }

# Run the simulation
results = simulate_meme_coin_portfolio(
    num_memes=1,
    capital_per_meme=0.01,
    initial_capital=1,
    short_failure_rate=0.9,
    long_failure_rate=0.7,
    success_multiplier=20,
    time_horizon_hours=6 * 30 * 24  # 6 months
)

# Plot results
plt.figure(figsize=(12, 8))

# Cash on Hand
plt.plot(results["Time Horizon"], results["Cash on Hand"], label="Cash on Hand", color="green")

# AUM
plt.plot(results["Time Horizon"], results["AUM"], label="Assets Under Management (AUM)", color="blue")

# Expected Value
plt.plot(results["Time Horizon"], results["Expected Value"], label="Expected Value", color="orange", linestyle="--")

# Labels and legend
plt.title("Meme Coin Portfolio Simulation Over Time")
plt.xlabel("Time (Hours)")
plt.ylabel("Amount ($SOL)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# Print expected value
print(f"Expected Value per Meme: {results['Expected Value per Meme']:.4f} $SOL")
