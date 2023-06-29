import sys
import dill as pickle
from functools import wraps, update_wrapper
import htcondor

class Condor_executor:
    
    def __init__(self, executable_class):
        self.exe_class = executable_class
        self.__name__ = self.exe_class.__name__
        self.rundir = "."
        pass

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.submit_to_condor()
    
    def build(self):
        self.create_pickle()

    def submit_to_condor(self):
        self.create_pickle()
        self.submit_job()
        
    @classmethod
    def run_pickle(cls, pickle_file):
        with open(pickle_file, 'rb') as pf:
            executable_class, args, kwargs = pickle.load(pf)
        executor = cls(executable_class)
        executor.exe_class(*args, **kwargs)

    def create_pickle(self):
        with open('saved.pickle', 'wb') as pf:
            pickle.dump([self.exe_class, self.args, self.kwargs], pf)
    
    def build_submit_description(self, *args, **kwargs):
        
        submit_description = {
            "executable": "gravitic.schedulers.htcondor",
            "arguments": "run --pickle saved.pickle",
            #"accounting_group": self.meta["accounting group"],
            "output": f"{self.rundir}/pesummary.out",
            "error": f"{self.rundir}/pesummary.err",
            "log": f"{self.rundir}/pesummary.log",
            #"request_cpus": self.meta["multiprocess"],
            #"getenv": "true",
            #"batch_name": f"PESummary/{self.production.event.name}/{self.production.name}",
            #"request_memory": "8192MB",
            #"should_transfer_files": "YES",
            #"request_disk": "8192MB",
        }
        return submit_description
        
    def submit_job(self):

        hostname_job = htcondor.Submit(self.build_submit_description())

        # try:
        #     # There should really be a specified submit node, and if there is, use it.
        #     schedulers = htcondor.Collector().locate(
        #         htcondor.DaemonTypes.Schedd, config.get("condor", "scheduler")
        #     )
        #     schedd = htcondor.Schedd(schedulers)
        # except:  # NoQA
        #     # If you can't find a specified scheduler, use the first one you find
        schedd = htcondor.Schedd()
        with schedd.transaction() as txn:
            cluster_id = hostname_job.queue(txn)
            print(cluster_id)

if __name__ == '__main__':
    if sys.argv[1] == "run":
        scheduler_exe = Condor_executor.run_pickle('saved.pickle')
    # elif sys.argv[1] == "condor":
    #     test = Condor_executor(test_function)
    #     test.submit_to_condor()
    # elif sys.argv[1] == "build":
    #     test = Condor_executor(test_function)
    #     test.build()
