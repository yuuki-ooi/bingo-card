import tkinter as tk
import random

class BingoCard:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Card")
        self.selected = [[False] * 5 for _ in range(5)]  # 選択状態を管理
        self.card_numbers = self.generate_card()  # ビンゴカードの生成

        # 5x5のボタンを配置
        self.buttons = []
        for i in range(5):
            row = []
            for j in range(5):
                button = tk.Button(root, text=str(self.card_numbers[i][j]), font=("Helvetica", 16),
                                   width=5, height=2, command=lambda x=i, y=j: self.select_number(x, y))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

        # 判定ボタンとラベル
        self.check_button = tk.Button(root, text="Check Bingo", command=self.check_bingo)
        self.check_button.grid(row=6, column=0, columnspan=5, pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label.grid(row=7, column=0, columnspan=5)

    def generate_card(self):
        card = []
        # B, I, N, G, O 列ごとに異なる範囲で番号を生成
        columns = [random.sample(range(i, i + 15), 5) for i in range(1, 76, 15)]
        # 真ん中を"FREE"に設定
        for i in range(5):
            column = columns[i]
            card.append(column)
        card[2][2] = "FREE"
        return list(map(list, zip(*card)))  # 転置して5x5の行列にする

    def select_number(self, x, y):
        if not self.selected[x][y] and self.card_numbers[x][y] != "FREE":
            self.buttons[x][y].config(bg="lightblue")
            self.selected[x][y] = True
        elif self.card_numbers[x][y] != "FREE":
            self.buttons[x][y].config(bg="SystemButtonFace")
            self.selected[x][y] = False

    def check_bingo(self):
        # 行と列、対角線でリーチ・ビンゴを確認
        def is_bingo_line(line):
            return all(self.selected[x][y] or self.card_numbers[x][y] == "FREE" for x, y in line)

        lines = [
            # 行
            [(i, j) for j in range(5)] for i in range(5)
        ] + [
            # 列
            [(j, i) for j in range(5)] for i in range(5)
        ] + [
            # 対角線
            [(i, i) for i in range(5)], [(i, 4 - i) for i in range(5)]
        ]

        if any(is_bingo_line(line) for line in lines):
            self.result_label.config(text="Bingo!")
        elif any(sum(self.selected[x][y] for x, y in line) == 4 for line in lines):
            self.result_label.config(text="Reach!")
        else:
            self.result_label.config(text="No Bingo or Reach")

if __name__ == "__main__":
    root = tk.Tk()
    bingo_card = BingoCard(root)
    root.mainloop()
