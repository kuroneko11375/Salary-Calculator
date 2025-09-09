"""
工作薪資計算程式

這是一個通用的工作薪資計算工具，支援：
1. 按日期範圍和週期計算薪資
2. 按天數統計計算薪資  
3. 自訂工作日期計算薪資

使用說明：
- 請修改 SALARY_CONFIG 中的數值以符合您的薪資結構
- 程式會根據工作日（週一到週日）自動計算對應薪資
- 支援週期性工作的薪資計算

作者: [SchwarzeKatze_R]
版本: 1.0
"""

from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry, Calendar
import locale
import babel.numbers
import babel.plural
import babel.core
import babel.dates

# 嘗試設定中文語系
try:
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
except locale.Error:
    print("無法設定為 zh_CN.UTF-8，請確認系統是否支援此語系。")

# ====== 配置區域 ======
# 請根據實際情況修改以下薪資設定
SALARY_CONFIG = {
    'weekday': 100,     # 週一~週四的薪資 (請修改為實際數值)
    'friday': 150,      # 週五的薪資 (請修改為實際數值)  
    'saturday': 200,    # 週六的薪資 (請修改為實際數值)
    'sunday': 180       # 週日的薪資 (請修改為實際數值)
}
# ==================

def get_daily_salary(target_date):
    """
    根據日期計算當日薪資
    
    Args:
        target_date: 目標日期
    
    Returns:
        int: 當日薪資金額
    """
    # Monday=0 ... Sunday=6
    day_of_week = target_date.weekday()
    if day_of_week in [0, 1, 2, 3]:  # Mon-Thu
        salary = SALARY_CONFIG['weekday']
    elif day_of_week == 4:  # Fri
        salary = SALARY_CONFIG['friday']
    elif day_of_week == 5:  # Sat
        salary = SALARY_CONFIG['saturday']
    else:  # Sun
        salary = SALARY_CONFIG['sunday']

    return salary

def calculate_total_salary(start_date, end_date, cycle_days):
    """
    計算週期性工作的總薪資
    
    Args:
        start_date: 開始日期
        end_date: 結束日期
        cycle_days: 週期天數
    
    Returns:
        int: 總薪資金額
    """
    total_salary = 0
    # 終止計算日期為該 end_date 的當月25日
    salary_end_date = end_date.replace(day=25)

    loop_date = start_date
    while loop_date <= end_date:
        if loop_date > salary_end_date:
            break
        total_salary += get_daily_salary(loop_date)
        loop_date += timedelta(days=cycle_days)

    return total_salary

def on_calculate_date():
    try:
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()

        cycle_days = int(entry_cycle.get())
        if cycle_days <= 0:
            messagebox.showwarning("警告", "週期天數必須大於0")
            return

        total = calculate_total_salary(start_date, end_date, cycle_days)
        label_result_date.config(text=f"總計: {total}")
    except ValueError as ve:
        messagebox.showerror("錯誤", f"輸入格式有誤: {ve}")
    except Exception as ex:
        messagebox.showerror("錯誤", f"發生錯誤: {ex}")

def on_clear_date():
    entry_cycle.delete(0, tk.END)
    entry_cycle.insert(0, "4") # 預設4天
    label_result_date.config(text="")

def on_calculate_quantity():
    """
    根據天數統計計算總薪資
    """
    try:
        count_weekday = int(entry_0_3.get() or "0")
        count_friday = int(entry_4.get() or "0")
        count_saturday = int(entry_5.get() or "0")
        count_sunday = int(entry_sun.get() or "0")

        # 計算總薪資
        total = (count_weekday * SALARY_CONFIG['weekday'] + 
                count_friday * SALARY_CONFIG['friday'] + 
                count_saturday * SALARY_CONFIG['saturday'] + 
                count_sunday * SALARY_CONFIG['sunday'])
        label_result_quantity.config(text=f"總計: {total}")
    except ValueError:
        messagebox.showerror("錯誤", "請輸入正確的整數值")
    except Exception as ex:
        messagebox.showerror("錯誤", f"發生錯誤: {ex}")

