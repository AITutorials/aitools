import os
import argparse

from importlib import util
from os.path import basename
from os.path import exists
from types import ModuleType
import math
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape


class UserTasks(TaskSet):
    @task
    def get_root(self):
        self.client.request(**request_body)


class WebsiteUser(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]



class StepLoadShape(LoadTestShape):
    """
    A step load shape
    Keyword arguments:
        step_time -- Time between steps
        step_load -- User increase amount at each step
        spawn_rate -- Users to stop/start per second at every step
        time_limit -- Time limit in seconds
    """

    def tick(self):
        run_time = self.get_run_time()

        if run_time > time_limit:
            return None

        current_step = math.floor(run_time / step_time) + 1
        return (current_step * step_load, spawn_rate)


def load_package_from_path(pkg_path: str, config_name) -> ModuleType:
    init_path = f"{pkg_path}/__init__.py"
    if not os.path.exists(init_path):
        with open(init_path, "w") as fp:
            fp.write("")
    name = basename(config_name)

    spec = util.spec_from_file_location(name, init_path)
    module = util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "--uri", "-u", required=True, help="本地浏览器打开地址", default="http://0.0.0.0:80"
    )
    parser.add_argument("--config", "-c", required=True, help="压测服务的配置文件名")
    args = parser.parse_args()
    uri = args.uri
    uri_port = uri.replace("http://", "").replace("https://", "").split(":")
    config = args.config
    path = os.getcwd()
    import sys
    sys.path.append(path)
    from stress_config import (
        url,
        request_body,
        step_time,
        step_load,
        spawn_rate,
        time_limit,
    )
    global request_body
    global step_time
    global step_load
    global spawn_rate
    global time_limit
    comm = f"locust -f {os.path.abspath(__file__)} --host {url} --web-host={uri_port[0]} --web-port={uri_port[1]}"
    os.system(comm)


if __name__ == "__main__":
    main()
