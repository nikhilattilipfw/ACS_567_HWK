import csv
import statistics

class FoodData:
    """
    Represents a single food item with its nutritional values.

    Attributes:
        food_item (str): The name of the food item.
        calories (float): Caloric content of the food item.
        protein (float): Protein content of the food item.
        carbs (float): Carbohydrate content of the food item.
    """
    def __init__(self, food_item, calories, protein, carbs):
        self.food_item = food_item
        self.calories = calories
        self.protein = protein
        self.carbs = carbs

class DataManager:
    """
    Manages the operations on food data including reading from and writing to a CSV file.
    Implements the Singleton pattern to ensure only one instance manages the data.

    Attributes:
        data (list of FoodData): A list to store food data.
        filename (str): The name of the CSV file to read from/write to.

    Methods:
        read_data: Reads data from the CSV file and stores it in the data list.
        save_data: Saves the current data list to the CSV file.
        add_data: Adds a new food item to the data list and updates the CSV file.
        edit_data: Edits an existing food item in the data list and updates the CSV file.
        delete_data: Deletes a food item from the data list and updates the CSV file.
        calculate_mean: Calculates the mean of a specified nutritional value across all food items.
        calculate_median: Calculates the median of a specified nutritional value across all food items.
        filter_data: Filters the data list based on a specified value of a nutritional field.
        print_data: Prints the current data list to the console.
    """
    _instance = None
    
    def __new__(cls):
        # Implement Singleton pattern
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance.data = []
            cls._instance.filename = "food_nutrition.csv"  # Set the default filename
        return cls._instance
    
    def read_data(self):
        # Reads data from the CSV file and stores it in the data list
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            self.data = [FoodData(**row) for row in reader]
        
        print("Loaded Data:")
        self.print_data()

    def save_data(self):
        # Saves the current data list to the CSV file
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["food_item", "calories", "protein", "carbs"])
            for item in self.data:
                writer.writerow([item.food_item, item.calories, item.protein, item.carbs])

    def add_data(self, food_item, calories, protein, carbs):
        # Adds a new food item to the data list and updates the CSV file
        new_food = FoodData(food_item=food_item, calories=calories, protein=protein, carbs=carbs)
        self.data.append(new_food)
        self.save_data()

    def edit_data(self, index, food_item, calories, protein, carbs):
        # Edits an existing food item in the data list and updates the CSV file
        if 0 <= index < len(self.data):
            self.data[index] = FoodData(food_item=food_item, calories=calories, protein=protein, carbs=carbs)
            self.save_data()

    def delete_data(self, index):
        # Deletes a food item from the data list and updates the CSV file
        if 0 <= index < len(self.data):
            del self.data[index]
            self.save_data()

    def calculate_mean(self, field):
        # Calculates the mean of a specified nutritional value across all food items
        values = [float(getattr(item, field)) for item in self.data]
        return statistics.mean(values)

    def calculate_median(self, field):
        # Calculates the median of a specified nutritional value across all food items
        values = [float(getattr(item, field)) for item in self.data]
        return statistics.median(values)

    def filter_data(self, field, value):
        # Filters the data list based on a specified value of a nutritional field
        return [item for item in self.data if getattr(item, field) == value]

    def print_data(self):
        # Prints the current data list to the console
        for item in self.data:
            print(f"{item.food_item}, {item.calories}, {item.protein}, {item.carbs}")

class Application:
    """
    The main application class that provides a user interface to interact with the data.

    Attributes:
        data_manager (DataManager): The instance of DataManager to handle data operations.

    Methods:
        display_menu: Displays the menu of options to the user.
        run: Runs the application, handling user input and performing actions based on it.
    """
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def display_menu(self):
        # Displays the menu options to the user
        print("\nMenu:")
        print("1. Read Data from File")
        print("2. Add Data")
        print("3. Edit Data")
        print("4. Delete Data")
        print("5. Data Analysis")
        print("6. Filter Data")
        print("7. Quit")

    def run(self):
        # Main loop to run the application and handle user interactions
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.data_manager.read_data()

            elif choice == '2':
                food_item = input("Enter Food Item: ")
                calories = float(input("Enter Calories: "))
                protein = float(input("Enter Protein: "))
                carbs = float(input("Enter Carbs: "))
                self.data_manager.add_data(food_item, calories, protein, carbs)
                print("Data added successfully.")

            elif choice == '3':
                index = int(input("Enter the index to edit: "))
                food_item = input("Enter Food Item: ")
                calories = float(input("Enter Calories: "))
                protein = float(input("Enter Protein: "))
                carbs = float(input("Enter Carbs: "))
                self.data_manager.edit_data(index, food_item, calories, protein, carbs)
                print("Data edited successfully.")

            elif choice == '4':
                index = int(input("Enter the index to delete: "))
                self.data_manager.delete_data(index)
                print("Data deleted successfully.")

            elif choice == '5':
                field = input("Enter the field for analysis (calories, protein, carbs): ")
                mean = self.data_manager.calculate_mean(field)
                median = self.data_manager.calculate_median(field)
                print(f"Mean {field}: {mean}")
                print(f"Median {field}: {median}")

            elif choice == '6':
                field = input("Enter the field for filtering (food_item, calories, protein, carbs): ")
                value = input(f"Enter the value to filter by {field}: ")
                filtered_data = self.data_manager.filter_data(field, value)
                print("Filtered Data:")
                for item in filtered_data:
                    print(f"{item.food_item}, {item.calories}, {item.protein}, {item.carbs}")

            elif choice == '7':
                print("Exiting the application. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Entry point of the application
    data_manager = DataManager()
    app = Application(data_manager)
    app.run()