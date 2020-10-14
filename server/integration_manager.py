import config
import time
from multiprocessing import Process
from integrator import autointegrator

max_jobs = config.max_integrators


def run_job(job):
    p = Process(target = autointegrator.runTest, kwargs = {"config": job["config"], "workdir": job["workdir"],
                                                           "jobID": job['jobID'], "type": job["change_type"],
                                                           "change_id": job["change_id"]
                                                           })
    p.name = job["project_name"]
    p.start()
    print("Started",p.name)
    return p


def manage_integrators(jobs):
    current_jobs = []
    active_projects = []
    if max_jobs == 0:
        print("CI not active on Server...exiting")
        return
    print ("Integration Manager Started...")
    while True:
        while len(current_jobs) == max_jobs:
            for job in current_jobs:
                if not job.is_alive():
                    current_jobs.remove(job)
                    active_projects.remove(job.name)
                print(job.name, "Done")
        j = 0
        for i in range(len(current_jobs), max_jobs):
            if not jobs.empty():
                job=jobs.get()
                if job["project_name"] in active_projects:
                    jobs.put(job)
                p = run_job(job)
                active_projects.append(p.name)
                current_jobs.append(p)
        print("Running Jobs:", len(current_jobs), "Waiting Jobs:", len(jobs))
        time.sleep(20)
