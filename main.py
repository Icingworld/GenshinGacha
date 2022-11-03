import random
import json


class Genshin:
    def __init__(self):
        # up池信息
        self.wu_xing_character_up = []
        self.si_xing_character_up = []
        self.wu_xing_character_rate = 0.006
        self.wu_xing_character_rate_now = 0
        self.wu_xing_character_rate_step = 0.06
        self.si_xing_rate = 0.051
        # 武器池
        """不做了，因为我不抽武器池"""
        self.wu_xing_weapon_up = []
        self.si_xing_weapon_up = []
        self.wu_xing_weapon_rate = 0
        self.wu_xing_weapon_rate_now = 0
        self.wu_xing_weapon_rate_step = 0
        self.si_xing_weapon_rate = 0

        # 非up池信息
        self.wu_xing_character = []  # 常驻6虎
        self.wu_xing_weapon = []  # 常驻武器
        self.si_xing_character = []  # up池常驻4星角色
        self.si_xing_character_al = []  # 常驻4星角色
        self.si_xing_weapon = []  # 常驻4星武器
        self.san_xing_weapon = []  # 常驻3星武器

        # 抽卡机制
        self.mode = 0  # 0角色 | 1武器
        self.ding_gui = 0  # 0武器1 | 1武器2
        self.ding_gui_list = []  # 0歪了 | 1没歪
        self.pool = 0  # 抽哪个角色池子
        self.is_wu_xing_wai = 0  # 小保底是否歪 0否 | 1是
        self.is_si_xing_wai = 0  # 4星是否歪 0否 | 1是
        self.count = 0  # 目前多少抽
        self.baodi_count = 0  # 5星后多少抽
        self.si_xing_count = 0  # 累计多少抽无4星
        self.crazy = 0  # 狂暴抽卡模式
        self.wu_xing_temp = {}
        self.si_xing_temp = {}
        self.wu_xing_history = {}
        self.si_xing_history = {}
        self.wu_xing_history_detail = []
        self.history = {}  # 抽卡历史
        self.key = ""
        key = "help"  # 初始化key
        self.init()

        while True:
            if key == "3":
                self.run()
                key = ""
                continue
            key = input("是否抽卡？") if key == "" else key
            if key == "0":  # 退出
                break
            elif key == "1":  # 切换模式
                self.mode = 0 if self.mode == 1 else 1
                self.note()
            elif key == "2":  # 切换池子
                self.pool = 0 if self.pool == 1 else 1
                self.note()
            elif key == "3":
                self.crazy = 1
                print("开启狂暴抽卡模式！")
                continue
            elif key == "4":  # 查看记录
                print("抽卡记录：")
                self.show_history()
            elif key == "5":  # 清空记录
                print("记录已清空！")
                self.clear()
            elif key == "6":  # 超级狂暴抽卡
                print("开启超级狂暴抽卡模式！抽到满命为止！")
                try:
                    if self.wu_xing_history[self.wu_xing_character_up[self.pool]] < 7:
                        self.key = "6"
                    else:
                        self.key = ""
                        self.show_history()
                        self.clear()
                except KeyError:
                    self.key = "6"
                self.crazy = 0
                self.run()
            elif key == "help":  # 帮助
                print("""
                欢迎使用文文小可爱的原神抽卡模拟器，作者UID：109628495，欢迎添加好友
                (使用说明)->是否抽卡？ (ENTER 十连) | (0 退出) | (1 切换角色/武器池) | (2 切换up池) | (3 狂暴抽卡) | (4 抽卡记录) | (5 清空记录) | (6 超级狂暴抽卡) | (help 帮助)
                """)
                self.note()
            else:
                self.run()
                self.crazy = 0
            key = self.key

    def init(self):
        # 确定up池信息
        self.wu_xing_character_up = ["妮露", "阿贝多"]  # 5星角色
        self.si_xing_character_up = ["香菱", "北斗", "芭芭拉"]  # 4星角色
        self.wu_xing_weapon_up = ["阿莫斯之弓", "不灭月华"]  # 5星武器
        self.si_xing_weapon_up = ["弓藏", "祭礼剑", "昭心", "匣里灭辰", "西风大剑"]  # 4星武器

        # 读取非up池信息
        # [五星常驻角色，五星常驻武器，四星常驻角色，御三家，四星常驻武器，三星武器]
        with open("pool.json", "r") as f:
            data = json.load(f)
        for characters in data[0].values():
            self.wu_xing_character.append(characters)
        for weapons in data[1].values():
            self.wu_xing_weapon.append(weapons)
        for characters in data[2].values():
            self.si_xing_character.append(characters)
            self.si_xing_character_al.append(characters)
        for characters in data[3].values():
            self.si_xing_character_al.append(characters)
        for weapons in data[4].values():
            self.si_xing_weapon.append(weapons)
        for weapons in data[5].values():
            self.san_xing_weapon.append(weapons)
        # 消除重复部分
        self.si_xing_character = list(set(self.si_xing_character))
        self.si_xing_weapon = list(set(self.si_xing_weapon))
        self.wu_xing_character_rate_now = self.wu_xing_character_rate
        self.wu_xing_weapon_rate_now = self.wu_xing_weapon_rate

    def note(self):
        pools = ["角色up池1：%s" % self.wu_xing_character_up[0], "角色up池2：%s" % self.wu_xing_character_up[1], "武器up池"]
        if self.mode == 0 and self.pool == 0:
            pool = pools[0]
        elif self.mode == 0 and self.pool == 1:
            pool = pools[1]
        else:
            pool = pools[2]
        print("当前抽取卡池为：%s" % pool)

    def run(self):
        """
        还没有做武器池和常驻池
        """
        if self.crazy == 1:
            num = input("【狂暴抽卡】请输入十连数量：")
            num_all = int(num) if num != "" else 8
        else:
            num_all = 1
        for j in range(num_all):
            items = []
            is_si_xing = 0
            for i in range(10):
                self.count += 1
                self.baodi_count += 1
                if self.mode == 0:  # 角色up池
                    if self.si_xing_count == 9 and is_si_xing == 0:  # 4星保底
                        self.si_xing_count = 0
                        si_xing = self.random_generate([0.5, 0.5])
                        if si_xing == 0:
                            rate = 1 / len(self.si_xing_character_up)
                            bu_wai = self.random_generate([rate] * len(self.si_xing_character_up))
                            items.append(self.si_xing_character_up[bu_wai])
                        else:
                            new_si_xing = self.si_xing_character + self.si_xing_weapon
                            rate = 1 / len(new_si_xing)
                            wai = self.random_generate([rate] * len(new_si_xing))
                            items.append(new_si_xing[wai])
                    if self.baodi_count > 72:
                        self.wu_xing_character_rate_now = self.wu_xing_character_rate + self.wu_xing_character_rate_step * (self.baodi_count - 72) if self.baodi_count < 90 else 1
                    item = self.random_generate([self.wu_xing_character_rate_now, self.si_xing_rate])
                    if item == 0:  # 抽到5星
                        self.si_xing_count += 1
                        self.wu_xing_character_rate_now = self.wu_xing_character_rate
                        wu_xing = self.random_generate([0.5, 0.5])
                        if self.is_wu_xing_wai == 1:  # 大保底
                            self.is_wu_xing_wai = 0
                            items.append(self.wu_xing_character_up[self.pool])
                        else:
                            if wu_xing == 0:
                                self.is_wu_xing_wai = 0
                                items.append(self.wu_xing_character_up[self.pool])
                            else:
                                self.is_wu_xing_wai = 1
                                rate = 1 / len(self.wu_xing_character)
                                wai = self.random_generate([rate] * len(self.wu_xing_character))
                                items.append(self.wu_xing_character[wai])
                        self.wu_xing_history_detail.append("%s: %d抽" % (items[-1], self.baodi_count))
                        self.baodi_count = 0
                    elif item == 1:  # 抽到4星
                        self.si_xing_count = 0
                        is_si_xing = 1
                        if self.is_si_xing_wai == 0:
                            si_xing = self.random_generate([0.5, 0.5])
                        else:
                            si_xing = 0
                        if si_xing == 0:
                            self.is_si_xing_wai = 0
                            rate = 1 / len(self.si_xing_character_up)
                            bu_wai = self.random_generate([rate] * len(self.si_xing_character_up))
                            items.append(self.si_xing_character_up[bu_wai])
                        else:
                            self.is_si_xing_wai = 1
                            new_si_xing = self.si_xing_character + self.si_xing_weapon
                            rate = 1 / len(new_si_xing)
                            wai = self.random_generate([rate] * len(new_si_xing))
                            items.append(new_si_xing[wai])
                    else:  # 抽到3星
                        self.si_xing_count += 1
                        rate = 1 / len(self.san_xing_weapon)
                        san_xing = self.random_generate([rate] * len(self.san_xing_weapon))
                        items.append(self.san_xing_weapon[san_xing])
                elif self.mode == 1:
                    pass
            items = self.remake(items)
            print(items)
            # 全部历史
            # for item in items:
            #     if item not in self.history.keys():
            #         self.history[item] = 1
            #     else:
            #         self.history[item] += 1

    # 将抽卡结果按照5星、4星、3星排列，更新抽卡记录
    def remake(self, lists: list) -> list:
        result_remake = []
        for item in lists:
            if item in self.wu_xing_character + self.wu_xing_character_up:
                if item not in self.wu_xing_temp.keys():
                    self.wu_xing_temp[item] = 1
                else:
                    self.wu_xing_temp[item] += 1
            elif item in self.si_xing_character + self.si_xing_character_up + self.si_xing_weapon:
                if item not in self.si_xing_temp.keys():
                    self.si_xing_temp[item] = 1
                else:
                    self.si_xing_temp[item] += 1
            else:
                result_remake.append(item)
        for i in self.si_xing_temp.keys():
            for j in range(self.si_xing_temp[i]):
                result_remake.insert(0, i)
        for i in self.wu_xing_temp.keys():
            for j in range(self.wu_xing_temp[i]):
                result_remake.insert(0, i)
        # 更新记录，另起一个函数更好
        for i in self.wu_xing_temp.keys():
            if i not in self.wu_xing_history.keys():
                self.wu_xing_history[i] = 1
            else:
                self.wu_xing_history[i] += 1
        for i in self.si_xing_temp.keys():
            if i not in self.si_xing_history.keys():
                self.si_xing_history[i] = 1
            else:
                self.si_xing_history[i] += 1
        self.wu_xing_temp = {}
        self.si_xing_temp = {}
        return result_remake

    # 按数量排序并展示记录
    def show_history(self):
        self.sort_dict(self.wu_xing_history)
        self.sort_dict(self.si_xing_history)
        print("共 %d 抽，距离保底 %d 抽" % (self.count, 90 - self.baodi_count))
        print("五星：%s" % self.wu_xing_history_detail)
        print("统计：%s" % self.wu_xing_history)
        print("四星：%s" % self.si_xing_history)

    def clear(self):
        self.wu_xing_history_detail = []
        self.wu_xing_history = {}
        self.si_xing_history = {}
        self.is_wu_xing_wai = 0
        self.is_si_xing_wai = 0
        self.count = 0
        self.baodi_count = 0
        self.si_xing_count = 0

    @staticmethod
    # 字典排序,用于查看记录时的数量排序
    def sort_dict(history: dict):
        pass

    @staticmethod
    # 生成随机抽卡事件
    def random_generate(lists: list) -> int:
        rate_sum = 0
        rate_len = len(lists)
        for i in range(rate_len):
            lists[i] = lists[i] if rate_sum + lists[i] <= 1 else 1 - rate_sum
            rate_sum += lists[i]
        max_len = 1000
        num = random.randint(0, max_len - 1)
        rate_temp = 0
        for i in range(rate_len):
            if rate_temp * max_len <= num < (rate_temp + lists[i]) * max_len:
                return i
            rate_temp += lists[i]
        return rate_len


new = Genshin()
