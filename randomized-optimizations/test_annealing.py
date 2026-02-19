from jobshop_trajectory_based import*
import matplotlib.pyplot as plt
INSTANCE_NAME = "a"
FILENAME = "jobshop_hackathon_instance.txt"
ITERATIONS=100000
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
    best_makespan, best_sequence,history_best_makespan,history_current_makespan = simulate_annealing(data, num_machines, num_jobs,ITERATIONS)
    end_time = time.time()
    duration = end_time - start_time

    print("\n--- Results ---")
    print(f"Best Makespan Found: {best_makespan}")
    print(f"Improvement: {random_makespan - best_makespan} units")
    print(f"Time Taken: {duration:.4f} seconds")
    print(f"Sequence: {best_sequence}")

    plt.figure(figsize=(12, 6))
    plt.plot(history_current_makespan, label='$f(x_{new})$: Trajectory', color='#3498db', alpha=0.4, linewidth=0.7)
    
    plt.plot(history_best_makespan, label='Best $f(x)$: Optimal Path', color='#e74c3c', linewidth=2)
    plt.title('Simulated Annealing: Minimization Move Analysis', fontsize=15, pad=20)
    plt.xlabel('Iterations ($x$)', fontsize=12)
    plt.ylabel('Makespan $f(x)$', fontsize=12)
    
    plt.legend(loc='upper right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
    
run_test()