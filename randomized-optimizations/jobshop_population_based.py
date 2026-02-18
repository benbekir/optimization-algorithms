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

def is_task_available(job_index, task_index, tasks: list[Task], num_machines, machine_ready_times, data) -> bool:
    if task_index == 0:
        return True
    task = tasks[job_index * num_machines + task_index - 1]
    allowed_start_time = task.duration + task.offset
    required_machine, _ = data[job_index][task_index]
    return machine_ready_times[required_machine] >= allowed_start_time


def get_initial_candidates(m, num_machines, num_jobs, data):
    candidates = list[Candidate]()
    for _ in range(m):
        # create a schedule for each machine
        schedule = [list[Task]() for _ in range(num_machines)]
        # create a task list for reverse lookups
        task_list: list[Task] = [None] * (num_jobs * num_machines)
        # for each machine, store when it becomes available again
        machine_ready_times = [0] * num_machines
        # for each job, store the index of the next task to schedule
        next_task_by_job = [0] * len(data)
        # jobs that still have tasks left
        active_jobs = [job_index for job_index, _ in enumerate(data)]

        # populate schedule for each machine
        while active_jobs:
            allowed_active_jobs = [job for job in active_jobs if is_task_available(job, next_task_by_job[job], task_list, num_machines, machine_ready_times, data)]
            # wait for machines in idle for other machines
            if len(allowed_active_jobs) == 0:
                selected_job = random.choice(active_jobs)
                selected_task = next_task_by_job[selected_job]
                previous_task = task_list[selected_job * num_machines + selected_task - 1]
                machine, duration = data[selected_job][selected_task]
                print("waiting in idle from", machine_ready_times[machine])
                machine_ready_times[machine] = previous_task.duration + previous_task.offset
                print("... until", machine_ready_times[machine], "(", duration, "+", previous_task.offset, ")")
            else:
                selected_job = random.choice(allowed_active_jobs)
                selected_task = next_task_by_job[selected_job]

            # queue task for required machine
            machine, duration = data[selected_job][selected_task]
            print(selected_job, selected_task, "->", machine, duration)
            offset = machine_ready_times[machine]
            task_info = Task(machine, selected_job, selected_task, duration, offset)
            schedule[machine].append(task_info)
            task_list[selected_job * num_machines + selected_task] = task_info
            machine_ready_times[machine] += duration

            # check if this was the last task for this job
            next_task_by_job[selected_job] += 1
            if next_task_by_job[selected_job] >= len(data[selected_job]):
                active_jobs.remove(selected_job)

        candidates.append(Candidate(schedule))
    # calculate shortest possible duration
    durations = [sum(task_info.duration for task_info in candidates[0].schedule[machine]) for machine in range(num_machines)]
    return candidates, max(durations)

def solve(strategy: Strategy, m, l, num_machines, num_jobs, data):
    candidates, best_possible_time = get_initial_candidates(m, num_machines, num_jobs, data)
    return candidates

if __name__ == "__main__":
    m = 1
    l = 1
    num_machines, num_jobs, data = parse_instance("jobshop.txt", "la02")
    candidates = solve(Strategy.PLUS, m, l, num_machines, num_jobs, data)
    plot_schedule(candidates[0].schedule)