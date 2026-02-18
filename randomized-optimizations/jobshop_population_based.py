from enum import Enum
from dataclasses import dataclass
from dataloader import parse_instance
from visualizer import plot_schedule
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
        return f"{self.time} {[[(task.job_index, task.task_index, task.duration, task.offset) for task in machine] for machine in self.schedule]}"

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

        # populate schedule for each machine
        while active_jobs:
            selected_job = random.choice(active_jobs)
            selected_task = next_task_by_job[selected_job]

            # queue task for required machine
            machine, duration = data[selected_job][selected_task]
            offset = max(task_ready_times[selected_job], machine_ready_times[machine])
            print(selected_job, selected_task, "->", machine, duration, ": starts at", offset, "ends at", offset + duration)
            task_info = Task(machine, selected_job, selected_task, duration, offset)
            schedule[machine].append(task_info)

            task_ready_times[selected_job] = duration + offset
            machine_ready_times[machine] += duration

            # check if this was the last task for this job
            next_task_by_job[selected_job] += 1
            if next_task_by_job[selected_job] >= len(data[selected_job]):
                active_jobs.remove(selected_job)

        candidates.append(Candidate(schedule))
    return candidates

def mutate(parents, l) -> list[Candidate]:
    pass

def solve(strategy: Strategy, m, l, max_generations, num_machines, num_jobs, data) -> Candidate:
    parents = get_initial_candidates(m, num_machines, num_jobs, data)
    offsprings = list[Candidate]()
    for _ in range(max_generations):
        offsprings = mutate(parents, l)
        if strategy == Strategy.PLUS:
            pass
        elif strategy == Strategy.COMMA:
            pass
    return parents[0]

if __name__ == "__main__":
    m = 10
    l = 1
    max_gens = 100

    num_machines, num_jobs, data = parse_instance("jobshop.txt", "la02")
    candidate = solve(Strategy.PLUS, m, l, max_gens, num_machines, num_jobs, data)
    print(candidate.time)
    plot_schedule(candidate.schedule)