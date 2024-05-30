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
            self.spots[row][col] = {'owner': 'Random', 'hours': random.randint(3, 10)}  # Random duration between 3 to 10 hours

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
        # Display updated garage
        self.display_garage()

    def increase_bank_balance(self, amount):
        self.bank_balance += amount
        print(f"Bank balance increased by ${amount}. New balance: ${self.bank_balance}")

    def display_bank_balance(self):
        print(f"Bank Balance: ${self.bank_balance}")

    def display_garage(self):
        self.display_bank_balance()
        print("Hour of the day:", self.hour_of_day)
        print("Day of the week:", self.day_of_week)
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.spots[row][col]:
                    print("[ ]", end=" ")  # Empty spot
                else:
                    owner = self.spots[row][col]['owner']
                    hours = self.spots[row][col]['hours']
                    if owner == 'You':
                        print("[R" + str(hours) + "]", end=" ")  # Your reservation
                    else:
                        print("[X" + str(hours) + "]", end=" ")  # Randomly parked car
            print()  # Move to the next row

def main():
    rows = 5
    cols = 5
    garage = ParkingGarage(rows, cols)
    garage.simulate_random_parking(8)  # Simulate 8 random parked cars

    while True:
        print("\n1. Reserve Parking Spot")
        print("2. Increase Bank Balance")
        print("3. Display Parking Garage")
        print("4. Decrement Hours")
        print("5. Display Bank Balance")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            time = int(input("Enter duration to reserve (in hours): "))
            garage.reserve_spot(time)
        elif choice == '2':
            amount = int(input("Enter the amount to increase bank balance: "))
            garage.increase_bank_balance(amount)
        elif choice == '3':
            garage.display_garage()
        elif choice == '4':
            num_hours = int(input("Enter number of hours to decrement: "))
            garage.decrement_hours(num_hours)
            print("Hours decremented.")
        elif choice == '5':
            garage.display_bank_balance()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()