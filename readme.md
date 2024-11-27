<div align="center">

# 🚂 TurboTicket Assistant

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*快速便利的訂票助手！*

[功能特點](#功能特點) • [系統需求](#系統需求) • [安裝指南](#安裝指南) • [使用說明](#使用說明) • [注意事項](#注意事項)

</div>

---

## ✨ 功能特點

- 🖥️ 直覺的圖形化使用者介面
- 📝 智能自動填寫訂票資訊
- 🔒 身分證字號安全遮蔽功能
- ⚡ 支援快速訂票模式
- 💾 支援儲存/載入常用訂票資訊
- 💳 自動選擇付款方式
- 🔔 即時操作提示和錯誤訊息

## 🛠️ 系統需求

- Python 3.x
- Chrome 瀏覽器
- ChromeDriver

## 📦 安裝指南

1. 克隆專案到本地：
```bash
git clone https://github.com/yourusername/turbo-ticket-assistant.git
```

2. 安裝必要套件：
```bash
pip install selenium
```

## 📖 使用說明

### 基本操作流程

1. 執行程式後，點擊「開啟網頁」按鈕
2. 完成「我不是機器人」驗證
3. 切換至「快速」訂票模式
4. 填寫訂票資訊：
   - 👤 身分證字號
   - 🚉 起點站
   - 🏁 終點站
   - 📅 乘車日期 (YYYY/MM/DD)
   - 🚂 車次
   - 🎫 訂票張數
5. 點擊「開始訂票」按鈕

### 資料安全功能

- 🔒 身分證字號輸入時自動遮蔽中間位數
- 💾 儲存資料時保持完整資訊
- 👁️ 載入資料時自動套用遮蔽保護
- 🔐 實際訂票時使用完整身分證字號

## ⚠️ 注意事項

- ✅ 使用前請確保網路連線正常
- ✅ 請確實完成人機驗證
- ✅ 日期格式必須為 YYYY/MM/DD
- ✅ 身分證字號會自動遮蔽保護隱私
- ❌ 訂票過程中請勿手動操作網頁
- 💡 付款方式預設為超商/郵局取票

## ❗ 錯誤處理

程式會顯示以下錯誤訊息：
- 🔄 網頁載入超時
- 🖱️ 元素無法點擊
- ⌨️ 資料填寫錯誤

## 👨‍💻 開發者資訊

本程式使用 MIT 授權條款，歡迎協助改進程式碼。
如有任何問題或建議，請[提出 Issue](https://github.com/yourusername/turbo-ticket-assistant/issues)。

## 📜 免責聲明

本程式僅供學習交流使用，請勿用於商業用途。使用者需遵守相關規定，開發者不對使用過程中造成的任何損失負責。

---

<div align="center">

Made with ❤️ by [BB]

</div>
