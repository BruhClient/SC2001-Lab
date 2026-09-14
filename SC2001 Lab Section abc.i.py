import random
import time
import math
import matplotlib.pyplot as plt

# Implement the hybrid algorithm
def insertion_sort(lst):

    comparison = 0

    for i in range(1, len(lst)):
        current = lst[i]
        j = i - 1

        while j >= 0: # Shift the larger values to the right
            comparison += 1

            if lst[j] <= current:
                break

            lst[j + 1] = lst[j]
            j -= 1

        lst[j + 1] = current

    return lst, comparison


def merge(left, right):

    new = []
    i = j = 0
    comparison = 0

    while i < len(left) and j < len(right): # Compare values from the left and right lists
        comparison += 1

        if left[i] <= right[j]:
            new.append(left[i])
            i += 1
        else:
            new.append(right[j])
            j += 1

    # Add any values that are left over
    new.extend(left[i:])
    new.extend(right[j:])

    return new, comparison


# Original merge sort using merge
def merge_sort(lst):

    n = len(lst)

    if n <= 1:  # Base case: a list with one element is already sorted
        return lst[:], 0

    middle = n // 2

    # Continue dividing until each sublist contains one element
    left, left_comparison = merge_sort(lst[:middle])
    right, right_comparison = merge_sort(lst[middle:])

    sorted_list, merge_comparison = merge(left, right)

    comparison = left_comparison + right_comparison + merge_comparison
    return sorted_list, comparison



# Using insertion when sublist size is smaller than s
# s is the threshold subarray size at which the hybrid algorithm switches from merge sort to insertion sort

def hybrid_sort(lst, s): 

    if s < 1: # s must be more than 0
        raise ValueError("S must be at least 1")

    n = len(lst)

    if n <= 1: # if s is 1, then return the list itself with 0 comparisons
        return lst[:], 0

    if n <= s: # Base case
        return insertion_sort(lst[:])

    middle = n // 2

    left, left_comparison = hybrid_sort(lst[:middle], s)
    right, right_comparison = hybrid_sort(lst[middle:], s)
    sorted_list, merge_comparison = merge(left, right)

    comparison = left_comparison + right_comparison + merge_comparison
    return sorted_list, comparison

# Generate Input Data 
def generate_data(sizes, x):
    """
    Generates dictionaries of datasets with increasing sizes.
    """
    datasets = {}
    for n in sizes:
        print(f"Generating dataset of size {n}...")
        # Generate array of n random integers in the range [1, x]
        datasets[n] = [random.randint(1, x) for _ in range(n)]
    return datasets

# Analyze Time Complexity & Plot 
def analyze_and_plot(datasets, fixed_s):
    """
    Runs the hybrid sort on the datasets, records key comparisons, 
    and plots the empirical results against theoretical complexity.
    """
    sizes = []
    comparisons = []
    
    for n, data in datasets.items():
        print(f"Sorting array of size {n} (This may take a while for large arrays)")
        start_time = time.time()
        
        # Call the existing hybrid_sort function which returns (sorted_list, comparison_count)
        _, comp = hybrid_sort(data, fixed_s) 
        
        elapsed_time = time.time() - start_time
        print(f" -> Completed in {elapsed_time:.2f} seconds with {comp} comparisons.")
        
        sizes.append(n)
        comparisons.append(comp)

    # Initialize Plot
    plt.figure(figsize=(10, 6))
    
    # Plotting empirical results
    plt.plot(sizes, comparisons, marker='o', color='blue', label=f'Empirical Comparisons (S={fixed_s})')

    # Plotting theoretical O(n log n) curve for baseline comparison
    # We find a constant 'c' to scale the theoretical curve to our first data point for a fair visual comparison
    if sizes:
        n0 = sizes[0]
        comp0 = comparisons[0]
        c = comp0 / (n0 * math.log2(n0))
        theoretical_comps = [c * n * math.log2(n) for n in sizes]
        plt.plot(sizes, theoretical_comps, marker='', linestyle='--', color='red', label='Theoretical O(n log n)')

    # Chart formatting
    plt.title(f'Key Comparisons vs. Input Size (Fixed Threshold S={fixed_s})')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Number of Key Comparisons')
    
    # Using a log scale for both axes since input sizes grow exponentially from 1k to 10M
    plt.xscale('log') 
    plt.yscale('log')
    
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.show()
    

