def calculate_metrics(processes, completion_times):
    # Helper function for calculating turnaround and waiting times.
    results = []
    tot_turnaround, tot_waiting = 0, 0

    for p in processes:
        pid = p['id']
        comp_time = completion_times[pid]
        turnaround = comp_time - p['arrival']
        waiting = turnaround - p['burst']

        tot_turnaround += turnaround
        tot_waiting += waiting

        results.append({
            'ID': pid, 'Dish': p['name'], 'Arrival': p['arrival'],
            'Burst': p['burst'], 'Completion': comp_time,
            'Turnaround': turnaround, 'Waiting': waiting
        })

    n = len(processes)
    return results, tot_turnaround/n, tot_waiting/n

def print_results(algo_name, results, avg_turnaround, avg_waiting, exec_log):
    print(f"\n{'='*50}")
    print(f"Algorithm: {algo_name}")
    print(f"{'='*50}")

    print("Execution Timeline:")
    timeline = " -> ".join([f"[T:{start}-{end} {pid}]" for pid, start, end in exec_log])
    print(timeline + "\n")

    print(f"{'ID':<4} | {'Dish':<18} | {'Comp':<5} | {'Turn':<5} | {'Wait':<5}")
    print("-" * 47)
    for r in results:
        print(f"{r['ID']:<4} | {r['Dish']:<18} | {r['Completion']:<5} | {r['Turnaround']:<5} | {r['Waiting']:<5}")

    print(f"\nAverage Turnaround Time: {avg_turnaround:.2f} mins")
    print(f"Average Waiting Time:    {avg_waiting:.2f} mins")

def fifo_scheduling(processes):
    time = 0
    completion_times = {}
    exec_log = []

    # Sort by arrival time
    procs = sorted(processes, key=lambda x: x['arrival'])

    for p in procs:
        if time < p['arrival']:
            time = p['arrival']
        start_time = time
        time += p['burst']
        completion_times[p['id']] = time
        exec_log.append((p['id'], start_time, time))

    metrics, avg_t, avg_w = calculate_metrics(processes, completion_times)
    return metrics, avg_t, avg_w, exec_log

def sjf_non_preemptive(processes):
    time = 0
    completed = 0
    n = len(processes)
    completion_times = {}
    exec_log = []

    # Sort primarily by arrival to establish sequence
    procs = sorted(processes, key=lambda x: x['arrival'])
    is_completed = {p['id']: False for p in processes}

    while completed < n:
        # Find all available processes at the current time
        available = [p for p in procs if p['arrival'] <= time and not is_completed[p['id']]]

        if not available:
            time += 1
            continue

        # Select one with the shortest burst time
        shortest = min(available, key=lambda x: x['burst'])

        start_time = time
        time += shortest['burst']
        completion_times[shortest['id']] = time
        is_completed[shortest['id']] = True
        exec_log.append((shortest['id'], start_time, time))
        completed += 1

    metrics, avg_t, avg_w = calculate_metrics(processes, completion_times)
    return metrics, avg_t, avg_w, exec_log

def round_robin(processes, quantum):
    time = 0
    ready_queue = []
    completed = 0
    n = len(processes)

    rem_time = {p['id']: p['burst'] for p in processes}
    completion_times = {}
    exec_log = []

    procs = sorted(processes, key=lambda x: x['arrival'])
    idx = 0

    # Add init arrivals
    while idx < n and procs[idx]['arrival'] <= time:
        ready_queue.append(procs[idx]['id'])
        idx += 1

    while completed < n:
        if not ready_queue:
            time += 1
            while idx < n and procs[idx]['arrival'] <= time:
                ready_queue.append(procs[idx]['id'])
                idx += 1
            continue

        current_pid = ready_queue.pop(0)
        time_slice = min(quantum, rem_time[current_pid])

        start_time = time
        time += time_slice
        rem_time[current_pid] -= time_slice
        exec_log.append((current_pid, start_time, time))

        # Add new arrivals during time slice
        while idx < n and procs[idx]['arrival'] <= time:
            ready_queue.append(procs[idx]['id'])
            idx += 1

        # Re-queue if not finished
        if rem_time[current_pid] > 0:
            ready_queue.append(current_pid)
        else:
            completion_times[current_pid] = time
            completed += 1

    metrics, avg_t, avg_w = calculate_metrics(processes, completion_times)
    return metrics, avg_t, avg_w, exec_log

if __name__ == "__main__":
    # Input Dataset
    kitchen_orders = [
        {'id': '01', 'name': 'Steak (well-done)', 'arrival': 0, 'burst': 10},
        {'id': '02', 'name': 'Caesar Salad',      'arrival': 1, 'burst': 3},
        {'id': '03', 'name': 'Pasta',             'arrival': 2, 'burst': 7},
        {'id': '04', 'name': 'Burger',            'arrival': 3, 'burst': 5},
        {'id': '05', 'name': 'Fries (appetizer)', 'arrival': 4, 'burst': 2}
    ]

    # First-In First-Out
    res_fifo, t_fifo, w_fifo, log_fifo = fifo_scheduling(kitchen_orders)
    print_results("FIFO (First-In, First-Out)", res_fifo, t_fifo, w_fifo, log_fifo)

    # Shortest Job First
    res_sjf, t_sjf, w_sjf, log_sjf = sjf_non_preemptive(kitchen_orders)
    print_results("SJF (Shortest Job First)", res_sjf, t_sjf, w_sjf, log_sjf)

    # Round Robin
    quantum = 3
    res_rr, t_rr, w_rr, log_rr = round_robin(kitchen_orders, quantum)
    print_results(f"Round Robin (Quantum = {quantum})", res_rr, t_rr, w_rr, log_rr)