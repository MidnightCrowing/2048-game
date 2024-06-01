from tkinter import Tk, Canvas
from threading import Thread
from random import randint
from time import sleep

# row:行, column:列
"""   外观定义类   """
def fg_colors(item: int) -> str:
    # 字体颜色
    match item:
        case 2 | 4 | 8:
            return 'Gray'
        case _:
            return 'White'
def bg_colors(item: str | int) -> str:
    # 背景颜色
    match item:
        case '默认背景颜色':
            return 'DarkGray'
        case 2 | 4:
            return 'WhiteSmoke'
        case 8:
            return 'NavajoWhite'
        case 16:
            return 'SandyBrown'
        case 32:
            return 'Coral'
        case 64:
            return 'OrangeRed'
        case 128:
            return 'Red'
        case 256 | 512 | 1024 | 2048:
            return 'Gold'
        case _:
            return 'Black'
def font(item: int) -> tuple:
    # 字体设置
    match item:
        case 2 | 4 | 8:
            return '黑体', 40, 'bold'
        case _:
            if item > 524288:
                size = 10
            else:
                size = 40 - len(str(item)) * 5
            return '黑体', size, 'bold'

# 创建组件
def create_grid(coordinate: tuple = None, number: int = None) -> None:
    global null_data
    if number is None:
        text = randint(0, 1)
        if text:  # text=1, True
            text = 2
        else:  # text=0, False
            text = 4
    else:
        text = number
    if coordinate is None:
        number = randint(0, len(null_data) - 1)
        x, y = null_data.pop(number)
    else:
        null_data.remove(coordinate)
        x, y = coordinate

    width = height = 72  # 方格大小
    can = Canvas(width=width, height=height, bg=bg_colors(item=text))
    can.create_text((width / 2, height / 2), text=f'{text}', font=font(item=text), fill=fg_colors(item=text))
    can.place(x=(2 * x - 1) * 40, y=(2 * y - 1) * 40, anchor='center')

    global grid_data
    grid_data[(x, y)] = {'can': can, 'text': text}

"""   事件处理类   """
def exchange(item: list) -> list:
    for i in range(len(item)):
        item[i] = (item[i][1], item[i][0])
    return item

def animation(can: Canvas, t_x: float, t_y: float, x_: int, y_: int, x__: int, y__: int) -> None:
    for i in range(10):
        i += 1
        x = x_ + t_x * i
        y = y_ + t_y * i
        can.place(x=x, y=y)
        sleep(0.01)
    can.place(x=x__, y=y__)
    can.destroy()

    
