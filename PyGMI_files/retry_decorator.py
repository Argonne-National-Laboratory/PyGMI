# -*- coding: utf-8 -*-
import time

# Retry decorator with return
def retry_with(tries=2,ans_type=int,default_ans=-1,wait=1):
    '''Retries a function or method until it returns an answer of the right type
    (e.g. int,float,str) and does not raise not an exception. If it runs out of tries
    a default answer is returned.
    '''
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries = tries # make mutable
            success=False
            while mtries >0 and not(success):
                try:
                    ans = f(*args, **kwargs) # first attempt
                    success=(type(ans)==ans_type)
                except:
                    success=False
                    mtries -= 1      # consume an attempt
                    time.sleep(wait)
            if success:
                res=ans
            else:
                print "ran out of retries: exception with function", f.func_name
                res=default_ans # Ran out of tries :-(
            return res
        return f_retry # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator

# Retry decorator without return
def retry(tries=2,wait=1):
    '''Retries a function or method until it does not raise not an exception.
    If it runs out of tries, nothing is done, and the program continue.
    '''
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries = tries # make mutable
            success=False
            while mtries >0 and not(success):
                try:
                    f(*args, **kwargs) # first attempt
                    success=True
                except:
                    success=False
                    mtries -= 1      # consume an attempt
                    time.sleep(wait)
            if not(success):
                print "ran out of retries: exception with function", f.func_name
        return f_retry # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator
