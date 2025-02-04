import os
from typing import Callable
import cloudpickle


# If file fn exists, cloudpickle.loads its contents and returns them.
# Otherwise, it calls fun and cloudpickle.dumps its return value to fn, and returs it.
def caching_query(fun: Callable, fn: str):
    if os.path.exists(fn):
        with open(fn, "rb") as f:
            return cloudpickle.load(f)
    else:
        result = fun()
        with open(fn, "wb") as f:
            cloudpickle.dump(result, f)

        return result
