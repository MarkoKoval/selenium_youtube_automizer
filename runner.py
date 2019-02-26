from SignIn import *

if __name__ == "__main__":
    videos = {"6bJrHkJ2M_I&t=": {"subscribe": 0, "evaluate": "like"}}
    values = [(k, v["subscribe"], v["evaluate"]) for k, v in videos.items()]*16
    start = time.time()
    do_stuff_in_some_processes(values)
    end = time.time()
    print(end - start)