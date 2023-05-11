# -*- coding:utf-8 -*-
"""
效果： line_lsd > line_fld > line_hough_p
"""
import cv2
import imghdr
import numpy as np
from pathlib import Path


def line_lsd(img: Path, line_length_limit=20, show=False):
    """
    直线检测效果好，直线合并效果好
    :param img:
    :param line_length_limit: 直线长度阈值
    :param show:
    :return:
    """
    horizontal_lines = []  # 水平线集合
    vertical_lines = []  # 垂直线集合
    img_ori = cv2.imread(str(img))
    img = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    # 加入二值化
    #img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
    #        cv2.THRESH_BINARY,11,2)
    # _, img = cv2.threshold(0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    h, w = img.shape
    line_length_limit = int(max(h / 1000, 1)) * line_length_limit
    # print("hw",h,w,line_length_limit)
    # 创建检测器
    detector = cv2.createLineSegmentDetector()
    try:
        # 检测
        lines = detector.detect(img)
        # 绘制检测结果
        for line in lines[0]:
            x0 = int(round(line[0][0]))
            y0 = int(round(line[0][1]))
            x1 = int(round(line[0][2]))
            y1 = int(round(line[0][3]))
            # 直线长度阈值控制
            if ( x0 > w * 0.95 or x0 < w * 0.1):
                continue
            if (y0 >= h * 0.95 or y0 <= h * 0.1):
                continue
            # if abs(x0 - x1) > abs(y0 - y1):
            #     print(x0, y0, x1, y1, "横线", line_length_limit, (abs(x0 - x1)))
            # else:
            #     print(x0, y0, x1, y1, "竖线", line_length_limit, (abs(y0 - y1)))
            if abs(x0 - x1) < line_length_limit and abs(y0 - y1) < line_length_limit:
                continue
            # ???
            if abs(x0 - x1) > 1100 or abs(y0 - y1) > 1100:
                continue
            if abs(x0 - x1) > abs(y0 - y1):
                horizontal_lines.append([(x0, y0), (x1, y1)])
            else:
                vertical_lines.append([(x0, y0), (x1, y1)])
            # print((x0, y0), (x1, y1))
            if show:
                cv2.line(img_ori, (x0, y0), (x1, y1), (0, 255, 0), 1, cv2.LINE_AA)  # 绿色线

    except Exception as e:
        print(e)
    if show:
        cv2.imwrite('sam0.png', img_ori)
        #cv2.imshow("LineSegmentDetector", img_ori)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    return horizontal_lines, vertical_lines


def line_fld(img: Path, line_length_limit=50, show=False):
    """
    pip uninstall opencv-contrib-python opencv-python 先卸载防止多个库之间冲突
    pip install opencv-contrib-python
    直线检测效果好，直线合并效果不太好
    """
    horizontal_lines = []  # 水平线集合
    vertical_lines = []  # 垂直线集合
    img_ori = cv2.imread(str(img))
    img = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    # 创建检测器
    detector = cv2.ximgproc.createFastLineDetector()
    try:
        # 检测
        lines = detector.detect(img)
        # 绘制检测结果
        color = 100
        for line in lines:
            x0 = int(round(line[0][0]))
            y0 = int(round(line[0][1]))
            x1 = int(round(line[0][2]))
            y1 = int(round(line[0][3]))
            color = color + 30
            if color > 225:
                color = 10
            # 直线长度阈值控制
            if abs(x0 - x1) < line_length_limit and abs(y0 - y1) < line_length_limit:
                continue
            if abs(x0 - x1) > abs(y0 - y1):
                horizontal_lines.append([(x0, y0), (x1, y1)])
            else:
                vertical_lines.append([(x0, y0), (x1, y1)])
            if show:
                cv2.line(img_ori, (x0, y0), (x1, y1), (255, 255, 255), 1, cv2.LINE_AA)  # 绿色线
                # cv2.line(img0, (x0, y0), (x1,y1), (color, color, color), 1, cv2.LINE_AA)  # 灰色渐变线
            print(x0, y0, x1, y1)
    except Exception as e:
        print(e)
    if show:
        # cv2.imwrite('res.jpg', img0)
        cv2.imshow("FastLineDetector", img_ori)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return horizontal_lines, vertical_lines


