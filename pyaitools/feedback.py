import os
import copy
import pandas as pd
import numpy as np


def _is_error_modify(matchedcontent, matchcontent):
    """判断用户修改是否为误修改
    目前，可以确定的误修改即修改内容和推荐内容相同时"""
    # 默认不是误修改
    error_modify_mark = 0
    if matchedcontent == matchcontent:
        # print(matchedcontent)
        # print(matchcontent)
        error_modify_mark = 1
    return error_modify_mark


def _get_content_columns(df, content_columns, i):
    """获取指定列的内容"""
    res = ""
    for cc in content_columns:
        try:
            rc = str(df.iloc[i][cc])
        except:
            rc = recommend_content_substitute
        if res:
            res = res + content_interval_mark + rc
        else:
            res = rc
    return res


def _calc(p_dict):
    """定义工程聚合后的计算方式"""
    p_dict = copy.deepcopy(p_dict)
    for key, value in p_dict.items():
        p_dict[key][0] = len(p_dict[key][0])
        p_dict[key][1] = p_dict[key][1].count(1)
        p_dict[key][2] = max(p_dict[key][2])
    return p_dict


def get_modification_rate_and_content(
    ori_path,
    buried_point_number_list,
    projectID,
    xlbqnumber,
    origin_content_columns,
    recommend_content_columns,
    modify_content_columns,
    non_empty_column=[],
    content_interval_mark="@",
    recommend_content_substitute="error",
):
    file_path_list = []
    all_pid_dict = dict()
    for dfile in os.listdir(ori_path):
        if dfile == ".DS_Store":
            continue
        ffile_path = os.path.join(ori_path, dfile)
        for ffile in os.listdir(ffile_path):
            if "csv" not in ffile:
                continue
            mark = 0
            for bpn in buried_point_number_list:
                if bpn in ffile:
                    mark = 1
                    break
            if not mark:
                continue
            # 对该功能的埋点文件进行解析
            csv_path = os.path.join(ffile_path, ffile)
            # 过滤空文件
            sc = os.stat(csv_path)
            if not sc.st_size:
                continue
            # 记录正在解析的文件路径
            file_path_list.append(csv_path)
            # 输出工程id和原始清单项为空的行，这样的行内容一定是有问题的
            df = pd.read_csv(csv_path).dropna(subset=non_empty_column)
            # 形成以工程id为key的字典, 这个字典的value是一个列表，列表的
            # 第一项为：本次修改计数列表[1,1,1,1...1]
            # 第二项为：本次修改是否为误修改的列表，[1,0,0,0,1]
            # 第三项为：本次修改时的清单数列表
            # 第四项为：本次修改时清单的内容，包括[原始清单，推荐清单，修改后清单]
            p_dict = dict()
            for i, pid in enumerate(df[projectID].values):
                # 记录清单内容
                curcontent = _get_content_columns(df, origin_content_columns, i)
                matchedcontent = _get_content_columns(df, recommend_content_columns, i)
                matchcontent = _get_content_columns(df, modify_content_columns, i)

                if pid not in p_dict:
                    p_dict[pid] = []
                    p_dict[pid].append([1])
                    # 判断是否为误修改
                    if _is_error_modify(matchedcontent, matchcontent):
                        p_dict[pid].append([1])
                    else:
                        p_dict[pid].append([0])
                    # 记录当前清单数
                    p_dict[pid].append([df.iloc[0][xlbqnumber]])
                    p_dict[pid].append([[curcontent, matchedcontent, matchcontent]])
                else:
                    p_dict[pid][0].append(1)
                    if _is_error_modify(matchedcontent, matchcontent):
                        p_dict[pid][1].append(1)
                    else:
                        p_dict[pid][1].append(0)
                    p_dict[pid][2].append(df.iloc[i][xlbqnumber])
                    p_dict[pid][3].append([curcontent, matchedcontent, matchcontent])
            # 对工程id字典进行计算
            all_pid_dict.update(_calc(p_dict))

    total_number, error_number, max_num, modify_content = np.sum(
        list(all_pid_dict.values()), axis=0, keepdims=False
    )
    modification_rate = round((total_number - error_number) / max_num, 4)
    # print(file_path_list)
    # print(f"触发文件数: {len(file_path_list)}")

    return (
        modify_content,
        modification_rate,
        len(all_pid_dict),
        total_number,
        error_number,
        int(max_num),
    )


if __name__ == "__main__":
    # 埋点数据文件夹
    ori_path = "./feedback"
    buried_point_number_list = ["1104127", "1104128"]
    # buried_point_number_list = ["1110061", "1110062"]
    # 理论上存在一些不可以为空的列，一旦他们的值为空，说明数据存在一定的问题
    # 为了避免影响计算，在这里可以删除其为空的所在行内容
    non_empty_column = ["projectid", "curdescription"]
    # 埋点表中每一行代表一次修改，需要将这些修改聚合到各自的工程上，所以每条数据需要工程id进行辨识
    projectID = "projectid"
    # 修改率的分母列（清单数）
    xlbqnumber = "xlbqnumber"
    # 内容间隔标志
    content_interval_mark = "@"
    # 原始内容相关的列
    origin_content_columns = ["curdescription", "curspec"]
    # 推荐内容相关的列
    recommend_content_columns = ["matcheddescription", "matchedspec"]
    # 修改内容相关的列
    modify_content_columns = ["matchdescription", "matchspec"]

    # 因为推荐内容不一定存在，埋点中可能缺失对应的列，需要指定内容标识
    recommend_content_substitute = "error"
    (
        modify_content,
        modification_rate,
        pid_num,
        total_number,
        error_number,
        max_num,
    ) = get_modification_rate_and_content(
        ori_path,
        buried_point_number_list,
        projectID,
        xlbqnumber,
        origin_content_columns,
        recommend_content_columns,
        modify_content_columns,
        non_empty_column,
        content_interval_mark,
        recommend_content_substitute,
    )
    print(f"修改内容:{modify_content}")
    print(f"修改率:{modification_rate}")
    print(f"触发工程数: {pid_num}")
    print(f"总修改数:{total_number}")
    print(f"误修改数:{error_number}")
    print(f"最大分母数:{max_num}")

