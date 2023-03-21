import os
import math
import argparse
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
from stress_config import *


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


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        "--uri", "-u", required=True, help="本地浏览器打开地址", default="http://0.0.0.0:80"
    )
    parser.add_argument("--config", "-c", required=True, help="压测服务的配置文件路径")
    args = parser.parse_args()
    uri = args.uri
    uri_port = uri.replace("http://", "").replace("https://", "").split(":")
    config = args.config
    # 获取当前文件所在路径
    config_file = os.path.abspath(__file__)
    new_config = "/".join(config_file.split("/")[:-1] + ["stress_config.py"])
    comm = f"cp {config} {new_config}"
    os.system(comm)
    from stress_config import url
    comm = f"locust -f {config_file} --host {url} --web-host={uri_port[0]} --web-port={uri_port[1]}"
    os.system(comm)


if __name__ == "__main__":
    main()
