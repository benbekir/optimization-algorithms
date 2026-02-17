from jobshop_population_based import*
import matplotlib.pyplot as plt
INSTANCE_NAME = "abz6"
FILENAME = "jobshop.txt"
ITERATIONS=50000
def run_test():
    try:
        num_jobs, num_machines, data = parse_instance(FILENAME, INSTANCE_NAME)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    print(f"--- Testing Simulated Annealing on {INSTANCE_NAME} ---")
    print(f"Jobs: {num_jobs}, Machines: {num_machines}")
    
    random_seq = initialize_sequence(num_machines, num_jobs)
    random_makespan = calculate_makespan(random_seq, num_machines, num_jobs, data)
    print(f"Initial Random Makespan: {random_makespan}")

    start_time = time.time()
    
    best_m, best_s,history_best_makespan,history_current_makespan = simulate_annealing(data, num_machines, num_jobs,ITERATIONS)
    
    end_time = time.time()
    duration = end_time - start_time

    print("\n--- Results ---")
    print(f"Best Makespan Found: {best_m}")
    print(f"Improvement: {random_makespan - best_m} units")
    print(f"Time Taken: {duration:.4f} seconds")
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(history_current_makespan, label='Current Makespan (Exploration)', alpha=0.3, color='blue')
    plt.plot(history_best_makespan, label='Best Makespan (Optimization)', color='red', linewidth=2)

    plt.title('Simulated Annealing Evolution for abz6')
    plt.xlabel('Iteration')
    plt.ylabel('Makespan')
    plt.legend()
    plt.grid(True)
    plt.savefig('annealing_evolution.png') # Saves the image to your folder
    
run_test()