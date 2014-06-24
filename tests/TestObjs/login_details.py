username = ""
password = ""

if not username or not password:
    err_str = \
        "Fill out login_details.py with your username and password."
    raise Exception(err_str)