def on_clear_quantity():
    entry_0_3.delete(0, tk.END)
    entry_4.delete(0, tk.END)
    entry_5.delete(0, tk.END)
    entry_sun.delete(0, tk.END)
    label_result_quantity.config(text="")

# 第三個頁籤相關程式：
custom_dates = []  # 用於儲存使用者自訂的值班日期列表

def on_add_selected_date():
    # 'day'模式下 cal.selection_get() 取得目前已選日期
    selected_date = cal.selection_get()
    if selected_date is None:
        messagebox.showinfo("提示", "尚未選擇日期")
        return
    if selected_date not in custom_dates:
        custom_dates.append(selected_date)
        update_custom_date_list()

def update_custom_date_list():
    listbox_custom_dates.delete(0, tk.END)
    for d in sorted(custom_dates):
        listbox_custom_dates.insert(tk.END, d.strftime("%Y-%m-%d"))

def on_clear_custom_dates():
    custom_dates.clear()
    update_custom_date_list()
    label_result_custom.config(text="")

def on_calculate_custom():
    """
    計算自訂日期的總薪資
    """
    total = 0
    for d in custom_dates:
        total += get_daily_salary(d)
    label_result_custom.config(text=f"總計: {total}")

# 主程式開始

root = tk.Tk()
root.title("工作薪資計算程式")
root.geometry("430x500")
root.resizable(False, False)  # 固定視窗大小

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=5)

# 日期計算 TAB
frame_date = ttk.Frame(notebook)
notebook.add(frame_date, text="日期計算")

# 建立主框架來置中內容
main_frame_date = ttk.Frame(frame_date)
main_frame_date.pack(expand=True, pady=20)

ttk.Label(main_frame_date, text="開始日期:", font=("Arial", 9)).grid(row=0, column=0, padx=10, pady=8, sticky="e")
start_cal = DateEntry(main_frame_date, date_pattern='yyyy/MM/dd', 
                     year=datetime.now().year, month=datetime.now().month, 
                     day=datetime.now().day, locale='zh_CN', width=12)
start_cal.grid(row=0, column=1, padx=10, pady=8, sticky="w")

ttk.Label(main_frame_date, text="結束日期:", font=("Arial", 9)).grid(row=1, column=0, padx=10, pady=8, sticky="e")
end_cal = DateEntry(main_frame_date, date_pattern='yyyy/MM/dd', 
                   year=datetime.now().year, month=datetime.now().month, 
                   day=datetime.now().day, locale='zh_CN', width=12)
end_cal.grid(row=1, column=1, padx=10, pady=8, sticky="w")

ttk.Label(main_frame_date, text="週期天數:", font=("Arial", 9)).grid(row=2, column=0, padx=10, pady=8, sticky="e")
entry_cycle = ttk.Entry(main_frame_date, width=15)
entry_cycle.grid(row=2, column=1, padx=10, pady=8, sticky="w")
entry_cycle.insert(0, "4")  # 預設4天

# 按鈕框架
button_frame_date = ttk.Frame(main_frame_date)
button_frame_date.grid(row=3, column=0, columnspan=2, pady=15)

btn_calc_date = ttk.Button(button_frame_date, text="計算", command=on_calculate_date, width=10)
btn_calc_date.pack(side="left", padx=5)

btn_clear_date = ttk.Button(button_frame_date, text="清除", command=on_clear_date, width=10)
btn_clear_date.pack(side="left", padx=5)

# 結果顯示
result_frame_date = ttk.Frame(main_frame_date)
result_frame_date.grid(row=4, column=0, columnspan=2, pady=10)

label_result_date = ttk.Label(result_frame_date, text="", font=("Arial", 10, "bold"), 
                             foreground="blue")
label_result_date.pack()

# 數量計算 TAB
frame_quantity = ttk.Frame(notebook)
notebook.add(frame_quantity, text="數量計算")

# 建立主框架來置中內容
main_frame_quantity = ttk.Frame(frame_quantity)
main_frame_quantity.pack(expand=True, pady=20)

