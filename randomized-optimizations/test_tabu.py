from jobshop_trajectory_based import*
import matplotlib.pyplot as plt
def run_tabu_test():
    INSTANCE_NAME = "abz7"
    FILENAME = "jobshop.txt"
    ITERATIONS = 5000
    TABU_SIZE = 30

    try:
        num_jobs, num_machines, data = parse_instance(FILENAME, INSTANCE_NAME)
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"--- Testing Tabu Search on {INSTANCE_NAME} ---")
    
    start_time = time.time()
    best_makespan, best_sequence, history_best_makespan, history_current_makespan = tabu_search(data, num_machines, num_jobs, ITERATIONS, TABU_SIZE)
    duration = time.time() - start_time
    print(f"Best Makespan: {best_makespan}")
    print(f"Time: {duration:.2f}s")
   
    plt.figure(figsize=(12, 6))
    plt.plot(history_current_makespan, label='Current $f(x)$ (Tabu Trajectory)', color='blue', alpha=0.5)
    plt.plot(history_best_makespan, label='Best $f(x)$', color='#e74c3c', linewidth=2)
    plt.title(f'Tabu Search Optimization: {INSTANCE_NAME}')
    plt.xlabel('Iteration')
    plt.ylabel('Makespan')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

run_tabu_test()