from .htcondor import Condor_executor


# wrap the executor to allow for deferred calling
def Schedule(function=None, **kwargs):
    if function:
        return Condor_executor(function)
    else:
        def wrapper(function):
            return Condor_executor(function, **kwargs)

        return wrapper