ttk.Label(main_frame_quantity, text="週一~週四天數:", font=("Arial", 9)).grid(row=0, column=0, padx=10, pady=8, sticky="e")
entry_0_3 = ttk.Entry(main_frame_quantity, width=15)
entry_0_3.grid(row=0, column=1, padx=10, pady=8, sticky="w")

ttk.Label(main_frame_quantity, text="週五天數:", font=("Arial", 9)).grid(row=1, column=0, padx=10, pady=8, sticky="e")
entry_4 = ttk.Entry(main_frame_quantity, width=15)
entry_4.grid(row=1, column=1, padx=10, pady=8, sticky="w")

ttk.Label(main_frame_quantity, text="週六天數:", font=("Arial", 9)).grid(row=2, column=0, padx=10, pady=8, sticky="e")
entry_5 = ttk.Entry(main_frame_quantity, width=15)
entry_5.grid(row=2, column=1, padx=10, pady=8, sticky="w")

ttk.Label(main_frame_quantity, text="週日天數:", font=("Arial", 9)).grid(row=3, column=0, padx=10, pady=8, sticky="e")
entry_sun = ttk.Entry(main_frame_quantity, width=15)
entry_sun.grid(row=3, column=1, padx=10, pady=8, sticky="w")

# 按鈕框架
button_frame_quantity = ttk.Frame(main_frame_quantity)
button_frame_quantity.grid(row=4, column=0, columnspan=2, pady=15)

btn_calc_quantity = ttk.Button(button_frame_quantity, text="計算", command=on_calculate_quantity, width=10)
btn_calc_quantity.pack(side="left", padx=5)

btn_clear_quantity = ttk.Button(button_frame_quantity, text="清除", command=on_clear_quantity, width=10)
btn_clear_quantity.pack(side="left", padx=5)

# 結果顯示
result_frame_quantity = ttk.Frame(main_frame_quantity)
result_frame_quantity.grid(row=5, column=0, columnspan=2, pady=10)

label_result_quantity = ttk.Label(result_frame_quantity, text="", font=("Arial", 10, "bold"), 
                                 foreground="blue")
label_result_quantity.pack()

# 自訂值班日期 TAB
frame_custom = ttk.Frame(notebook)
notebook.add(frame_custom, text="自訂值班日期")

# 建立主框架
main_frame_custom = ttk.Frame(frame_custom)
main_frame_custom.pack(expand=True, pady=10)

# 日曆區域
cal_frame = ttk.Frame(main_frame_custom)
cal_frame.pack(pady=5)

cal = Calendar(cal_frame, selectmode='day', showweeknumbers=False, 
              date_pattern='yyyy/mm/dd', locale='zh_CN')
cal.pack()

# 說明文字
ttk.Label(main_frame_custom, text="點選日曆中的日期來選擇該日期", 
         font=("Arial", 8)).pack(pady=5)

# 按鈕區域
button_frame_custom = ttk.Frame(main_frame_custom)
button_frame_custom.pack(pady=10)

btn_add_dates = ttk.Button(button_frame_custom, text="加入選取日期", 
                          command=on_add_selected_date, width=12)
btn_add_dates.pack(side="left", padx=3)

btn_clear_custom_list = ttk.Button(button_frame_custom, text="清除列表", 
                                  command=on_clear_custom_dates, width=10)
btn_clear_custom_list.pack(side="left", padx=3)

btn_calc_custom = ttk.Button(button_frame_custom, text="計算總計", 
                            command=on_calculate_custom, width=10)
btn_calc_custom.pack(side="left", padx=3)

# 日期列表區域
list_frame = ttk.Frame(main_frame_custom)
list_frame.pack(pady=5)

ttk.Label(list_frame, text="已選擇的日期:", font=("Arial", 9)).pack()
listbox_custom_dates = tk.Listbox(list_frame, width=30, height=6, font=("Arial", 8))
listbox_custom_dates.pack(pady=5)

# 結果顯示
result_frame_custom = ttk.Frame(main_frame_custom)
result_frame_custom.pack(pady=5)

label_result_custom = ttk.Label(result_frame_custom, text="", font=("Arial", 10, "bold"), 
                               foreground="blue")
label_result_custom.pack()

root.mainloop()
