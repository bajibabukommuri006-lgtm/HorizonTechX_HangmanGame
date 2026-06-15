import csv
import os
from datetime import datetime

# ─────────────────────────────────────────────────────
#  Horizon TechX — Task 2: Stock Portfolio Tracker
#  Key concepts: dictionary, input/output,
#                basic arithmetic, file handling
# ─────────────────────────────────────────────────────

# ── Hardcoded stock prices (USD) ──────────────────────
STOCK_PRICES = {
    "AAPL":  180.00,   # Apple
    "TSLA":  250.00,   # Tesla
    "GOOGL": 140.00,   # Alphabet (Google)
    "MSFT":  415.00,   # Microsoft
    "AMZN":  185.00,   # Amazon
    "META":  500.00,   # Meta
    "NFLX":  650.00,   # Netflix
    "NVDA":  870.00,   # NVIDIA
    "RELIANCE": 28.50, # Reliance Industries (NSE, in USD equiv.)
    "TCS":   42.00,    # Tata Consultancy Services
}

DIVIDER  = "─" * 52
DIVIDER2 = "═" * 52


# ── Helpers ────────────────────────────────────────────
def show_available_stocks():
    print(f"\n  {'SYMBOL':<10} {'COMPANY / NOTE':<28} {'PRICE (USD)':>10}")
    print("  " + DIVIDER)
    names = {
        "AAPL": "Apple Inc.", "TSLA": "Tesla Inc.",
        "GOOGL": "Alphabet (Google)", "MSFT": "Microsoft",
        "AMZN": "Amazon", "META": "Meta Platforms",
        "NFLX": "Netflix", "NVDA": "NVIDIA",
        "RELIANCE": "Reliance Industries", "TCS": "Tata Consultancy",
    }
    for sym, price in STOCK_PRICES.items():
        print(f"  {sym:<10} {names[sym]:<28} ${price:>9.2f}")
    print()


def get_portfolio():
    """Prompt the user to enter stock symbols and quantities."""
    portfolio = {}
    print("\n  Enter stock symbol and quantity (type 'done' when finished).")
    print("  Type 'list' to see all available stocks.\n")

    while True:
        symbol = input("  Stock symbol: ").strip().upper()

        if symbol == "DONE":
            if not portfolio:
                print("  ⚠  No stocks added. Please add at least one.\n")
                continue
            break

        if symbol == "LIST":
            show_available_stocks()
            continue

        if symbol not in STOCK_PRICES:
            print(f"  ⚠  '{symbol}' not found. Type 'list' to see available stocks.\n")
            continue

        try:
            qty = int(input(f"  Quantity for {symbol}: ").strip())
            if qty <= 0:
                print("  ⚠  Quantity must be a positive whole number.\n")
                continue
        except ValueError:
            print("  ⚠  Please enter a valid integer quantity.\n")
            continue

        if symbol in portfolio:
            portfolio[symbol] += qty
            print(f"  ✅  Updated {symbol}: total {portfolio[symbol]} shares.\n")
        else:
            portfolio[symbol] = qty
            print(f"  ✅  Added {qty} share(s) of {symbol}.\n")

    return portfolio


def calculate_portfolio(portfolio):
    """Return a list of (symbol, qty, price, value) rows and the grand total."""
    rows = []
    total = 0.0
    for symbol, qty in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * qty
        total += value
        rows.append((symbol, qty, price, value))
    rows.sort(key=lambda r: r[3], reverse=True)   # sort by value descending
    return rows, total


def display_portfolio(rows, total):
    """Pretty-print the portfolio table to the console."""
    print("\n  " + DIVIDER2)
    print("         📊  YOUR STOCK PORTFOLIO")
    print("  " + DIVIDER2)
    print(f"  {'SYMBOL':<8} {'QTY':>6} {'PRICE (USD)':>12} {'VALUE (USD)':>13}")
    print("  " + DIVIDER)

    for symbol, qty, price, value in rows:
        pct = (value / total * 100) if total else 0
        bar = "█" * int(pct / 5)          # simple bar (max 20 chars wide)
        print(f"  {symbol:<8} {qty:>6} ${price:>11.2f} ${value:>12.2f}  {bar} {pct:.1f}%")

    print("  " + DIVIDER)
    print(f"  {'TOTAL PORTFOLIO VALUE':<28} ${total:>12.2f}")
    print("  " + DIVIDER2)
    print(f"  Holdings: {len(rows)} stock(s)   |   "
          f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")


# ── File saving ────────────────────────────────────────
def save_as_txt(rows, total, filename):
    with open(filename, "w") as f:
        f.write("=" * 52 + "\n")
        f.write("       STOCK PORTFOLIO TRACKER REPORT\n")
        f.write("=" * 52 + "\n")
        f.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 52 + "\n")
        f.write(f"{'SYMBOL':<8} {'QTY':>6} {'PRICE':>12} {'VALUE':>13}\n")
        f.write("-" * 52 + "\n")
        for symbol, qty, price, value in rows:
            f.write(f"{symbol:<8} {qty:>6} ${price:>11.2f} ${value:>12.2f}\n")
        f.write("-" * 52 + "\n")
        f.write(f"{'TOTAL':<28} ${total:>12.2f}\n")
        f.write("=" * 52 + "\n")
    print(f"  ✅  Saved as TXT → {os.path.abspath(filename)}")


def save_as_csv(rows, total, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Quantity", "Price_USD", "Value_USD", "Weight_%"])
        for symbol, qty, price, value in rows:
            pct = round(value / total * 100, 2) if total else 0
            writer.writerow([symbol, qty, f"{price:.2f}", f"{value:.2f}", pct])
        writer.writerow([])
        writer.writerow(["TOTAL", "", "", f"{total:.2f}", "100.00"])
    print(f"  ✅  Saved as CSV → {os.path.abspath(filename)}")


def save_results(rows, total):
    """Ask the user which format(s) to save and handle it."""
    print("  Save your portfolio?")
    print("  [1] Save as .txt")
    print("  [2] Save as .csv")
    print("  [3] Save both")
    print("  [4] Skip — don't save\n")

    choice = input("  Your choice (1/2/3/4): ").strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    if choice in ("1", "3"):
        save_as_txt(rows, total, f"portfolio_{timestamp}.txt")
    if choice in ("2", "3"):
        save_as_csv(rows, total, f"portfolio_{timestamp}.csv")
    if choice == "4":
        print("  ℹ  Results not saved.")
    if choice not in ("1", "2", "3", "4"):
        print("  ⚠  Invalid choice. Results not saved.")


# ── Main ───────────────────────────────────────────────
def main():
    print("\n" + DIVIDER2)
    print("       💹  STOCK PORTFOLIO TRACKER")
    print("  " + "Horizon TechX — Python Internship Task 2")
    print(DIVIDER2)

    show_available_stocks()

    while True:
        portfolio  = get_portfolio()
        rows, total = calculate_portfolio(portfolio)
        display_portfolio(rows, total)
        save_results(rows, total)

        again = input("\n  Track another portfolio? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thank you for using Stock Portfolio Tracker. Goodbye!\n")
            break


if __name__ == "__main__":
    main()