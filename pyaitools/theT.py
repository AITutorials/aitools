import copy


def _the_minimum_normalization(
    coordinate_group: list, direction=0, extend_increment=10
):
    """线段最小规范化
    param: direction: 0表示要对横线规范化，1表示要对竖线规范化
    """
    coordinate_group = copy.deepcopy(coordinate_group)
    if direction == 0:
        # [(1031, 258), (141, 270)]
        if coordinate_group[0][1] < coordinate_group[1][1]:
            # coordinate_group[0] = list(coordinate_group[0])
            coordinate_group[1] = [coordinate_group[1][0], coordinate_group[0][1]]
        else:
            # coordinate_group[1] = list(coordinate_group[1])
            coordinate_group[0] = [coordinate_group[0][0], coordinate_group[1][1]]

        coordinate_group.sort(key=lambda x: x[0])
        # 延长增量
        coordinate_group[0] = (
            coordinate_group[0][0] - extend_increment,
            coordinate_group[0][1],
        )
        coordinate_group[1] = (
            coordinate_group[1][0] + extend_increment,
            coordinate_group[1][1],
        )

    else:
        # [(1031, 22), (1035, 270)]
        if coordinate_group[0][0] < coordinate_group[1][0]:
            # coordinate_group[0] = list(coordinate_group[0])
            coordinate_group[1] = [coordinate_group[0][0], coordinate_group[1][1]]
        else:
            # coordinate_group[1] = list(coordinate_group[1])
            coordinate_group[0] = [coordinate_group[1][0], coordinate_group[0][1]]

        coordinate_group.sort(key=lambda x: x[1])
        coordinate_group[0] = (
            coordinate_group[0][0],
            coordinate_group[0][1] - extend_increment,
        )
        coordinate_group[1] = (
            coordinate_group[1][0],
            coordinate_group[1][1] + extend_increment,
        )
    return coordinate_group


def _get_crossover_point(h_coordinate_group, v_coordinate_group):
    """获取水平/垂直线交点"""
    # 判断是否满足交点条件
    # 水平交点定理：竖线段的横坐标（一个数）如果在横线段两点的横坐标区间内，且横线段的纵坐标（一个数）在竖线段的纵坐标
    # 区间内，那么两条线段有交点，且交点的横坐标为竖线的横坐标，纵坐标为横线的纵坐标。
    # if v_coordinate_group[0][0] in [h_coordinate_group[0][0], h_coordinate_group[1][0]]:
    #    print(h_coordinate_group, v_coordinate_group)
    #    print("&&")
    if (
        h_coordinate_group[0][0] <= v_coordinate_group[0][0] <= h_coordinate_group[1][0]
        and v_coordinate_group[0][1]
        <= h_coordinate_group[0][1]
        <= v_coordinate_group[1][1]
    ):
        crossover_point = (v_coordinate_group[0][0], h_coordinate_group[0][1])
        # 还需要记录交点的相关线段，以便之后计算连通性
        h_range = [h_coordinate_group[0][0], h_coordinate_group[1][0]]
        v_range = [v_coordinate_group[0][1], v_coordinate_group[1][1]]
        crossover_point_range = [h_range, v_range]
    else:
        crossover_point = 0
        crossover_point_range = 0
    return crossover_point, crossover_point_range


def _get_one_side(cl, point_list, direction="up"):
    """获得某个坐标点上／下／左／右的其他点"""
    # 获得该点在排序后列表的索引
    cl_index = point_list.index(cl)
    if direction == "up" or direction == "right":
        # 此时up:point_list应该是纵坐标从小到大排序的结果v_crossover_list
        # 此时right: point_list应该是横坐标从小到大的排序结果
        crossover_list = point_list[cl_index + 1 :]

    if direction == "down" or direction == "left":
        crossover_list = point_list[:cl_index]

    return crossover_list


