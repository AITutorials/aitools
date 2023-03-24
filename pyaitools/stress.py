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
    parser.add_argument("--config", "-c", required=True, help="压测服务的配置文件名")
    parser.add_argument("--dynamic", "-d", required=False, action="store_true", help="存在该参数使用动态请求体")
    args = parser.parse_args()
    config = args.config
    dynamic = args.dynamic
    path = os.getcwd()
    import sys
    sys.path.append(path)

    from stress_config import max_user, spawn_time, time_limit
   
    if dynamic:
        print("正在使用动态请求体...")
        from stress_config import RequestBody 
        url = RequestBody().url
    else:
        from stress_config import request_body
        url = request_body.get("url")
        rb = request_body



    class UserTasks(TaskSet):
        @task
        def get_root(self):
            if dynamic:
                 rb = RequestBody().dynamic()
            res = self.client.request(**rb)
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
    spawn_rate = (max_user / spawn_time) * 0.5  
    runner.start(max_user, spawn_rate)

    # in 60 seconds stop the runner
    gevent.spawn_later(time_limit, lambda: runner.quit())

    # wait for the greenlets
    runner.greenlet.join()

    # stop the web server for good measures
    #web_ui.stop()
if __name__ == "__main__":
    main()
