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
         
 #This is the function that calculates the makespan
 #We basically take the current operation from our sequence and see what machine is assigned to it and what is the machine's time to do that operation
 #The start time for the free machine is when the machine finishes its job and when the job is free to move on to the next step
 #After iterating through the whole steps of the sequence we return the biggest value of machine_free_time. The reason is, that the sequnce ends when the biggest time ends.
def calculate_makespan(sequence, num_machines, num_jobs, data):
    machine_free_time=[0]*num_machines
    job_op_index_next_time=[0]*num_jobs
    job_current_operation=[0]*num_jobs
    for job_id in sequence:
        op_current=job_current_operation[job_id]
        if op_current>= len(data[job_id]):
            continue
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
def get_neighbour_annealing(sequence):
    neighbour=list(sequence)
    idx1,idx2=random.sample(range(len(neighbour)), 2)
    neighbour[idx1],neighbour[idx2]=neighbour[idx2],neighbour[idx1]
    return neighbour 
def get_neighbour_tabu(sequence):
    neighbour=list(sequence)
    idx1,idx2=random.sample(range(len(neighbour)), 2)
    neighbour[idx1],neighbour[idx2]=neighbour[idx2],neighbour[idx1]
    return neighbour, (idx1,idx2) 

#This is the simulate annealing algorithm. The way I thought of it is the same way it was presented in the lecture.
#We have a Temperature T and a cooling rate, through which we control how sensitive the algorithm is to wrong choices
#Through each iteration we take 2 indices from our current sequence randomly and swap their places, thus obtaining a new sequence and computing their makespan. If their makespan proves useful we keep the current sequence and makespan and compare them to the best ones
def simulate_annealing(data,num_machines,num_jobs,num_iterations):
    current_seq=initialize_sequence(num_machines,num_jobs)
    current_makespan=calculate_makespan(current_seq,num_machines,num_jobs,data)
    best_seq=list(current_seq)
    best_makespan=current_makespan
    history_best_makespan=[]
    history_current_makespan=[]
    T=5000.0
    cooling_rate=0.9999
    for i in range(num_iterations):
        neighbor=get_neighbour_annealing(current_seq)
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

#This is the tabu search algorithm
#For each iteration we swap indexes for a given number of times, in this case 50 times and add in a list the current sequence, the makespan and the pairs of indexes
#After this we sort the list in ascending order and verify if move(the pair of indexes) is not in the tabulist or if the current maklespan is better than the best makespan
#We use an or in that if because of something called Aspiration. What is the purpose of Aspiration, well basically if we find something that is better than everything we have seen, but is in the tabu_list, we still take it as a solution
#The rest of the algorithm is fairly similar to the annealing, except that we also have to check if the size of the list has overtaken the size of the tabu
def tabu_search(data, num_machines, num_jobs,Iterations, tabu_size):
    current_seq=initialize_sequence(num_machines,num_jobs)
    current_makespan= calculate_makespan(current_seq,num_machines,num_jobs,data)
    best_seq=list(current_seq)
    best_makespan=current_makespan
    tabu_list=[]
    history_best_makespan=[]
    history_current_makespan=[]
    for i in range(Iterations):
        neighbor=[]
        for j in range(50):
            neighbor_copy,move=get_neighbour_tabu(current_seq)
            makespan=calculate_makespan(neighbor_copy,num_machines,num_jobs,data)
            neighbor.append((neighbor_copy,makespan,move))
        neighbor.sort(key=lambda x:x[1])
        for neighbor, makepsan,move in neighbor:
            if move not in tabu_list or makepsan<best_makespan:
                current_seq=neighbor
                current_makespan=makepsan
                tabu_list.append(move)
                if len(tabu_list)>tabu_size:
                    tabu_list.pop(0)
                if current_makespan<best_makespan:
                    best_seq=current_seq
                    best_makespan=current_makespan
                break
        history_best_makespan.append(best_makespan)
        history_current_makespan.append(current_makespan)
    return best_makespan,best_seq,history_best_makespan,history_current_makespan