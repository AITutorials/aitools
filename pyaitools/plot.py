# 制图代码
# 导入matplotlib
import matplotlib.pyplot as plt


def multiline_plot(
    x_axis_data,
    y_axis_data,
    x_axis_name,
    y_axis_name,
    x_axis_rotation,
    y_axis_rotation,
    line_width,
    line_color,
    line_name,
    line_alpha,
    legend_loc,
    save_path,
    is_grid=True,
    show_Y=True,
    show_X=False,
):

    # 初始化画布和轴
    fig, ax = plt.subplots()

    if not y_axis_data or not x_axis_data:
        raise ("X,Y轴数据是必须要写的！")
    else:
        x_axis_str_data = []
        x_axis_num_data = []
        y_axis_str_data = []
        y_axis_num_data = []
        # 判断输入数据类型
        if isinstance(x_axis_data[0], str):
            x_axis_str_data = x_axis_data
        else:
            x_axis_num_data = x_axis_data

        if isinstance(y_axis_data[0][0], str):
            y_axis_str_data = y_axis_data
        else:
            y_axis_num_data = y_axis_data

    if x_axis_str_data:
        leng = len(x_axis_str_data)
        x_p = list(range(0, leng))
    else:
        x_p = x_axis_num_data

    if y_axis_str_data:
        leng = len(y_axis_str_data[0])
        y_p = [list(range(0, leng))] * len(y_axis_str_data)
    else:
        y_p = y_axis_num_data

    for i in range(0, len(y_p)):
        ax.plot(
            x_p,
            y_p[i],
            linewidth=line_width[i],
            label=line_name[i],
            color=line_color[i],
            alpha=line_alpha[i],
        )
        # 添加折线点纵坐标，但不显示0
        for x, y in zip(x_p, y_axis_num_data[i]):
            if y != 0:
                if show_Y:
                    ax.text(x, y, (y), color=line_color[i])
                elif show_X:
                    ax.text(x, y, (x), color=line_color[i])
                else:
                    ax.text(x, y, "", color=line_color[i])

    ax.legend(loc=legend_loc)
    # 设置y坐标名称
    ax.set_ylabel(y_axis_name)
    # 设置x坐标名称
    ax.set_xlabel(x_axis_name)

    if x_axis_str_data:
        leng = len(x_axis_str_data)
        # 设置x轴刻度
        ax.set_xticks(list(range(0, leng)))
        # 设置x刻度名称
        ax.set_xticklabels(x_axis_str_data, rotation=x_axis_rotation)

    if y_axis_str_data:
        leng = len(y_axis_str_data[0])
        # 设置y轴刻度
        ax.set_yticks(list(range(0, leng)))
        # 设置y刻度名称
        ax.set_yticklabels(y_axis_str_data, rotation=y_axis_rotation)

    # 加入表格线
    if is_grid:
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
    # 设置布局
    plt.tight_layout()

    # plt.show()
    print(f"保存图像至路径: {save_path}")
    plt.savefig(save_path)
    plt.close(fig)


if __name__ == "__main__":
    y1 = [
        0.1,
        0.2,
        0.3,
    ]
    y2 = [0.5, 0.6, 0.7]
    y3 = [0.8, 0.9, 1.0]
    x1 = ["50V", "100V", "250V"]

    y_axis_data = [y1, y2, y3]
    x_axis_data = x1
    x_axis_name = ""
    y_axis_name = "Price"
    x_axis_rotation = 30
    y_axis_rotation = 0
    line_width = [2] * 3
    line_color = ["b", "r", "g"]
    line_name = ["50V", "100V", "250V"]
    line_alpha = [0.5] * 3
    legend_loc = "upper left"
    is_grid = True
    show_Y = True
    show_X = False
    save_path = "at_pre.png"
    multiline_plot(
        x_axis_data,
        y_axis_data,
        x_axis_name,
        y_axis_name,
        x_axis_rotation,
        y_axis_rotation,
        line_width,
        line_color,
        line_name,
        line_alpha,
        legend_loc,
        save_path,
    )
