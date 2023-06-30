import sys
import dill as pickle
import htcondor

class Condor_executor:
    
    def __init__(self, executable_class, *params, **kw_params):
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


        name = f"gravitic"
        if "name" in kwargs:
            name += f"/{kwargs['name']}"
        else:
            name += f"/{self.exe_class.__name__}"
        
        submit_description = {
            "executable": "gravitic.schedulers.htcondor",
            "arguments": "--pickle saved.pickle",
            #"accounting_group": self.meta["accounting group"],
            "output": f"{self.rundir}/{name}.out",
            "error": f"{self.rundir}/{name}.err",
            "log": f"{self.rundir}/{name}.log",
            "request_cpus": kwargs.get('cpus', 1),
            #"getenv": "true",
            "batch_name": name,
            #"request_memory": "8192MB",
            #"should_transfer_files": "YES",
            "request_disk": kwargs.get('disk', "8192MB"),
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
