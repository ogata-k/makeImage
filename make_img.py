# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 18:20:22 2017

@author: Owner
"""

from PIL import Image
import os
import time


# 入力関係
def get_useable_int(msg, minimam, maximam=None):
    while True:
        try:
            num = int(input(msg))
        except ValueError:
            print("入力が不正です。")
            continue
        if num < minimam or (maximam is not None and num > maximam):
            print("入力された数値は使えません。")
        else:
            break
    return num


def get_high_width():
    h = get_useable_int("縦の長さを入力してください:", 1)
    w = get_useable_int("横の長さを入力してください:", 1)
    return (h, w)


def get_color_type():
    print("使用する色の系統を入力してください。")
    print("r:赤色系統")
    print("g:緑色系統")
    print("b:青色系統")
    print("d:黒色系統")
    while True:
        ctype = input(">>")
        if ctype not in ["r", "g", "b", "d"]:
            print("入力された系統は不正です。rgbdのどれかを入力してください。")
        else:
            break
    return ctype


# ルール関係
def is_nums_rule(target, h, w, maxnum):
    if len(target) != h:
        return False
    for l in target:
        if len(l) != w:
            return False
        for c in l:
            if c not in list(range(maxnum)):
                return False
    return True


def input_nums_rule(h):
    while True:
        try:
            tmp = [[int(x) for x in list(input())] for i in range(h)]
        except ValueError:
            print("入力が不正です。")
            continue
        break
    return tmp


def make_rule(h, w, maxnum):
    print("長さが{1}となる0から{2}未満の数字からなる文字列を{0}回入力してください。".
          format(h, w, maxnum))
    rule = input_nums_rule(h)
    while not is_nums_rule(rule, h, w, maxnum):
        print("文字列は不正でした。もう一度入力をお願いします。")
        rule = input_nums_rule(h)

    return rule


# 変換関係
def insert(target, base, h, w):
    hbase = len(base)
    wbase = len(base[0])
    for i in range(hbase):
        for j in range(wbase):
            target[h+i][w+j] = base[i][j]


def converter(target, bases):
    hbase = len(bases[0])  # 各baseの縦の長さ(すべてのbaseに長さの差はない)
    wbase = len(bases[0][0])  # 各baseの縦の長さ(すべてのbaseに長さの差はない)
    htarget = len(target)  # targetの縦の長さ
    wtarget = len(target[0])  # targetの横の長さ
    tmp = [[0 for j in range(wtarget*wbase)] for i in range(htarget*hbase)]
    for h in range(htarget):
        for w in range(wtarget):
            insert(tmp, bases[target[h][w]], h*hbase, w*wbase)
    return tmp


# 文字列での表示関係
# 注意 多数版には対応していない
def print_img(target, convert_dict={0: "O", 1: "@"}):
    for l in target:
        for c in l:
            print(convert_dict[c], end="")
        print()


# 画像関係
def make_img(target, NUM, color_type="d"):
    # color_typeはr, b, g, d(dark)の4種類
    color_dict = {"r": 0, "g": 1, "b": 2, "d": None}
    img = Image.new("RGB", (len(target[0]), len(target)))
    sep = 255 // (NUM-1)
    for h in range(len(target)):
        for w in range(len(target[0])):
            c = target[h][w]
            col = 255-c*sep
            colors = [col, col, col]
            if color_dict[color_type] is not None:
                colors[color_dict[color_type]] = 255
            img.putpixel((w, h), tuple(colors))
    print("画像の生成に成功しました。\n")
    return img


def resize_img(img):
    sizers = [img.size, (1024, 768), (1280, 1024), (1500, 500),
              (400, 400), (640, 520), (1024, 1024)]
    strings = ["そのまま", "４：３", "５：４", "ヘッダー用", "アイコン用",
               "Lineホーム用", "大きめの正方形"]
    print("画像のサイズを変更することができます。")
    for i, (sizer, s) in enumerate(zip(sizers, strings)):
        print("{0}:{1[0]}×{1[1]}（{2}）".format(i, sizer, s))
    choice = get_useable_int("対応する番号を入力してください:", 0, len(sizers)-1)
    resize_img = img.resize(sizers[choice])
    print("変換が完了しました。")
    return resize_img

if __name__ == "__main__":
    NUM = get_useable_int("挿入用リストの個数(2以上10以下)を入力してください:", 2, 10)
    HSIZE, WSIZE = get_high_width()
    bases = []
    for i in range(NUM):
        print("\n"+str(i)+"の時の挿入用を入力します。")
        bases.append(make_rule(HSIZE, WSIZE, NUM))

    print("\n変換用初期ルールを入力します。")
    h, w = get_high_width()
    print()
    target = make_rule(h, w, NUM)

    COUNT = get_useable_int("\n変換を繰り返す回数を入力してください:", 0)
    for count in range(COUNT):
        target = converter(target, bases)  # 変換
        # print_img(target, CONVERTDICT)  # 文字列での表示

    # 画像の生成と変換と保存
    print()
    ctype = get_color_type()
    img = make_img(target, NUM, color_type=ctype)
    img = resize_img(img)

    try:
        os.chdir("image")
    except:
        os.mkdir("image")
        os.chdir("image")
    fname = time.strftime("%Y%m%d%H%M%S.png", time.localtime())
    img.save(fname)
    input("改行を押して終了します。")
