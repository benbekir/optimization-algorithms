from enum import Enum
from dataclasses import dataclass
from helpers.dataloader import parse_instance
from helpers.visualizer import plot_schedule
import random

class Strategy(Enum):
    PLUS = 1
    COMMA = 2

@dataclass
class Task:
    machine_index: int
    job_index: int
    task_index: int
    duration: int
    offset: int

class Candidate:
    def __init__(self, schedule: list[list[Task]]) -> None:
        self.schedule = schedule
        self.time = max(machine[-1].duration + machine[-1].offset for machine in schedule)

    def __repr__(self) -> str:
        # {[[(task.job_index, task.task_index, task.duration, task.offset) for task in machine] for machine in self.schedule]}
        return f"{self.time}"

def create_candidate(schedule, machine_ready_times, task_ready_times, next_task_by_job, active_jobs) -> Candidate:
    # populate schedule for each machine
    while active_jobs:
        selected_job = random.choice(active_jobs)
        selected_task = next_task_by_job[selected_job]

        # queue task for required machine
        machine, duration = data[selected_job][selected_task]
        offset = max(task_ready_times[selected_job], machine_ready_times[machine])
        #print(selected_job, selected_task, "->", machine, duration, ": starts at", offset, "ends at", offset + duration)
        task_info = Task(machine, selected_job, selected_task, duration, offset)
        schedule[machine].append(task_info)

        task_ready_times[selected_job] = duration + offset
        machine_ready_times[machine] += duration

        # check if this was the last task for this job
        next_task_by_job[selected_job] += 1
        if next_task_by_job[selected_job] >= len(data[selected_job]):
            active_jobs.remove(selected_job)
    
    return Candidate(schedule)

def get_initial_candidates(m, num_machines, num_jobs, data):
    candidates = list[Candidate]()
    for _ in range(m):
        # create a schedule for each machine
        schedule = [list[Task]() for _ in range(num_machines)]
        # for each machine, store when it becomes available again
        machine_ready_times = [0] * num_machines
        task_ready_times = [0] * num_jobs
        # for each job, store the index of the next task to schedule
        next_task_by_job = [0] * len(data)
        # jobs that still have tasks left
        active_jobs = [job_index for job_index, _ in enumerate(data)]
        candidate = create_candidate(schedule, machine_ready_times, task_ready_times, next_task_by_job, active_jobs)
        candidates.append(candidate)
    return candidates

def mutate(parents: list[Candidate], l) -> list[Candidate]:
    children_per_parent = l / len(parents)
    children = list[Candidate]()
    for parent in parents:
        for _ in range(int(children_per_parent)):
            # select random task to split at
            jobs = len(parent.schedule)
            tasks = len(parent.schedule[0])
            random_job = random.randint(0, jobs - 1)
            random_task = random.randint(0, tasks - 1)
            chosen_task = parent.schedule[random_job][random_task]
            schedule = [list[Task]() for _ in range(num_machines)]
            
            # copy parent schedule to child
            for i in range(jobs):
                for j in range(tasks):
                    if parent.schedule[i][j].offset <= chosen_task.offset:
                        schedule[i].append(parent.schedule[i][j])
            
            # reconstruct state from the partial schedule
            machine_ready_times = [0] * num_machines
            task_ready_times = [0] * num_jobs
            next_task_by_job = [0] * num_jobs
            
            # scan through copied tasks to rebuild state
            for i, machine_tasks in enumerate(schedule):
                if machine_tasks:
                    last_task = machine_tasks[-1]
                    machine_ready_times[i] = last_task.offset + last_task.duration
                
            # find the highest task_index for each job
            for job_index in range(num_jobs):
                max_task_index = -1
                for machine_tasks in schedule:
                    for task in machine_tasks:
                        if task.job_index == job_index and task.task_index > max_task_index:
                            max_task_index = task.task_index
                            task_ready_times[job_index] = task.offset + task.duration
                next_task_by_job[job_index] = max_task_index + 1
            
            # only jobs with remaining tasks are active
            active_jobs = [job_index for job_index in range(num_jobs) if next_task_by_job[job_index] < len(data[job_index])]
            
            candidate = create_candidate(schedule, machine_ready_times, task_ready_times, next_task_by_job, active_jobs)
            children.append(candidate)
    return children

def solve(strategy: Strategy, m, l, max_generations, num_machines, num_jobs, data) -> Candidate:
    parents = get_initial_candidates(m, num_machines, num_jobs, data)
    offsprings = list[Candidate]()
    for _ in range(max_generations):
        offsprings = mutate(parents, l)
        if strategy == Strategy.PLUS:
            offsprings.extend(parents)
            offsprings.sort(key=lambda x: x.time) 
            parents = []
            for i in range(m):
                parents.append(offsprings[i])
            print(parents)
        elif strategy == Strategy.COMMA:
            offsprings.sort(key=lambda x: x.time) 
            parents = []
            for i in range(m):
                parents.append(offsprings[i])
            print(parents)
    parents.sort(key=lambda x: x.time) 
    return parents[0]

if __name__ == "__main__":
    m = 5
    l = 15
    max_gens = 25

    num_machines, num_jobs, data = parse_instance("jobshop_hackathon_instance.txt", "a")
    candidate = solve(Strategy.PLUS, m, l, max_gens, num_machines, num_jobs, data)
    plot_schedule(candidate.schedule)