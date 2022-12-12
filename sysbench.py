import subprocess
import sys

thread_nums = []

start = 2
while start <= 1024:
    thread_nums.append(start)
    start *= 2

sched_name = sys.argv[1]

with open(sched_name+".csv", 'w') as f:
        print("name,num_threads,total_time,total_events,min,avg,max,95p,fairness_events_avg,fairness_events_stddev,fairness_time_avg,fairness_time_stddev,", file=f)

for t in thread_nums:
    cmd = "/home/kunal/source/ghost-userspace/bazel-bin/ghost_bench " + str(t)
    res = subprocess.run(cmd.split(), capture_output=True)
    #print(res.stderr)
    data = dict()
    data["name"] = sched_name
    data["num_threads"] = t
    for line in res.stdout.splitlines():
        line = line.decode("utf-8")
        if "total time:" in line:
            data["total_time"] = line.split()[2][:-1]
        elif "total number of events:" in line:
            data["total_events"] = line.split()[4]
        elif "min:" in line:
            data["min"] = line.split()[1]
        elif "avg:" in line:
            data["avg"] = line.split()[1]
        elif "max:" in line:
            data["max"] = line.split()[1]
        elif "95th" in line:
            data["95p"] = line.split()[2]
        elif "events" in line:
            data["fairness_events_avg"] = line.split()[2].split('/')[0]
            data["fairness_events_stddev"] = line.split()[2].split('/')[1]
        elif "execution time" in line:
            data["fairness_time_avg"] = line.split()[3].split('/')[0]
            data["fairness_time_stddev"] = line.split()[3].split('/')[1]
    with open(sched_name+".csv", 'a') as f:
            for i in data:
                print(data[i], end=",", file=f)
            print("",file=f)
