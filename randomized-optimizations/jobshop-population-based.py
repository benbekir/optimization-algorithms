import re
#Tabu Search and Simulated Annealing
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
            machine=line_content[j]
            time=line_content[j+1]
            job_data_copy.append((machine,time))
        jobs_data.append(job_data_copy)
    return jobs_data
data=parse_instance("jobshop.txt","abz6")
print(data)
            
    