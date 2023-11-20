import tkinter as tk
from tkinter import ttk
import subprocess
import matplotlib.pyplot as plt

# Initialize results dictionary
results = {'bfs': [], 'dfs': [], 'ids': [], 'uniform': [], 'astar': []}

def update_city_dropdown(event, entry, dropdown, var):
    current_input = var.get().lower()
    filtered_cities = [city for city in cities if current_input in city.lower()]
    dropdown['values'] = filtered_cities

def run_algorithm():
    global results

    start_city = start_city_var.get()
    end_city = end_city_var.get()
    algorithm = algorithm_var.get()
    cost_function = cost_function_var.get()

    command = [
        "python3",
        "route.py",
        start_city,
        end_city,
        algorithm,
        cost_function
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    results[algorithm].append(result.stdout)

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result.stdout)
    output_text.config(state=tk.DISABLED)

def analyze_results():
    global results

    for algorithm, runs in results.items():
        print(f"Results for {algorithm} algorithm:")
        for i, run in enumerate(runs, start=1):
            print(f"Run {i}:\n{run}")
        print("\n")

    algorithms = list(results.keys())
    run_counts = [len(runs) for runs in results.values()]

    plt.bar(algorithms, run_counts, color='blue')
    plt.xlabel('Algorithm')
    plt.ylabel('Number of Runs')
    plt.title('Algorithm Comparison')
    plt.show()

# Read city names from the file
with open('city-gps.txt', 'r') as file:
    cities = [line.split()[0] for line in file]

# Create the main window
window = tk.Tk()
window.title("Routing GUI")

# Create dropdowns for city selection
start_city_var = tk.StringVar()
end_city_var = tk.StringVar()

start_city_label = tk.Label(window, text="Start City:")
start_city_entry = ttk.Entry(window, textvariable=start_city_var)
start_city_dropdown = ttk.Combobox(window, textvariable=start_city_var, values=cities)

end_city_label = tk.Label(window, text="End City:")
end_city_entry = ttk.Entry(window, textvariable=end_city_var)
end_city_dropdown = ttk.Combobox(window, textvariable=end_city_var, values=cities)

start_city_label.grid(row=0, column=0, padx=10, pady=10)
start_city_entry.grid(row=0, column=1, padx=10, pady=10)
start_city_dropdown.grid(row=0, column=2, padx=10, pady=10)

end_city_label.grid(row=1, column=0, padx=10, pady=10)
end_city_entry.grid(row=1, column=1, padx=10, pady=10)
end_city_dropdown.grid(row=1, column=2, padx=10, pady=10)

# Bind the event to update the start and end city dropdowns dynamically
start_city_entry.bind("<KeyRelease>", lambda event: update_city_dropdown(event, start_city_entry, start_city_dropdown, start_city_var))
start_city_dropdown.bind("<KeyRelease>", lambda event: update_city_dropdown(event, start_city_dropdown, start_city_dropdown, start_city_var))
end_city_entry.bind("<KeyRelease>", lambda event: update_city_dropdown(event, end_city_entry, end_city_dropdown, end_city_var))
end_city_dropdown.bind("<KeyRelease>", lambda event: update_city_dropdown(event, end_city_dropdown, end_city_dropdown, end_city_var))

# Create dropdown for algorithm selection
algorithm_var = tk.StringVar()
algorithm_label = tk.Label(window, text="Routing Algorithm:")
algorithm_dropdown = ttk.Combobox(window, textvariable=algorithm_var, values=["bfs", "dfs", "ids", "uniform", "astar"])

algorithm_label.grid(row=2, column=0, padx=10, pady=10)
algorithm_dropdown.grid(row=2, column=1, padx=10, pady=10)

# Create dropdown for cost function selection
cost_function_var = tk.StringVar()
cost_function_label = tk.Label(window, text="Cost Function:")
cost_function_dropdown = ttk.Combobox(window, textvariable=cost_function_var, values=["segments", "distance", "time"])

cost_function_label.grid(row=3, column=0, padx=10, pady=10)
cost_function_dropdown.grid(row=3, column=1, padx=10, pady=10)

# Create a button to run the algorithm
run_button = tk.Button(window, text="Run Algorithm", command=run_algorithm)
run_button.grid(row=4, column=0, columnspan=3, pady=20)

# Create a button to analyze results
analyze_button = tk.Button(window, text="Analyze Results", command=analyze_results)
analyze_button.grid(row=5, column=0, columnspan=3, pady=20)

# Create a text widget for displaying the output with increased height
output_text = tk.Text(window, height=15, width=50, state=tk.DISABLED)
output_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Set row and column weights for resizing
for i in range(7):
    window.grid_rowconfigure(i, weight=1)
for i in range(3):
    window.grid_columnconfigure(i, weight=1)

# Start the main event loop
window.mainloop()
