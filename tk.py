import tkinter as tk
import calendar
from datetime import datetime, timedelta


# 表示される月の日にちと曜日を保存する関数
def get_dates_and_weekdays(year, month):
    # 月の最初の日を取得
    start_date = datetime(year, month, 1)
    # 翌月の最初の日を計算し、その1日前（月の最後の日）を取得
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    # 月の全ての日付と曜日を含むリストを作成
    dates_and_weekdays = []
    current_date = start_date
    while current_date <= end_date: 
        weekday_name = calendar.day_name[current_date.weekday()] # calendar.day_nameによりweekdayで取得した曜日番号をMondayなどの文字列にする
        dates_and_weekdays.append((current_date.strftime("%Y-%m-%d"), weekday_name)) # strftimeによって日付を文字列化(例:2026-05-01)
        current_date += timedelta(days=1) # 1日進める

    return dates_and_weekdays

    

class MultiSelectCalendar(tk.Frame):

    # 初期化
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_grid()
        self.create_widgets()
        self.date_list = [] # 選択された日付を保存するためのリスト

    # レイアウト設定     
    def create_grid(self):
        self.grid_rowconfigure(0, weight=1) # 上メニュー
        self.grid_rowconfigure(1, weight=4) # カレンダー
        self.grid_rowconfigure(2, weight=1) # 閉じるボタン

    # GUI作成
    def create_widgets(self):
        self.top = tk.Frame(self) # 上部UI専用フレーム
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.current_day = datetime.now().day
        self.year_choose = tk.IntVar() # int型に設定
        self.month_choose = tk.IntVar()
        self.year_choose.set(self.current_year)
        self.month_choose.set(self.current_month)
        # Spinbox=上下選択ボタン
        self.year_spinbox = tk.Spinbox(self.top, from_=self.current_year-5, to=self.current_year+10, textvariable=self.year_choose, width=5,command =self.fill_day)

        self.year_spinbox.pack(side="left")
        self.year_label = tk.Label(self.top, text="年")
        self.year_label.pack(side="left")
        self.month_spinbox = tk.Spinbox(self.top, from_=1, to=12, textvariable=self.month_choose, width=5,command = self.fill_day)
        self.month_spinbox.pack(side="left")
        self.month_label = tk.Label(self.top, text="月")
        self.month_label.pack(side="left")
        self.top.grid(row=0, column=0, sticky="nsew")
        self.calender = tk.Canvas(self, width=500, height=500)
        self.calender.bind("<Button-1>", self.select_day) # "<Button-1>"=左クリックイベント登録
        self.create_calender() # 枠描画
        self.fill_day() # 日付表示
        self.calender.grid(row=1, column=0, sticky="nsew")
        self.exit_button = tk.Button(self, text="閉じる", command=self.close)
        self.exit_button.grid(row=2, column=0, sticky="nsew")
        
    # 終了
    def close(self):
        self.master.destroy()
    
    # カレンダーの枠描画
    def create_calender(self):
        self.calender.create_rectangle(0, 0, 490, 490, fill="white") # 背景
        self.calender.create_line(0, 70, 490, 70)
        self.calender.create_line(0, 140, 490, 140)
        self.calender.create_line(0, 210, 490, 210)
        self.calender.create_line(0, 280, 490, 280)
        self.calender.create_line(0, 350, 490, 350)
        self.calender.create_line(0, 420, 490, 420)
        self.calender.create_line(70, 0, 70, 490)
        self.calender.create_line(140, 0, 140, 490)
        self.calender.create_line(210, 0, 210, 490)
        self.calender.create_line(280, 0, 280, 490)
        self.calender.create_line(350, 0, 350, 490)
        self.calender.create_line(420, 0, 420, 490)
        self.calender.create_text(35, 35, text="日", font=("Helvetica", 20), fill="red")
        self.calender.create_text(105, 35, text="月", font=("Helvetica", 20))
        self.calender.create_text(175, 35, text="火", font=("Helvetica", 20))
        self.calender.create_text(245, 35, text="水", font=("Helvetica", 20))
        self.calender.create_text(315, 35, text="木", font=("Helvetica", 20))
        self.calender.create_text(385, 35, text="金", font=("Helvetica", 20))
        self.calender.create_text(455, 35, text="土", font=("Helvetica", 20), fill="blue")
    


    # 日付表示
    def fill_day(self):
        self.calender.delete("all") # Canvas全消去(前の月の日付削除)
        self.create_calender()
        self.year = int(self.year_spinbox.get())
        self.month = int(self.month_spinbox.get())

        day_list = get_dates_and_weekdays(self.year,self.month)

        week_count = 0
        for day in day_list:
            if day[1] == "Sunday":
                self.calender.create_text(35, 105+70*week_count, text=day[0][8:], font=("Helvetica", 20), fill="red")
            if day[1] == "Monday":
                self.calender.create_text(105, 105+70*week_count, text=day[0][8:], font=("Helvetica", 20))
            if day[1] == "Tuesday":
                self.calender.create_text(175, 105+70*week_count, text=day[0][8:], font=("Helvetica", 20))
            if day[1] == "Wednesday":
                self.calender.create_text(245, 105+70*week_count, text=day[0][8:], font=("Helvetica", 20))
            if day[1] == "Thursday":
                self.calender.create_text(315, 105+70*week_count, text=day[0][8:], font=("Helvetica", 20))
            if day[1] == "Friday":
                self.calender.create_text(385, 105+70*week_count, text=day[0][8:], font=("Helvetica", 20))
            if day[1] == "Saturday":
                self.calender.create_text(455, 105+70*week_count, text=day[0][8:], font=("Helvetica", 20), fill="blue")
                week_count += 1
            


    # 日付選択
    def choose_day(self,x,y):
        x = x//70
        y = y//70-1
        day = self.calender.itemcget(self.calender.find_closest(x*70+35, y*70+105)[0], "text")
        if not day.isdigit():
            return
        date = f"{self.year}-{self.month}-{day:02}"
        if date in self.date_list:
            self.date_list.remove(date)
            self.calender.itemconfig(self.calender.find_closest(x*70+35,y*70+105)[0], fill = "black")
        else:
            self.date_list.append(date)
            self.calender.itemconfig(self.calender.find_closest(x*70+35,y*70+105)[0], fill = "green")
        print(self.date_list)
        return self.date_list
    


    # クリック処理
    def select_day(self, event):
        self.choose_day(event.x, event.y)
        print(sorted(self.date_list))

root = tk.Tk()
app = MultiSelectCalendar(root)
root.mainloop()
