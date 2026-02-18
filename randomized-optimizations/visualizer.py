import matplotlib.pyplot as plt
from matplotlib import colormaps

def plot_schedule(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    cmap = colormaps.get_cmap('tab20')
    for m_idx, machine_tasks in enumerate(data):
        for task in machine_tasks:
            ax.broken_barh([(task.offset, task.duration)], (m_idx - 0.4, 0.8), 
                            facecolors=cmap(task.job_index % 20), edgecolor='black', linewidth=1) 
            ax.text(task.offset + task.duration/2, m_idx, f'J{task.job_index}({task.task_index})', 
                    ha='center', va='center', color='black', fontsize=9) 

    ax.set_xlabel('Time Units')
    ax.set_ylabel('Machine Index')
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels([f'Machine {i}' for i in range(len(data))]
)
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    plt.title('Job Shop Schedule Visualization')
    plt.tight_layout()
    plt.show()