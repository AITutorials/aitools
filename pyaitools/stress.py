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
from . import utils

setup_logging("INFO", None)


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--config", "-c", required=True, help="压测服务的配置文件名")
    parser.add_argument(
        "--dynamic", "-d", required=False, action="store_true", help="存在该参数使用动态请求体"
    )
    args = parser.parse_args()
    config = args.config
    dynamic = args.dynamic
    path = os.getcwd()
    stress_config = utils.get_config_from_filename(path, config)
    max_user = stress_config["max_user"]
    spawn_time = stress_config["spawn_time"]
    time_limit = stress_config["time_limit"]
    url = stress_config["url"]

    
    class UserTasks(TaskSet):
        @task
        def get_root(self):
            if dynamic:
                rb = stress_config["RequestBody"]().dynamic()
            else:
                rb = stress_config["request_body"]
            res = self.client.request(**rb)
            if res.status_code != 200:
                raise ("响应码异常！")

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
    # web_ui.stop()


if __name__ == "__main__":
    main()