class KeyPress:
    """   处理步骤库   """

    # 初始化变量
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        self.data_dict = {}

    # 读取数据
    def step1(self) -> list:
        data_list = []
        for i in grid_data:
            self.data_dict[i] = [False, grid_data[i]['text']]
            data_list.append(i)

        return data_list

    # 对变量进行排序
    def step2(self, data_list: list) -> list:
        match self.x, self.y:
            case (self.x, -1):  # 上
                data_list.sort(reverse=False)  # 对列表进行排序, 小->大
            case (self.x, 1):  # 下
                data_list.sort(reverse=True)  # 对列表进行排序, 大->小
            case (-1, self.y):  # 左
                data_list = exchange(item=data_list)  # 交换x,y
                data_list.sort(reverse=False)  # 对列表进行排序, 小->大
                data_list = exchange(item=data_list)
            case (1, self.y):  # 右
                data_list = exchange(item=data_list)
                data_list.sort(reverse=True)  # 对列表进行排序, 大->小
                data_list = exchange(item=data_list)

        return data_list

    # 计算理论移动位置
    def step3(self, data_list: list) -> list:
        data_list_ = []
        while data_list:
            item = data_list.pop(0)
            item_x, item_y = item
            for i in range(4):
                item__x, item__y = item_x + self.x * (i + 1), item_y + self.y * (i + 1)
                try:
                    text__ = self.data_dict[(item__x, item__y)][1]
                except KeyError:
                    if item__x == 0:
                        self.data_dict[item].append((1, item__y))
                        data_list_.append([(item_x, item_y), (1, item__y)])
                        # print(f'    ({item_x}, {item_y}) -> (1, {item__y})')
                        break
                    elif item__x == 5:
                        self.data_dict[item].append((4, item__y))
                        data_list_.append([(item_x, item_y), (4, item__y)])
                        # print(f'    ({item_x}, {item_y}) -> (4, {item__y})')
                        break
                    elif item__y == 0:
                        self.data_dict[item].append((item__x, 1))
                        data_list_.append([(item_x, item_y), (item__x, 1)])
                        # print(f'    ({item_x}, {item_y}) -> ({item__x}, 1)')
                        break
                    elif item__y == 5:
                        self.data_dict[item].append((item__x, 4))
                        data_list_.append([(item_x, item_y), (item__x, 4)])
                        # print(f'    ({item_x}, {item_y}) -> ({item__x}, 4)')
                        break
                    else:
                        continue
                else:
                    text_ = self.data_dict[item][1]
                    if text_ == text__ and not self.data_dict[(item__x, item__y)][0]:
                        self.data_dict[item][0] = True
                        self.data_dict[(item__x, item__y)][0] = True
                        item__x, item__y = self.data_dict[(item__x, item__y)][2]
                        self.data_dict[item].append((item__x, item__y))
                        data_list_.append([(item_x, item_y), (item__x, item__y)])
                        # print(f'    ({item_x}, {item_y}) -> ({item__x}, {item__y})')
                        break
                    else:
                        item__x, item__y = item__x - self.x, item__y - self.y
                        self.data_dict[item].append((item__x, item__y))
                        data_list_.append([(item_x, item_y), (item__x, item__y)])
                        # print(f'    ({item_x}, {item_y}) -> ({item__x}, {item__y})')
                        break

        return data_list_

    # 判断操作是否有效
    @staticmethod
    def step4(data_list: list) -> bool:
        for i1, i2 in data_list:
            if i1 != i2:
                return True
        return False

    # 输出实际移动位置
    def step5(self, data_list: list) -> dict:
        dict_, dict__ = {}, {}
        for i in data_list:
            dict_[i[1]] = []
        for i in data_list:
            dict_[i[1]].append(i[0])
        if self.y == -1:  # 上
            for c in range(4):
                c += 1
                cs = {}
                for i in dict_:
                    if i[0] == c:
                        cs[i[1]] = i
                    elif i[0] > c:
                        break
                result = list(cs.keys())
                result.sort(reverse=False)
                for i in result:
                    dict__[(c, result.index(i) + 1)] = dict_[cs[i]]
        elif self.y == 1:  # 下
            for c in range(4):
                c += 1
                cs = {}
                for i in dict_:
                    if i[0] == c:
                        cs[i[1]] = i
                    elif i[0] < c:
                        break
                result = list(cs.keys())
                result.sort(reverse=True)
                for i in result:
                    dict__[(c, 4 - result.index(i))] = dict_[cs[i]]
        elif self.x == -1:  # 左
            for r in range(4):
                r += 1
                rs = {}
                for i in dict_:
                    if i[1] == r:
                        rs[i[0]] = i
                    elif i[1] > r:
                        break
                result = list(rs.keys())
                result.sort(reverse=False)
                for i in result:
                    dict__[(result.index(i) + 1), r] = dict_[rs[i]]
        else:  # 右
            for r in range(4):
                r += 1
                rs = {}
                for i in dict_:
                    if i[1] == r:
                        rs[i[0]] = i
                    elif i[1] < r:
                        break
                result = list(rs.keys())
                result.sort(reverse=True)
                for i in result:
                    dict__[(4 - result.index(i)), r] = dict_[rs[i]]
        return dict__

    # 创建线程执行动画
    @staticmethod
    def step6(data_list: dict) -> None:
        data_list_ = data_list
        for i1 in data_list_:
            for i2 in data_list_[i1]:
                can = grid_data[i2]['can']
                x_, y_ = (2 * i2[0] - 1) * 40, (2 * i2[1] - 1) * 40
                x__, y__ = (2 * i1[0] - 1) * 40, (2 * i1[1] - 1) * 40
                d_x, d_y = x__ - x_, y__ - y_
                t_x, t_y = d_x / 10, d_y / 10
                Thread(target=animation, args=(can, t_x, t_y, x_, y_, x__, y__)).start()

    # 计算移动后的结果
    @staticmethod
    def step7(data_list: dict) -> dict:
        data_list_ = {}
        for i in data_list:
            text = 0
            for item in data_list[i]:
                text = text + grid_data[item]['text']
            data_list_[i] = text
            if text == 2048:
                game_over(is_=True)

        return data_list_

    # 覆盖数据
    @staticmethod
    def step8(data_list: dict) -> None:
        global grid_data, null_data
        grid_data.clear()
        null_data = [(1, 1), (1, 2), (1, 3), (1, 4),
                     (2, 1), (2, 2), (2, 3), (2, 4),
                     (3, 1), (3, 2), (3, 3), (3, 4),
                     (4, 1), (4, 2), (4, 3), (4, 4)]
        for i in data_list:
            create_grid(coordinate=i, number=data_list[i])
def keypress(x: int = 0, y: int = 0) -> None:
    if game or game is None:
        step = KeyPress(x=x, y=y)  # 初始化变量
        data_list = step.step1()  # 读取数据
        data_list = step.step2(data_list=data_list)  # 对变量进行排序
        data_list = step.step3(data_list=data_list)  # 计算理论移动位置
        if step.step4(data_list=data_list):  # 判断操作是否有效
            data_list = step.step5(data_list=data_list)  # 输出实际移动位置
            step.step6(data_list=data_list)  # 创建线程执行动画
            data_list = step.step7(data_list=data_list)  # 计算移动后的结果
            step.step8(data_list=data_list)  # 覆盖数据

            create_grid()
        elif not null_data:
            game_over(is_=False)

# 游戏结束触发
def game_over(is_: bool) -> None:
    global game
    if is_:
        game = None
        root.title('恭喜！')
    else:
        text = 4
        for i in grid_data:
            text_ = grid_data[i]['text']
            if text_ > text:
                text = text_
        if game is None:
            root.title(f'恭喜！  —最高：{text}')
        else:
            game = False
            root.title(f'Game Over  —最高：{text}')

"""   参数定义类   """
game = True
grid_data = {}  # 组件数据
null_data = [(1, 1), (1, 2), (1, 3), (1, 4),
             (2, 1), (2, 2), (2, 3), (2, 4),
             (3, 1), (3, 2), (3, 3), (3, 4),
             (4, 1), (4, 2), (4, 3), (4, 4)]  # 空格子

if __name__ == '__main__':
    """   窗口类   """
    root = Tk()
    root.geometry('320x320')
    root.title('2048')
    root.resizable(height=False, width=False)  # 固定窗口宽度

    """   组件类   """
    Canvas(root, bg=bg_colors(item='默认背景颜色'), width=320, height=320).pack()

    """   按键绑定   """
    root.bind_all('<KeyPress-Up>', lambda event: keypress(y=-1))  # 上
    root.bind_all('<KeyPress-Down>', lambda event: keypress(y=1))  # 下
    root.bind_all('<KeyPress-Left>', lambda event: keypress(x=-1))  # 左
    root.bind_all('<KeyPress-Right>', lambda event: keypress(x=1))  # 右

    # 创建组件
    create_grid()

    # 循环
    root.mainloop()
