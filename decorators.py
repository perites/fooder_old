import logging

from functools import wraps


def error_catcher(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            answer = func(*args, **kwds)
            return answer

        except Exception as e:
            logging.error(f"Error occured : {e}")
            return {"message": str(e)}, 500

    return wrapper
