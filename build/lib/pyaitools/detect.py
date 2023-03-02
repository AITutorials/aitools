import pandas as pd

sample_path = "./train.csv"
deconflict_sample_path = "./new_train.csv"


def corpus_conflict_detect(
    sample_path,
    deconflict_sample_path,
    sep = ",",
    label_list=["Y", "N"],
    choiceDeleteLabel="Y",
    csample_path="./conflict_sample.txt"
):


    if not label_list or len(label_list) != 2:
        raise("标签列表中的元素必须存在且只能是两个，我们只支持二分类的语料冲突检测！")
    df = pd.read_csv(sample_path, lineterminator="\n", sep=sep)
    # 形成一个基本检查字典
    check_dict = {label_list[0]: set(), label_list[1]: set()}
    for dfc in df.values:
        sent = ""
        label = dfc[-1]
        for i in range(len(dfc) - 1):
            sent += str(dfc[i]) + sep
        if label == label_list[0]:
            check_dict[label_list[0]].add(sent)
        else:
            check_dict[label_list[1]].add(sent)
    print(f"去重后{label_list[0]}标签数量: {len(check_dict[label_list[0]])}")
    print(f"去重后{label_list[1]}标签数量: {len(check_dict[label_list[1]])}")
    csample = check_dict[label_list[0]] & check_dict[label_list[1]]
    print(f"去重后冲突样本数量:{len(csample)}")
    fp = open(csample_path, "w")
    for csa in csample:
        fp.write(csa + "\n")
    fp.close()
    print(f"冲突样本已写入路径:{csample_path}")
    # 利用检查字典对N集合进行冲突检测
    if label_list[0] == choiceDeleteLabel:
        check_dict[label_list[0]] = (
            check_dict[label_list[0]] - check_dict[label_list[1]]
        )
    else:
        check_dict[label_list[1]] = (
            check_dict[label_list[1]] - check_dict[label_list[0]]
        )
    print(f"去冲突+去重复后{label_list[0]}标签数量: {len(check_dict[label_list[0]])}")
    print(f"去冲突+去重复后{label_list[1]}标签数量: {len(check_dict[label_list[1]])}")
    fp = open(deconflict_sample_path, "w")
    for cn in list(df.columns)[:-1]:
        fp.write(cn + sep)
    else:
        fp.write(list(df.columns)[-1] + "\n")
    for k, v in check_dict.items():
        for vv in v:
            fp.write(vv + k + "\n")
    fp.close()
    return


if __name__ == "__main__":
    corpus_conflict_detect(sample_path, deconflict_sample_path)

