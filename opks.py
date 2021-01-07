# -*- coding: utf-8 -*-
# @Author  : SiHuan

import math
import csv
import sys


class dfm():
    def __init__(self, de: int, mi: int, se: int):
        self.de = de
        self.mi = mi
        self.se = se

    def sjz(self):
        return float(self.de) + float(self.mi)/60 + float(self.se)/3600


class kzd():

    def __init__(self, dianhao: str, x: float, y: float, z: float, i: float):
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.dianhao = dianhao


class sbd():

    def __init__(self, dianhao: int, ss: float, zs: float, xs: float, hdfm: dfm, vdfm: dfm, kzd: kzd):
        self.dianhao = dianhao
        # # 碎步点的控制点
        self.kzd = kzd
        # 控制点到碎步点的方位角
        self.alpha = math.radians(hdfm.sjz())
        # 控制点到碎步点的竖直角
        self.delta = math.radians(90 - vdfm.sjz())
        # 控制点到碎步点的距离（视距测量）
        self.l = 100 * abs(ss - xs) * (math.cos(self.delta) ** 2) / 1000
        # 碎步点的 x
        self.x = kzd.x + self.l * math.cos(self.alpha)
        # 碎步点的 y
        self.y = kzd.y + self.l * math.sin(self.alpha)
        # 碎步点的 z
        self.z = kzd.z + self.l * math.tan(self.delta) + kzd.i - zs/1000
        # 高差
        self.dh = self.z - kzd.z
        # 斜距
        self.xj = math.sqrt(self.dh ** 2 + self.l ** 2)

    def for_cass(self):
        return [self.dianhao,'',f'{self.y:.3f}',f'{self.x:.3f}',f'{self.z:.3f}']

    def for_print(self):
        return f"{self.dianhao:>5}{self.kzd.dianhao:>10}{self.xj:>10.3f}{self.l:>10.3f}{self.dh:>10.3f}{self.x:>10.3f}{self.y:>10.3f}{self.z:>10.3f}"
    
    def for_web_print(self):
        return [f'{self.dianhao}',f'{self.kzd.dianhao}',f'{self.xj:.3f}',f'{self.l:.3f}',f'{self.dh:.3f}',f'{self.x:.3f}',f'{self.y:.3f}',f'{self.z:.3f}']



def main(arg):
    print(f"{'碎步点':^5}{'所属控制点':^6}{'斜距':^6}{'平距':^10}{'高差':^5}{'坐标x':^6}{'坐标y':^10}{'坐标z':^5}")
    with open('cass.dat', 'w', newline='') as f:
        with open(arg[1], 'r' ) as o_f:
            writer = csv.writer(f)
            line = o_f.readline()
            while line:
                if line[0] == '`':
                    line = o_f.readline()
                    continue
                od = line.split()
                if line[0] == '#':
                    now_kzd = kzd(od[0], float(od[1]), float(
                        od[2]), float(od[3]), float(od[4]))
                else:
                    hdfm = dfm(int(od[4]), int(od[5]), int(od[6]))
                    # vdfm = dfm(int(od[6]), int(od[7]), int(od[9]))
                    vdfm = dfm(90,0,0)
                    now_sbd = sbd(od[0], float(od[1]), float(od[2]),
                                  float(od[3]), hdfm, vdfm, now_kzd)
                    writer.writerow(now_sbd.for_cass())
                    print(now_sbd.for_print())
                line = o_f.readline()

if __name__ == "__main__":
    main(sys.argv)
