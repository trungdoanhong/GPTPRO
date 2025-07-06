# 🚨 Hướng dẫn fix lỗi ChromeDriver

## Nếu gặp lỗi: `[WinError 193] %1 is not a valid Win32 application`

### ⚡ Cách nhanh nhất:
```bash
python fix_chromedriver.py
```

### 🔧 Hoặc chạy lệnh sau:
```bash
# 1. Xóa cache cũ
rmdir /s "%USERPROFILE%\.wdm"

# 2. Chạy script fix
python fix_chromedriver.py

# 3. Khởi động lại Command Prompt
```

### 🪟 Hoặc dùng batch script:
```bash
install_chromedriver.bat
```

---

## Nguyên nhân lỗi:
- webdriver-manager tải xuống phiên bản ChromeDriver sai kiến trúc (win32 thay vì win64)
- Cache cũ chứa driver không tương thích
- Phiên bản ChromeDriver không khớp với Chrome
- User-data-dir đang được Chrome khác sử dụng
- Xung đột profile giữa Chrome chính và automation

## Cách fix:
1. **Tự động**: Chạy `python fix_chromedriver.py`
2. **Thủ công**: Xóa cache và tải lại ChromeDriver đúng phiên bản
3. **Batch**: Chạy `install_chromedriver.bat` (Windows)

## Sau khi fix:
- Khởi động lại Command Prompt
- Chạy lại `python chatgpt_automation.py`
- Nếu vẫn lỗi, liên hệ để được hỗ trợ

---

## 💡 Mẹo:
- Luôn sử dụng phiên bản Chrome mới nhất
- Đảm bảo kết nối internet ổn định khi tải ChromeDriver
- Kiểm tra antivirus có chặn ChromeDriver không
- Chương trình tự động tạo profile riêng để tránh xung đột
- Headless mode giúp chạy nhanh hơn và ít tốn tài nguyên
- Cookies/login sẽ được copy từ Chrome chính (nếu có) 