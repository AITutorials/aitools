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
        print("请求uri出错！!")
        os.popen(comm)
        return 
    if resu:
        if resu.status_code == requests.codes.ok:
            if not res:
                print("服务正常运行...")
            else:
                if resu.text == str(res):
                    print("服务正常运行...")
                else:
                    print("服务正常响应，但返回内容不相符！")
                    os.popen(comm)
        else:
            print("服务接口没有正常响应！")
            os.popen(comm)


def run():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--uri", "-u", required=True, help="侦测的服务接口请求地址（如：http://0.0.0.0:8008）!")
    parser.add_argument("--comm", "-c", required=True, help="侦测失败后服务重启的shell命令!")
    parser.add_argument("--sec", "-s", default=5, help="侦测的时间间隔, 单位为秒, 默认为5s!")
    parser.add_argument(
        "--timeout", "-t", default=10, help="侦测的服务接口超时时间, 单位为秒, 默认为10s!"
    )
    parser.add_argument("--res", "-r", default=None, help="侦测的服务接口输出结果（字符串）,如果存在此参数，说明要求接口即需要满足正常响应同时结果也要对得上, 默认为None!")
    args = parser.parse_args()
    uri = args.uri
    res = args.res
    comm = args.comm
    sec = args.sec
    timeout = args.timeout
    scheduler = BlockingScheduler()
    scheduler.add_job(job, "interval", seconds=5, args=[uri, res, comm, sec, timeout])
    scheduler.start()


if __name__ == "__main__":
    run()
