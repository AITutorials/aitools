import math
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape


sample = {"content": {
    "match_threshold": 50,
    "use_index": 0,
    "enterprise_list": [
        {
            "id": 5,
            "description": "多孔砖墙",
            "spec": "1)砖品种:页岩烧结多孔砖;2)墙体厚度、砌块规格、砂浆强度等级、配合比:综合考虑,且满足图纸及设计规范要求;"
        },
        {
          "id": 1232,
          "description": "多孔砖墙",
          "spec": "综合考虑,且满足图纸及设计规范要求;"
}
    ],
    "user_list": [
        {
            "uid": 5,
            "description": "多孔砖墙",
            "spec": "1)砖品种:页岩烧结多孔砖;2)墙体厚度、砌块规格、砂浆强度等级、配合比:综合考虑,且满足图纸及设计规范要求;"
        },
        {
           "uid": 1232,
           "description": "多孔砖墙",
           "spec": "综合考虑,且满足图纸及设计规范要求;"
        }
    ]} 
}
url = "http://8.142.6.226/lp/text_compare/"


#  method=None, url=None, headers=None, files=None, data=None,
#  params=None, auth=None, cookies=None, hooks=None, json=None
request_body = {"json": sample, "url": url}

# 请求时间间隔
step_time = 30
# 每次增加的用户数
step_load = 1
# 起始用户数
spawn_rate = 1
# 总体时间
time_limit = 300

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

