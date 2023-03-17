import os
import requests
from datetime import datetime
import argparse

# pip install apscheduler==3.9.1
from apscheduler.schedulers.blocking import BlockingScheduler


# command = "supervisorctl restart lp_server"
# uri = "http://8.142.6.226:80/v1/test/"


def job(uri, res, comm, sec, timeout):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        resu = requests.get(uri, timeout=timeout)
    except:
        print("服务无响应!")
        os.popen(comm)
        return 
    if resu:
        if resu.text == str(res):
            print("服务正常运行...")
        else:
            print("服务响应，但返回结果与预计不一致！")


def run():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--uri", "-u", help="侦测的服务接口请求地址（如：http://0.0.0.0:8008）!")
    parser.add_argument("--res", "-r", help="侦测的服务接口输出结果（字符串）!")
    parser.add_argument("--comm", "-c", help="侦测失败后服务重启的shell命令!")
    parser.add_argument("--sec", "-s", default=5, help="侦测的时间间隔, 单位为秒, 默认为5s!")
    parser.add_argument(
        "--timeout", "-t", default=10, help="侦测的服务接口超时时间, 单位为秒, 默认为10s!"
    )
    args = parser.parse_args()
    uri = args.uri
    res = args.res
    comm = args.comm
    sec = args.sec
    timeout = args.timeout
    if not uri or not res or not comm:
        print("必要的参数缺失!")
        explain()
        return
    scheduler = BlockingScheduler()
    scheduler.add_job(job, "interval", seconds=5, args=[uri, res, comm, sec, timeout])
    scheduler.start()


def explain():
    print("--uri 侦测的服务接口请求地址")
    print("--res 服务接口返回的结果（字符串）")
    print("--comm 侦测失败后服务重启的shell命令")
    print("--sec 侦测的时间间隔, 单位为秒, 默认为5s")
    print("--timeout 侦测的服务接口超时时间, 单位为秒, 默认为10s")


if __name__ == "__main__":
    run()