# Analyze Time Complexity & Plot again but for fixed n and different values of S
def analyze_and_plot_vs_s(data, s_values):

    # Instead of keeping a fixed S, we now fix n and vary S.
    # We run hybrid sort on a single fixed dataset with a range of values for S, record key comparisons, and plot the results
    
    n = len(data)
    s_list = []
    comparisons = []

    for s in s_values:
        print(f"Sorting array of size {n} with S={s} (This may take a while for large arrays)")
        start_time = time.time()

        # Use a fresh copy of data each time to avoid insertion_sort mutating input
        _, comp = hybrid_sort(data[:], s)

        elapsed_time = time.time() - start_time
        print(f" -> Completed in {elapsed_time:.2f} seconds with {comp} comparisons.")

        s_list.append(s)
        comparisons.append(comp)


    # Initialize Plot
    plt.figure(figsize=(10,6))

    # Plotting empirical results
    plt.plot(s_list, comparisons, marker='o', color='green', label=f'Empirical Comparisons (n={n})')

    # Chart formatting
    plt.title(f'Key Comparisons vs. Threshold S (Fixed Input Size n={n})')
    plt.xlabel('Threshold S')
    plt.ylabel('Number of Key Comparisons')

    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.show()

    return s_list,comparisons

# Study how to determine an optimal value of S across different input sizes of n

def find_optimal_s(datasets, s_values):

    # For each dataset (of different sizes n), we do the following:
        # 1. Test a range of S values
        # 2. Record the S value that minimizes the number of key operations
        # 3. Plot optimal S found against input size n.

    optimal_s_per_n = {}

    for n, data in datasets.items():
        print(f"\nFinding optimal S for array of size {n}...")
        best_s = None
        best_comp = None

        for s in s_values:
            _, comp = hybrid_sort(data[:], s)
            print(f"S{s} -> {comp} comparisons")

            if best_comp is None or comp < best_comp:
              best_comp = comp
              best_s = s

        optimal_s_per_n[n] = (best_s, best_comp)
        print(f" -> Optimal S for n={n} is {best_s} with {best_comp} comparisons")

    # Initialize Plot
    ns = list(optimal_s_per_n.keys())
    best_s_values = [optimal_s_per_n[n][0] for n in ns]

    plt.figure(figsize=(10,6))
    plt.plot(ns, best_s_values, marker='o', color='purple', label='Optimal S')

    # Chart Formatting
    plt.title('Optimal Threshold S vs. Input Size n')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Optimal S')

    # Log scale for x-axis (n grows exponentially)
    plt.xscale('log')

    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.show()

    return optimal_s_per_n

# Execution Block
if __name__ == "__main__":
    # Define sizes stepping from 1,000 to 10,000,000
    test_sizes = [1000, 10000, 100000, 1000000, 10000000] 
    
    max_value_x = 1000000 # Example maximum value for the dataset integers
    fixed_threshold_s = 10 # Example fixed value for threshold S
    
    # Run Part (b) to generate data
    print("--- Starting Data Generation ---")
    generated_datasets = generate_data(test_sizes, max_value_x)
    
    # Run Part (c.i) to sort and plot
    print("\n--- Starting Sorting & Analysis ---")
    analyze_and_plot(generated_datasets, fixed_threshold_s)

    # Run Part (c.ii) to sort and plot

    print("\n--- Starting Sorting & Analysis ---")
    fixed_n_dataset = generated_datasets[1000000]
    s_values_cii = [2,5,10,20,30,50,75,100,150,200]
    analyze_and_plot_vs_s(fixed_n_dataset, s_values_cii)
    
    # Run Part (c.iii) to determine optimal value of S for each test size
    print("\n--- Starting Optimal S Analysis ---")
    optimal_s_sizes = [1000, 10000, 100000, 1000000]
    optimal_s_datasets = generate_data(optimal_s_sizes, max_value_x)
    s_values_ciii = [2,5,10,20,30,50,75,100]
    find_optimal_s(optimal_s_datasets, s_values_ciii)
    