def line_hough_p(img: Path, line_length_limit=50, show=False):
    """
    Hough_line算法的改进版
    :return:
    """
    horizontal_lines = []  # 水平线集合
    vertical_lines = []  # 垂直线集合
    img_ori = cv2.imread(str(img))
    img = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, 50, 200, apertureSize=3)
    try:
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 80, 30, 10)
        for line in lines:
            x0 = int(round(line[0][0]))
            y0 = int(round(line[0][1]))
            x1 = int(round(line[0][2]))
            y1 = int(round(line[0][3]))
            # 直线长度阈值控制
            if abs(x0 - x1) < line_length_limit and abs(y0 - y1) < line_length_limit:
                continue
            if abs(x0 - x1) > abs(y0 - y1):
                horizontal_lines.append([(x0, y0), (x1, y1)])
            else:
                vertical_lines.append([(x0, y0), (x1, y1)])
            if show:
                cv2.line(img_ori, (x0, y0), (x1, y1), (0, 255, 0), 1, cv2.LINE_AA)
    except Exception as e:
        print(e)
    if show:
        cv2.imshow("HoughLinesP", img_ori)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return horizontal_lines, vertical_lines


def is_table(img: Path, table_line_count_limit=(20, 20), line_length_limit=20, show=False):
    """
    是否表格图片
    :param img: 图片
    :param table_line_count_limit: 表格图片线条数据阈值，当水平和垂直都超过则是表格图片, (水平阈值, 垂直阈值)
    :param line_length_limit: 线条长度限制阈值
    :param show: 是否显示线条检测图
    :return: True 表格图片 | False 文档图片
    """
    if not imghdr.what(img):
        return False
    horizontal_lines, vertical_lines = line_lsd(img, line_length_limit=line_length_limit, show=show)
    total_lines_count = len(horizontal_lines) + len(vertical_lines)
    predict_type = len(horizontal_lines) >= table_line_count_limit[0] and len(vertical_lines) >= table_line_count_limit[
        1]
    print("水平线共{0}条，垂直线共{1}条，总共{2}条".format(len(horizontal_lines), len(vertical_lines), total_lines_count))
    print("predict_type->", predict_type, img.parent, img.name)
    return predict_type


def test_acc(src_dir: Path, table_line_count_limit=(20, 20), line_length_limit=50):
    acc_count = 0
    total_count = 0
    for file in src_dir.rglob("*.*"):
        gt_type = file.parent.name
        predict_type = is_table(file, table_line_count_limit=table_line_count_limit,
                                line_length_limit=line_length_limit)
        predict_type = "表格" if predict_type else "文档"
        if gt_type == predict_type:
            acc_count += 1
        print(file, gt_type, predict_type)
        total_count += 1
    print("acc: ", acc_count / total_count)


if __name__ == "__main__":
    img_=Path("/data/tu/第137页-126.PNG")
    # line_fld(img_, show=True)
    # line_hough_p(img_, show=True)
    a, b = line_lsd(img_, show=True)
    print(f"检测到的横线数量:{len(a)}")
    print(f"检测到的竖线数量:{len(b)}") 
    from pyaitools.theT import find_the_minimum_closed_interval
    _, res = find_the_minimum_closed_interval(a, b, offset=0, extend_increment=10)
    print(f"规范化后形成的最小矩形数量:{len(res)}")
    picture = cv2.imread(str(img_))      # picture_path为图片路径;(cv读取的文件为BGR形式)
    for jx in res:
        cv2.rectangle(picture, jx[1], jx[3], (255, 0, 255), 2)
    cv2.imwrite("sam.png", picture)
    #print(res)
    # print(is_table(img_, table_line_count_limit=(10, 5), line_length_limit=30, show=True))
    # test_acc(Path("/Users/zhousf/Desktop/表格文档分类"), table_line_count_limit=(5, 5), line_length_limit=50)
