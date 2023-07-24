import logging

from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def error_catcher(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            return func(*args, **kwds)

        except Exception as e:
            logging.error(f"Error occured : {e}")
            return {"message": str(e)}, 500

    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        if current_user.is_authenticated:
            return func(*args, **kwds)
        else:
            next_url = url_for(func.__name__, *args, **kwds)
            return redirect(f"/login?next_url={next_url}")

    return wrapper


# def function_name(func):
#     @wraps(func)
#     def wrapper(*args, **kwds):
#         pass
#     return wrapper
