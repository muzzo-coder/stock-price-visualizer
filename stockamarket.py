import time
import threading
import random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def generate_stock_data():
    while True:
        stock_data = {
            'Stock A': random.uniform(100, 200),
            'Stock B': random.uniform(50, 150),
            'Stock C': random.uniform(200, 300),
            'Stock D': random.uniform(300, 400),  
        }
        yield stock_data
        time.sleep(1)


def plot_stock_data(stock_prices):
    fig, ax = plt.subplots()
    
    def update(frame):
        ax.clear()
        for stock, prices in stock_prices.items():
            ax.plot(prices, label=stock)
        ax.legend(loc='upper left')
        ax.set_title('Real-Time Stock Prices')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Price')

    ani = FuncAnimation(fig, update, interval=1000)
    plt.show()


def log_stock_data(stock_data):
    with open("stock_data_log.txt", "a") as file:
        for stock, price in stock_data.items():
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {stock}: {price:.2f}\n")


def calculate_average_prices(stock_prices):
    averages = {stock: (sum(prices) / len(prices)) if prices else 0 for stock, prices in stock_prices.items()}
    return averages

def start_dashboard():
    stock_prices = {'Stock A': [], 'Stock B': [], 'Stock C': [], 'Stock D': []}
    stock_data_gen = generate_stock_data()

    def update_stock_prices():
        while True:
            stock_data = next(stock_data_gen)
            log_stock_data(stock_data) 
            for stock, price in stock_data.items():
                stock_prices[stock].append(price)

                
                if len(stock_prices[stock]) > 100:
                    stock_prices[stock].pop(0)

            time.sleep(1)

    threading.Thread(target=update_stock_prices, daemon=True).start()

    root = tk.Tk()
    root.title("Stock Monitoring Dashboard")

    tk.Label(root, text="Welcome to the Real-Time Stock Monitoring Dashboard", font=("Arial", 14)).pack(pady=10)

    def show_recent_prices():
        recent_prices = "\n".join(
            [f"{stock}: {prices[-1]:.2f}" if prices else f"{stock}: No data"
             for stock, prices in stock_prices.items()]
        )
        messagebox.showinfo("Recent Prices", recent_prices)

    def show_average_prices():
        averages = calculate_average_prices(stock_prices)
        average_prices = "\n".join([f"{stock}: {avg:.2f}" for stock, avg in averages.items()])
        messagebox.showinfo("Average Prices", average_prices)

    def export_to_csv():
        with open("stock_data_export.csv", "w") as file:
            file.write("Stock,Price\n")
            for stock, prices in stock_prices.items():
                for price in prices:
                    file.write(f"{stock},{price:.2f}\n")
        messagebox.showinfo("Export", "Stock data exported to stock_data_export.csv")

    tk.Button(root, text="View Real-Time Graph", command=lambda: plot_stock_data(stock_prices)).pack(pady=10)
    tk.Button(root, text="Show Recent Prices", command=show_recent_prices).pack(pady=10)
    tk.Button(root, text="Show Average Prices", command=show_average_prices).pack(pady=10)
    tk.Button(root, text="Export Data to CSV", command=export_to_csv).pack(pady=10)
    tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_dashboard()
