import csv
import json
import pprint

class Pay:
    def __init__(self):
        # 加工後の明細リスト
        self.pay_after = []
        # 支払い種類ごとの合計金額リスト
        self.kind_cost = {}

    """ jsonファイルの情報を取得
    """
    def key(self):
        # 支払の種類ごとのマップをjsonファイルから取得
        with open("source/item.json", 'r', encoding="utf-8") as f:
            json_data = json.load(f)

        return json_data

    """　明細リストを加工し、品目と金額のみの行を作成
    """
    def row(self):
        # 明細表リストをcsvファイルから取得
        with open('source/enavi202101(7981).csv', 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            pays = [row for row in reader]
        # 一行目のヘッダ部分を削除
        pays.remove(pays[0])

        # 明細リストを加工して格納
        for pay in pays:
            # 品目の文言を空白文字で分割
            pay_item = pay[1].split()
            # 明細一行分の配列
            pay_col = []

            # 品目名を加工
            if pay_item[0] == "現地利用額":
                # 不要な行を飛ばす
                continue
            else:
                # 分割した配列を統合
                pay_item = "".join(pay_item)

            # 明細に品目と金額を格納
            pay_col.append(pay_item)
            pay_col.append(pay[4])
            # 一行分の明細を格納
            self.pay_after.append(pay_col)

        return self.pay_after

    """ 支払い種類ごとの合計金額を計算
    """
    def result(self, json_data, pays):
        # "食事", "日用品", "月々の支払", "月々の交遊費", "交遊費", "その他"の合計金額
        sum1, sum2, sum3, sum4, sum5, sum6 = 0, 0, 0, 0, 0, 0

        # 明細リストを順に参照
        for pay in pays:
            # print(pay, end="\n")

            # jsonファイルを支払い種類ごとに参照
            for data in json_data:
                if data == "食費":
                    if pay[0] in json_data[data]:
                        sum1 += int(pay[1])
                        # print(pay[0], pay[1], sum1, end="\n")
                elif data == "日用品":
                    if pay[0] in json_data[data]:
                        sum2 += int(pay[1])
                        # print(pay[0], pay[1], sum2, end="\n")
                elif data == "月々の支払":
                    if pay[0] in json_data[data]:
                        sum3 += int(pay[1])
                        # print(pay[0], pay[1], sum3, end="\n")
                elif data == "月々の交遊費":
                    if pay[0] in json_data[data]:
                        sum4 += int(pay[1])
                        # print(pay[0], pay[1], sum4, end="\n")
                elif data == "交遊費":
                    if pay[0] in json_data[data]:
                        sum5 += int(pay[1])
                        # print(pay[0], pay[1], sum5, end="\n")
                elif data == "その他":
                    if pay[0] in json_data[data]:
                        sum6 += int(pay[1])
                        # print(pay[0], pay[1], sum6, end="\n")

        self.kind_cost = {"食費":sum1, "日用品":sum2, "月々の支払":sum3, "月々の交遊費":sum4, "交遊費":sum5, "その他":sum6}

        return self.kind_cost

    """ 取りこぼした品目を計算
    """
    def miss(self, json_data, pays):
        # 合計金額, 取りこぼし品目の合計金額
        sum0, sum1 = 0, 0

        # 明細リストを順に参照
        for pay in pays:
            # 全ての金額を合計
            sum0 += int(pay[1])

            # jsonファイルのvalueを平坦化
            json_data_value = sum(json_data.values(), [])
            # jsonファイルが拾えていない品目を取得
            if pay[0] not in json_data_value:
                print(pay, end="\n")
                sum1 += int(pay[1])

        # 合計金額を出力
        print('合計金額 : {sum0}円\n'.format(sum0))
        # 取りこぼし品目の合計を出力する
        print('取りこぼし品目の合計 : {sum1}円\n'.format(sum1))

    """ 計算結果を出力
    """
    def total(self, result):
        total = 0

        for key in result:
            total += result[key]

        print(result, end="\n")
        print(total, end="\n")

pay = Pay()

# key関数
json_data = pay.key()
# row関数
pays = pay.row()
# result関数
result = pay.result(json_data, pays)
# miss関数
pay.miss(json_data, pays)
# total関数
# pay.total(result)