def find_the_minimum_closed_interval(h_l, v_l, extend_increment=10, offset=2):
    """找到最小封闭区间(在水平/垂直线中区间为矩形)"""
    crossover_list = []
    crossover_dict = dict()
    for h in h_l:
        for v in v_l:
            h_ = _the_minimum_normalization(
                h, direction=0, extend_increment=extend_increment
            )
            v_ = _the_minimum_normalization(
                v, direction=1, extend_increment=extend_increment
            )
            point, point_range = _get_crossover_point(h_, v_)
            if point and point_range:
                crossover_list.append(point)
                crossover_dict[point] = point_range

    crossover_list = list(set(crossover_list))
    # print("***")
    # print(f"去重复后的交点数量:{len(crossover_list)}")
    # print("***")
    # print(crossover_dict)
    # 对交点进行排序，之后按照向上-->向右-->向下-->向左的方式来判断矩形
    h_crossover_list = sorted(crossover_list, key=lambda x: x[0])
    v_crossover_list = sorted(crossover_list, key=lambda x: x[1])

    res = []
    for cl in crossover_list:
        cl_h = cl[0]
        cl_v = cl[1]
        # 向上找
        for upc in _get_one_side(cl, v_crossover_list, "up"):
            upc_h = upc[0]
            upc_v = upc[1]
            # 横坐标一致，说明在一条竖线上
            if abs(cl_h - upc_h) <= offset:
                # 判断连通性
                # 连通性定理：对于上下两点的连通性，下点所在竖线的上端点纵坐标(大值) >= 上点所在竖线的下端点纵坐标（小值）
                cl_sx_u = crossover_dict[cl][1][1]
                upc_sx_d = crossover_dict[upc][1][0]
                if cl_sx_u >= upc_sx_d:
                    # 向右找
                    for rightc in _get_one_side(upc, h_crossover_list, "right"):
                        rightc_h = rightc[0]
                        rightc_v = rightc[1]
                        # 纵坐标一致，说明在一条线上
                        if abs(upc_v - rightc_v) <= offset:
                            # 对于左右两点的连通性，左点所在横线的（右端点横坐标）大值 >=
                            # 右点所在横线的（左端点横坐标）（小值）
                            upc_hx_u = crossover_dict[upc][0][1]
                            rightc_hx_d = crossover_dict[rightc][0][0]
                            if upc_hx_u >= rightc_hx_d:
                                # 当向右找到第三个点时，如果存在第四个点，那么它的相关属性是确定的，它的纵坐标是起始点的纵坐标，横坐标是找到的右点的横坐标
                                # 如果存在这样的点，进而判断它与起始点和右点的连通性即可确认矩形
                                for downc in _get_one_side(
                                    rightc, v_crossover_list, "down"
                                ):
                                    downc_h = downc[0]
                                    downc_v = downc[1]
                                    if (
                                        abs(downc_h - rightc_h) <= offset
                                        and abs(downc_v - cl_v) <= offset
                                    ):
                                        # 分别判断连通性
                                        downc_sx_u = crossover_dict[downc][1][1]
                                        downc_hx_d = crossover_dict[downc][0][0]
                                        rightc_sx_d = crossover_dict[rightc][1][0]
                                        cl_hx_u = crossover_dict[cl][0][1]
                                        if (
                                            cl_hx_u >= downc_hx_d
                                            and downc_sx_u >= rightc_sx_d
                                        ):
                                            # 此时封闭矩形成立
                                            res.append([cl, upc, rightc, downc])

    return crossover_dict, res


if __name__ == "__main__":

    h_l = [
        [(164, 1129), (381, 1126)],
        [(387, 1177), (527, 1174)],
        [(157, 606), (363, 603)],
        [(386, 1076), (526, 1074)],
        [(526, 1077), (386, 1079)],
        [(379, 652), (519, 650)],
        [(1016, 1455), (1121, 1465)],
        [(1022, 1339), (1142, 1350)],
        [(1134, 1356), (1022, 1346)],
    ]

    v_l = [
        [(522, 732), (521, 653)],
        [(156, 659), (157, 737)],
        [(377, 656), (379, 733)],
        [(376, 733), (375, 656)],
        [(1011, 1438), (1020, 1339)],
        [(1026, 1348), (1018, 1438)],
        [(1125, 1466), (1136, 1358)],
        [(1143, 1352), (1131, 1472)],
    ]

    _, res = find_the_minimum_closed_interval(h_l, v_l)
    print(len(res))

    # path为图片路径;(cv读取的文件为BGR形式)
    # picture = cv2.imread(str(path))
    # for jx in res:
    #    cv2.rectangle(picture, jx[1], jx[3], (255, 0, 255), 2)
    # cv2.imwrite("new.png", picture)
