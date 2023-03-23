import os
import argparse

from importlib import util
from os.path import basename
from os.path import exists
from types import ModuleType
import math
from locust import HttpUser, TaskSet, task, constant, task, events

import gevent
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging

setup_logging("INFO", None)


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
    #parser.add_argument(
    #    "--uri", "-u", required=True, help="本地浏览器打开地址", default="0.0.0.0:80"
    #)
    parser.add_argument("--config", "-c", required=True, help="压测服务的配置文件名")
    args = parser.parse_args()
    config = args.config
    path = os.getcwd()
    import sys
    sys.path.append(path)
    from stress_config import (
        url,
        request_body,
        max_rps,
        spawn_time,
        time_limit,
    )

    class UserTasks(TaskSet):
        @task
        def get_root(self):
            res = self.client.request(**request_body)
            if res.status_code != 200:
                raise("响应码异常！")

    class WebsiteUser(HttpUser):
        host = url
        wait_time = constant(0.5)
        tasks = [UserTasks]
    
    # setup Environment and Runner
    env = Environment(user_classes=[WebsiteUser], events=events)
    runner = env.create_local_runner()
    # start a WebUI instance
    # web_ui = env.create_web_ui(uri_port[0], uri_port[1])
     
    # execute init event handlers (only really needed if you have registered any)
    env.events.init.fire(environment=env, runner=runner)
    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))

    # start a greenlet that save current stats to history
    gevent.spawn(stats_history, env.runner)

    # start the test
    # 攀升率为1, 通过10s完成0-20用户
    # 攀升率为2, 通过5s完成0-20用户
    
    # 预计最大并发数（模拟过程到此RPS时稳定）
    # max_rps = 100
    # 攀升时间(s)，从第一个用户到用户数（最大并发数的一半）需要多少秒
    # spawn_time = 15

    spawn_rate = (max_rps / spawn_time) * 0.5  
    runner.start(max_rps, spawn_rate)

    # in 60 seconds stop the runner
    gevent.spawn_later(time_limit, lambda: runner.quit())

    # wait for the greenlets
    runner.greenlet.join()

    # stop the web server for good measures
    #web_ui.stop()
    #comm = f"locust -f {os.path.abspath(__file__)} --host {url} --web-host={uri_port[0]} --web-port={uri_port[1]}"
    #os.system(comm)
if __name__ == "__main__":
    main()
