import tkinter as tk
import random

class ParkingGarage:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.spots = [[{} for _ in range(cols)] for _ in range(rows)]  # Initialize all spots as empty dictionaries
        self.bank_balance = 50
        self.hour_of_day = 12  # Arbitrary hour of the day (12:00 PM)
        self.day_of_week = 'Monday'  # Arbitrary day of the week (Monday)

    def generate_parking_cost(self):
        # Define base parking cost
        base_cost = 10  # Base cost for parking

        # Adjust cost based on the hour of the day and the day of the week
        if 8 <= self.hour_of_day <= 17:  # Parking between 8 AM and 5 PM
            if self.day_of_week in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                # Weekday pricing
                return base_cost * 1.5  # 50% surcharge during weekdays
            else:
                # Weekend pricing
                return base_cost  # No surcharge on weekends
        else:
            # Off-peak pricing
            return base_cost * 0.75  # 25% discount during off-peak hours

    def find_available_spot(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.spots[row][col]:
                    return row, col
        return None  # If no available spot found

    def reserve_spot(self, time):
        total_cost = self.generate_parking_cost()

        # Check if the bank balance is sufficient
        if self.bank_balance >= total_cost:
            # Deduct the cost from the bank balance
            self.bank_balance -= total_cost

            # Reserve the spot
            spot = self.find_available_spot()
            if spot is not None:
                row, col = spot
                self.spots[row][col] = {'owner': 'You', 'hours': time}
                print(f"Parking spot at ({row}, {col}) reserved for {time} hours.")
                print("You were charged: $", total_cost)
                self.display_bank_balance()
            else:
                print("No available parking spots.")
        else:
            print("Insufficient funds to reserve the parking spot.")

    def simulate_random_parking(self, num_occupied):
        for _ in range(num_occupied):
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            while self.spots[row][col]:
                row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            self.spots[row][col] = {'owner': 'Random',
                                    'hours': random.randint(3, 10)}  # Random duration between 3 to 10 hours

    def decrement_hours(self, num_hours):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.spots[row][col]:
                    self.spots[row][col]['hours'] -= num_hours
                    if self.spots[row][col]['hours'] <= 0:
                        self.spots[row][col] = {}  # Remove reservation if hours are zero
        # Update arbitrary variables
        for _ in range(num_hours):
            self.hour_of_day = (self.hour_of_day + 1) % 24  # Increment hour (24-hour clock)
            if self.hour_of_day == 0:
                # Increment day if hour wraps around to 0
                days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                current_day_index = days_of_week.index(self.day_of_week)
                self.day_of_week = days_of_week[(current_day_index + 1) % 7]
        # Simulate random parking
        remaining_spots = sum(1 for row in self.spots for spot in row if not spot)
        num_random_parkers = random.randint(0, remaining_spots - 1)  # Random number of random parkers
        self.simulate_random_parking(num_random_parkers)  # Simulate random parking

    def increase_bank_balance(self, amount):
        self.bank_balance += amount

    def display_bank_balance(self):
        return self.bank_balance

    def display_garage(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                x0, y0 = col * 50, row * 50
                x1, y1 = x0 + 50, y0 + 50
                if not self.spots[row][col]:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                else:
                    fill = ""
                    text = ""
                    owner = self.spots[row][col]['owner']
                    hours = self.spots[row][col]['hours']
                    if owner == 'You':
                        fill = "yellow"
                        text = str(hours)
                    else:
                        fill = "red"
                        text = str(hours)

                    canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
                    canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=text)


class ParkingGarageGUI:
    def __init__(self, root, parking_garage):
        self.root = root
        self.root.title("Parking Garage Simulator")

        # Create labels
        self.label = tk.Label(root, text="Parking Garage Simulator", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Create entry widgets
        self.reserve_label = tk.Label(root, text="Duration to reserve (in hours):")
        self.reserve_label.grid(row=1, column=0, padx=10, pady=5)
        self.reserve_entry = tk.Entry(root)
        self.reserve_entry.grid(row=1, column=1, padx=10, pady=5)

        self.balance_label = tk.Label(root, text="Amount to increase bank balance:")
        self.balance_label.grid(row=2, column=0, padx=10, pady=5)
        self.balance_entry = tk.Entry(root)
        self.balance_entry.grid(row=2, column=1, padx=10, pady=5)

        self.decrement_label = tk.Label(root, text="Amount of hours to decrement by:")
        self.decrement_label.grid(row=3, column=0, padx=10, pady=5)
        self.decrement_entry = tk.Entry(root)
        self.decrement_entry.grid(row=3, column=1, padx=10, pady=5)

        # Create buttons
        self.reserve_button = tk.Button(root, text="Reserve Parking Spot", command=self.reserve_spot)
        self.reserve_button.grid(row=1, column=2, padx=10, pady=5)

        self.bank_balance_button = tk.Button(root, text="Increase Bank Balance", command=self.increase_balance)
        self.bank_balance_button.grid(row=2, column=2, padx=10, pady=5)

        self.display_button = tk.Button(root, text="Display Parking Garage", command=self.display_garage)
        self.display_button.grid(row=1, column=3, padx=10, pady=5)

        self.decrement_button = tk.Button(root, text="Decrement Hours", command=self.decrement_hours)
        self.decrement_button.grid(row=3, column=2, padx=10, pady=5)

        self.balance_display_label = tk.Label(root, text="Bank Balance:")
        self.balance_display_label.grid(row=3, column=3, padx=10, pady=5)

        self.balance_display_var = tk.StringVar()  # Variable to hold bank balance value
        self.balance_display_var.set("")  # Initialize as empty string
        self.balance_display = tk.Label(root, textvariable=self.balance_display_var)
        self.balance_display.grid(row=3, column=4, padx=10, pady=5)

        # Display the day of the week
        self.day_label = tk.Label(root, text="Day of the Week:")
        self.day_label.grid(row=6, column=0, padx=10, pady=5)

        # Create a StringVar to hold the value of day_of_week
        self.day_var = tk.StringVar()
        self.day_var.set(parking_garage.day_of_week)  # Initialize with the value from ParkingGarage

        # Create a label to dynamically display the value of day_of_week
        self.day_display_label = tk.Label(root, textvariable=self.day_var)
        self.day_display_label.grid(row=6, column=1, padx=10, pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

        # Create canvas for displaying parking garage
        self.canvas = tk.Canvas(root, width=250, height=250)
        self.canvas.grid(row=5, column=0, columnspan=4, padx=10, pady=5)

        # Store the ParkingGarage instance
        self.parking_garage = parking_garage

        # Initialize Parking Garage
        self.parking_garage.simulate_random_parking(8)

        # Display the parking garage
        self.display_garage()

    def reserve_spot(self):
        time_str = self.reserve_entry.get()
        if time_str:
            try:
                time = int(time_str)
                self.parking_garage.reserve_spot(time)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("Please enter a value for duration.")
        self.display_garage()

    def increase_balance(self):
        time_str = self.balance_entry.get()
        if time_str:
            try:
                time = int(time_str)
                self.parking_garage.increase_bank_balance(time)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("Please enter a valid amount.")

        self.update_bank_balance_display()

    def decrement_hours(self):
        time_str = self.decrement_entry.get()
        if time_str:
            try:
                time = int(time_str)
                self.parking_garage.decrement_hours(time)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            self.parking_garage.decrement_hours(1)

        # Update the displayed day of the week
        self.day_var.set(self.parking_garage.day_of_week)

        self.display_garage()


    def display_garage(self):
        self.canvas.delete("all")  # Clear previous drawings on the canvas
        self.parking_garage.display_garage(self.canvas)

    def update_bank_balance_display(self):
        balance = self.parking_garage.display_bank_balance()
        self.balance_display_var.set(str(balance))


def main():
    root = tk.Tk()
    parking_garage = ParkingGarage(5, 5)
    app = ParkingGarageGUI(root, parking_garage)
    root.mainloop()


if __name__ == "__main__":
    main()
