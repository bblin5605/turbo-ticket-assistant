from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import tkinter as tk
from tkinter import ttk
import time
import json
import os
from tkinter import messagebox
from tkcalendar import DateEntry

class TurboTicket:
    def __init__(self):
        self.driver = None
        self.url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"
        self.save_file = "ticket_data.json"
        
        # 初始化 Tk
        self.root = tk.Tk()
        self.root.title("TurboTicket Assistant")
        self.root.geometry("500x600")
        
        # 設定主題樣式
        style = ttk.Style()
        style.configure("Action.TButton", padding=5)
        style.configure("TLabelframe", padding=10)
        style.configure("TLabelframe.Label", font=("", 10, "bold"))
        
        self.load_saved_data()
        self.setup_gui()
        
    def load_saved_data(self):
        # 初始化儲存資料結構
        self.saved_data = {
            "slot1": {},
            "slot2": {},
            "slot3": {}
        }
        # 如果檔案存在則載入
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    self.saved_data = json.load(f)
            except:
                print("載入儲存資料時發生錯誤")

    def setup_gui(self):
        # 建立主要的捲動框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 開啟網頁按鈕
        self.start_button = tk.Button(main_frame, text="開啟訂票網頁", command=self.open_website)
        self.start_button.pack(pady=10)
        
        # 建立水平框架來容納提示訊息和儲存區
        info_container = ttk.Frame(main_frame)
        info_container.pack(fill="x", pady=10)
        
        # 左側儲存區域的框架
        save_frame = ttk.LabelFrame(info_container, text="儲存與載入", padding=(5, 2))
        save_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        # 建立三個儲存區的框架，改為垂直排列
        for i in range(3):
            slot_frame = ttk.Frame(save_frame)
            slot_frame.pack(pady=2)
            
            ttk.Label(slot_frame, text=f"區{i+1}", font=("", 9)).pack(side=tk.LEFT, padx=2)
            
            save_btn = ttk.Button(slot_frame, 
                                text="存", 
                                command=lambda x=i+1: self.save_data(f"slot{x}"),
                                style="Action.TButton",
                                width=3)
            save_btn.pack(side=tk.LEFT, padx=1)
            
            load_btn = ttk.Button(slot_frame, 
                                text="取", 
                                command=lambda x=i+1: self.load_data(f"slot{x}"),
                                style="Action.TButton",
                                width=3)
            load_btn.pack(side=tk.LEFT, padx=1)
        
        # 狀態標籤
        self.status_label = ttk.Label(save_frame, text="", font=("", 9))
        self.status_label.pack(pady=(5,0))
        
        # 右側提示訊息
        reminder_text = "請注意：\n" \
                       "1. 請先按下「開啟訂票網頁」\n" \
                       "2. 請在網頁中：\n" \
                       "   - 切換至「快速」訂票模式\n" \
                       "   - 查詢您要搭乘的車次\n" \
                       "   - 將出發站、抵達站和車次號碼\n" \
                       "     複製到本程式中\n" \
                       "3. 輸入或載入訂票資料\n" \
                       "4. 按下「開始訂票」前請先勾選「我不是機器人」"
        reminder_label = tk.Label(info_container, text=reminder_text, fg="red", justify=tk.LEFT)
        reminder_label.pack(side=tk.LEFT, fill="both", expand=True)
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # 建立一個框架來容納所有輸入欄位
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x", pady=10)
        
        # 身分證字號
        tk.Label(input_frame, text="身分證字號：").grid(row=0, column=0, sticky='w', pady=5)
        self.id_entry = tk.Entry(input_frame, width=30)
        self.id_entry.grid(row=0, column=1, pady=5, padx=5)
        # 添加輸入變更事件綁定
        self.id_entry.bind('<KeyRelease>', self.mask_id_number)
        # 儲存實際的身分證字號
        self.actual_id = ""
        
        # 出發站和抵達站的框架
        stations_frame = ttk.Frame(input_frame)
        stations_frame.grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        
        # 出發站
        tk.Label(stations_frame, text="出發站：").pack(side=tk.LEFT)
        self.from_station = tk.Entry(stations_frame, width=12)
        self.from_station.pack(side=tk.LEFT, padx=(0,5))
        
        # 交換按鈕
        swap_btn = ttk.Button(stations_frame, 
                            text="⇄",
                            width=3,
                            command=self.swap_stations)
        swap_btn.pack(side=tk.LEFT, padx=5)
        
        # 抵達站
        tk.Label(stations_frame, text="抵達站：").pack(side=tk.LEFT, padx=(5,0))
        self.to_station = tk.Entry(stations_frame, width=12)
        self.to_station.pack(side=tk.LEFT)
        
        # 日期選擇框架
        date_frame = ttk.Frame(input_frame)
        date_frame.grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        
        tk.Label(date_frame, text="乘車日期：").pack(side=tk.LEFT)
        self.date_entry = tk.Entry(date_frame, width=25)
        self.date_entry.pack(side=tk.LEFT, padx=(0,5))
        
        # 日曆按鈕
        def set_date():
            def confirm_date():
                selected_date = cal.get_date().strftime('%Y/%m/%d')
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, selected_date)
                top.destroy()
            
            top = tk.Toplevel(self.root)
            top.title("選擇日期")
            
            # 設定彈出視窗在主視窗中央
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 100
            top.geometry(f"300x250+{x}+{y}")
            
            cal = DateEntry(top, width=12, background='darkblue',
                          foreground='white', borderwidth=2,
                          date_pattern='yyyy/mm/dd',
                          locale='zh_TW')
            cal.pack(padx=10, pady=10)
            
            ttk.Button(top, text="確認", command=confirm_date).pack(pady=5)
            
        calendar_btn = ttk.Button(date_frame, 
                                text="📅", 
                                width=3,
                                command=set_date)
        calendar_btn.pack(side=tk.LEFT)
        
        # 車次輸入
        tk.Label(input_frame, text="車次：").grid(row=4, column=0, sticky='w', pady=5)
        self.train_number = tk.Entry(input_frame, width=30)
        self.train_number.grid(row=4, column=1, pady=5)
        
        # 座位數量下拉選單
        tk.Label(input_frame, text="一般座票數：").grid(row=5, column=0, sticky='w', pady=5)
        self.ticket_count = ttk.Combobox(input_frame, 
                                       values=["1", "2", "3", "4", "5", "6"],
                                       state="readonly",
                                       width=5)
        self.ticket_count.set("1")  # 預設選擇1張票
        self.ticket_count.grid(row=5, column=1, sticky='w', pady=5)
        self.ticket_count.bind('<<ComboboxSelected>>', self.update_child_ticket_options)
        
        # 兒童票數下拉選單
        tk.Label(input_frame, text="內含兒童票數：").grid(row=6, column=0, sticky='w', pady=5)
        self.child_ticket_count = ttk.Combobox(input_frame,
                                             values=["0", "1"],
                                             state="readonly",
                                             width=5)
        self.child_ticket_count.set("0")  # 預設選擇0張兒童票
        self.child_ticket_count.grid(row=6, column=1, sticky='w', pady=5)
        
        # 底部按鈕區域
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(pady=20, fill="x")
        
        # 右側操作按鈕
        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(side=tk.RIGHT)
        
        # 開始訂票按鈕
        self.book_button = ttk.Button(button_frame, 
                                    text="開始訂票", 
                                    command=self.start_booking,
                                    style="Action.TButton")
        self.book_button.pack(side=tk.LEFT, padx=5)
        
        # 關閉瀏覽器按鈕
        self.close_button = ttk.Button(button_frame, 
                                     text="關閉瀏覽器", 
                                     command=self.close_browser)
        self.close_button.pack(side=tk.LEFT, padx=5)
        
    def open_website(self):
        try:
            if not self.driver:
                # 添加選項來停用沙盒
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_argument('--log-level=3')
                options.add_argument('--silent')
                
                self.driver = webdriver.Chrome(options=options)
                
            self.driver.get(self.url)
            # 等待頁面加載完成
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "wrapper"))
            )
            # 獲取輸入的資料
            id_number = self.id_entry.get()
            from_stn = self.from_station.get()
            to_stn = self.to_station.get()
            
            print(f"身分證字號：{id_number}")
            print(f"出發站：{from_stn}")
            print(f"抵達站：{to_stn}")
            
        except Exception as e:
            print(f"開啟網站時發生錯誤：{str(e)}")
            
    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            
    def validate_date(self, date_str):
        try:
            if not date_str:
                return False
            year, month, day = date_str.replace('/', ' ').split()
            # 檢查年份是否為4位數
            if not (len(year) == 4 and year.isdigit()):
                return False
            # 檢查月份和日期是否在有效範圍內
            month = int(month)
            day = int(day)
            if not (1 <= month <= 12 and 1 <= day <= 31):
                return False
            return True
        except:
            return False

    def start_booking(self):
        try:
            if not self.driver:
                return
                
            # 顯示提示訊息
            result = tk.messagebox.askokcancel(
                "確認",
                "請確認您已經勾選了「我不是機器人」\n\n" \
                "若尚未勾選，請點擊「取消」並完成「勾選」後再試",
                icon='warning'
            )
            
            if not result:
                return
                
            # 等待基本資料區塊載入
            basic_info = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "basic-info"))
            )
            
            # 選擇身分證單選按鈕
            person_radio = self.driver.find_element(By.ID, "personlType")
            if not person_radio.is_selected():
                person_radio.click()
            
            # 填寫身分證字號（使用實際的身分證字號）
            id_input = self.driver.find_element(By.ID, "pid")
            id_input.clear()
            id_input.send_keys(self.actual_id)
            
            # 填寫出發站
            start_station = self.driver.find_element(By.ID, "startStation")
            start_station.clear()
            start_station.send_keys(self.from_station.get())
            
            # 填寫抵達站
            end_station = self.driver.find_element(By.ID, "endStation")
            end_station.clear()
            end_station.send_keys(self.to_station.get())
            
            # 擇單程
            oneway_radio = self.driver.find_element(By.CSS_SELECTOR, "input[value='ONEWAY']")
            if not oneway_radio.is_selected():
                oneway_radio.click()
            
            # 選擇依車次
            by_train_radio = self.driver.find_element(By.ID, "orderType1")
            if not by_train_radio.is_selected():
                by_train_radio.click()
            
            # 填寫一般座位數量
            normal_seat = self.driver.find_element(By.ID, "normalQty")
            normal_seat.clear()
            normal_seat.send_keys(self.ticket_count.get())
            
            # 驗證日期格式
            if not self.validate_date(self.date_entry.get()):
                print("請輸入正確的日期格式（YYYY/MM/DD）")
                return
            
            # 填寫日期 - 使用 JavaScript 直接設定值
            date_value = self.date_entry.get()
            js_script = f'document.getElementById("rideDate1").value = "{date_value}"'
            self.driver.execute_script(js_script)
            
            # 填寫車次
            train_no = self.driver.find_element(By.ID, "trainNoList1")
            train_no.clear()
            train_no.send_keys(self.train_number.get())
            
            # 點擊訂票按鈕後等待3秒
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='訂票']")
            submit_button.click()
            time.sleep(0.5)

            try:
                # 獲取兒童票數量
                child_tickets = int(self.child_ticket_count.get())
                
                # 根據兒童票數量設定票種
                if child_tickets > 0:
                    for index in range(1, child_tickets + 1):
                        try:
                            select = self.driver.find_element(By.CSS_SELECTOR, 
                                f"select[data-name='ticketType[{index}]']")
                            select_element = Select(select)
                            select_element.select_by_value("2")  # 2 代表孩童票
                        except Exception as e:
                            print(f"設定第 {index} 張兒童票時發生錯誤：{str(e)}")
                
                # 尋找並點擊完成訂票按鈕
                next_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'][title='完成訂票']")
                print("找到完成訂票按鈕")
                
                # 滾動到按鈕位置
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(0.5)  # 等待滾動完成
                
                # 使用 JavaScript 點擊按鈕
                self.driver.execute_script("arguments[0].click();", next_button)
                print("已點擊完成訂票按鈕")
                
                time.sleep(0.5)
            except Exception as e:
                print(f"尋找或點擊完成訂票按鈕時發生錯誤：{str(e)}")

            try:
                # 選擇付款方式
                payment_select = self.driver.find_element(By.NAME, "paymentMethod")
                select_element = Select(payment_select)
                select_element.select_by_value("ONSITE")  # 選擇車站窗口/超商/郵局付款
                time.sleep(0.5)  # 短暫等待確保選項被選中
                
                # 使用多種方式嘗試找到下一步按鈕
                try:
                    # 方法1：使用完整的 CSS 選擇器
                    next_step_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'][title='下一步：付款/取票資訊']")
                except:
                    try:
                        # 方法2：使用部分 class 名稱
                        next_step_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-3d")
                    except:
                        # 方法3：使用 XPath
                        next_step_button = self.driver.find_element(By.XPATH, "//button[contains(text(), '下一步')]")
                
                # 使用 JavaScript 點擊按鈕
                self.driver.execute_script("arguments[0].click();", next_step_button)
                time.sleep(0.5)  # 等待0.5秒確保操作完成
                
            except Exception as e:
                print(f"選擇付款方式時發生錯誤：{str(e)}")

        except Exception as e:
            print(f"訂票過程發生錯誤：{str(e)}")
            
    def run(self):
        self.root.mainloop()

    def update_child_ticket_options(self, event=None):
        """更新兒童票數的可選擇數量，不得超過總票數"""
        total_tickets = int(self.ticket_count.get())
        # 更新童票的可選擇數量（從0到總票數）
        self.child_ticket_count['values'] = [str(i) for i in range(total_tickets + 1)]
        # 如果目前選擇的兒童票數超過新的總票數，則重設為0
        if int(self.child_ticket_count.get()) > total_tickets:
            self.child_ticket_count.set("0")

    def save_data(self, slot):
        # 儲存當前輸入的資料
        current_data = {
            "id": self.actual_id,  # 儲存實際的身分證字號
            "from_station": self.from_station.get(),
            "to_station": self.to_station.get(),
            "date": self.date_entry.get(),
            "train_number": self.train_number.get(),
            "ticket_count": self.ticket_count.get(),
            "child_ticket_count": self.child_ticket_count.get()
        }
        
        self.saved_data[slot] = current_data
        
        # 儲存到檔案
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.saved_data, f, ensure_ascii=False, indent=2)
            # 更新狀態標籤樣式
            self.status_label.configure(text=f"✓ 已成功儲存至區域 {slot[-1]}", 
                                      foreground="green")
            self.root.after(2000, lambda: self.status_label.configure(text=""))
        except Exception as e:
            self.status_label.configure(text="⚠ 儲存失敗！", 
                                      foreground="red")
            print(f"儲存資料時發生錯誤：{str(e)}")

    def load_data(self, slot):
        # 載入選擇的儲存區資料
        if slot in self.saved_data and self.saved_data[slot]:
            data = self.saved_data[slot]
            self.actual_id = data.get("id", "")  # 載入實際的身分證字號
            self.id_entry.delete(0, tk.END)
            if self.actual_id:
                masked = self.actual_id[:2] + '*' * (len(self.actual_id)-4) + self.actual_id[-2:]
                self.id_entry.insert(0, masked)
            
            self.from_station.delete(0, tk.END)
            self.from_station.insert(0, data.get("from_station", ""))
            
            self.to_station.delete(0, tk.END)
            self.to_station.insert(0, data.get("to_station", ""))
            
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, data.get("date", ""))
            
            self.train_number.delete(0, tk.END)
            self.train_number.insert(0, data.get("train_number", ""))
            
            # 先設定總票數
            self.ticket_count.set(data.get("ticket_count", "1"))
            # 更新兒童票可選擇數量
            self.update_child_ticket_options()
            # 再設定兒童票數
            self.child_ticket_count.set(data.get("child_ticket_count", "0"))
            
            self.status_label.configure(text=f"✓ 已載入區域 {slot[-1]} 的資料", 
                                      foreground="green")
            self.root.after(2000, lambda: self.status_label.configure(text=""))
        else:
            self.status_label.configure(text=f"⚠ 區域 {slot[-1]} 沒有儲存的資料", 
                                      foreground="red")
            self.root.after(2000, lambda: self.status_label.configure(text=""))

    def swap_stations(self):
        """交換出發站和抵達站的內容"""
        from_value = self.from_station.get()
        to_value = self.to_station.get()
        
        self.from_station.delete(0, tk.END)
        self.from_station.insert(0, to_value)
        
        self.to_station.delete(0, tk.END)
        self.to_station.insert(0, from_value)

    def mask_id_number(self, event=None):
        """遮蔽身分證字號，只顯示前後兩位"""
        current = self.id_entry.get()
        if current != self.actual_id:  # 防止重複處理
            self.actual_id = current
            if len(current) > 4:
                masked = current[:2] + '*' * (len(current)-4) + current[-2:]
                self.id_entry.delete(0, tk.END)
                self.id_entry.insert(0, masked)

if __name__ == "__main__":
    bot = TurboTicket()
    bot.run()