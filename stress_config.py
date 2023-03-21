# 导入测试用例
from sample import sample

# 目标服务的请求地址
url = "http://8.142.6.226/lp/text_compare/"

# 请求体可以包含以下参数：（参考requests）method，url，headers，files，data，params，auth，cookies，hooks，json
request_body = {"method": "POST", "url": url, "json": sample}


## 压力测试的相关配置

# 请求时间间隔
step_time = 30
# 每次增加的用户数
step_load = 1
# 起始用户数
spawn_rate = 1
# 总体时间
time_limit = 300
