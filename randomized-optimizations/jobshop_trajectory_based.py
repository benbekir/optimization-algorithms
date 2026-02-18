import re
import random
import time
import math
def parse_instance(file_name, instance_name):
    with open(file_name,'r') as f:
        lines=f.readlines()
    start_idx=-1
    for i,line in enumerate(lines):
       if f"instance {instance_name}" in line.strip():
           start_idx=i
           break
    if start_idx == -1:
        raise ValueError(f"Instance {instance_name} not found in file {file_name}.")
    skip_line=start_idx+4
    num_jobs,num_machines=map(int, lines[skip_line].split())
    jobs_data=[]
    for i in range(1, num_jobs+1):
        line_content=lines[skip_line+i].strip().split()
        job_data_copy=[]
        for j in range(0, len(line_content),2):
            machine=int(line_content[j])
            time=int(line_content[j+1])
            job_data_copy.append((machine,time))
        jobs_data.append(job_data_copy)
    return num_machines, num_jobs,jobs_data
         
 #Tabu Search and Simulated Annealing
def calculate_makespan(sequence, num_machines, num_jobs, data):
    machine_free_time=[0]*num_machines
    job_op_index_next_time=[0]*num_jobs
    job_current_operation=[0]*num_jobs
    for job_id in sequence:
        op_current=job_current_operation[job_id]
        machine_id,duration=data[job_id][op_current]
        start_time=max(machine_free_time[machine_id], job_op_index_next_time[job_id])
        end_time=start_time+duration
        machine_free_time[machine_id]=end_time
        job_op_index_next_time[job_id]=end_time
        job_current_operation[job_id]+=1
    return max(machine_free_time)

def initialize_sequence(num_machines,num_jobs):
 sequence=[]
 for i in range(num_jobs):
    sequence.extend([i]*num_machines)
 random.shuffle(sequence)
 return sequence
def get_neighbour(sequence):
    neighbour=list(sequence)
    idx1,idx2=random.sample(range(len(neighbour)), 2)
    neighbour[idx1],neighbour[idx2]=neighbour[idx2],neighbour[idx1]
    return neighbour 

def simulate_annealing(data,num_machines,num_jobs,num_iterations):
    current_seq=initialize_sequence(num_machines,num_jobs)
    current_makespan=calculate_makespan(current_seq,num_machines,num_jobs,data)
    best_seq=list(current_seq)
    best_makespan=current_makespan
    history_best_makespan=[]
    history_current_makespan=[]
    T=900.0
    cooling_rate=0.99
    for i in range(num_iterations):
        neighbor=get_neighbour(current_seq)
        neighbor_makepsan=calculate_makespan(neighbor,num_machines,num_jobs,data)
        diff=neighbor_makepsan-current_makespan
        if diff<0 or random.random()<math.exp(-diff/T):
            current_seq=neighbor
            current_makespan=neighbor_makepsan
        if current_makespan<best_makespan:
            best_seq=list(current_seq)
            best_makespan=current_makespan
        T*=cooling_rate
        history_best_makespan.append(best_makespan)
        history_current_makespan.append(current_makespan)
    return best_makespan,best_seq,history_best_makespan,history_current_makespan
