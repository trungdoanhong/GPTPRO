# ChatGPT Automation với Selenium

Chương trình Python tự động truy cập ChatGPT, chọn mô hình GPT-4o, đặt câu hỏi và copy câu trả lời.

## Yêu cầu hệ thống

- Python 3.7+
- Google Chrome browser
- Kết nối internet

## Cài đặt

1. Cài đặt các package cần thiết:
```bash
pip install -r requirements.txt
```

2. Đảm bảo Google Chrome đã được cài đặt trên máy tính.

3. Kiểm tra ChromeDriver hoạt động:
```bash
python test_chromedriver.py
```

4. Nếu có lỗi ChromeDriver, chạy:
```bash
python fix_chromedriver.py
```

## Sử dụng

### Cách đơn giản nhất:
```bash
python simple.py
```

### Chạy với demo menu:
```bash
python demo.py
```

### Chạy chương trình chính (headless):
```bash
python chatgpt_automation.py   # Mặc định chạy headless và tái sử dụng cache đăng nhập Chrome
```

### Tùy chỉnh câu hỏi:
Mở file `chatgpt_automation.py` và thay đổi biến `QUESTION` trong hàm `main()`:
```python
QUESTION = "Câu hỏi của bạn ở đây"
```

### Tuỳ chỉnh headless & profile
```python
from chatgpt_automation import ChatGPTAutomation

# Chạy headless, sử dụng profile 'Default' và user-data-dir mặc định (đã đăng nhập sẵn)
bot = ChatGPTAutomation()

# Hoặc chỉ định thư mục profile cụ thể
bot = ChatGPTAutomation(user_data_dir=r"C:\Users\YOU\AppData\Local\Google\Chrome\User Data", profile_directory="Profile 1")
```

## Danh sách file

- `simple.py` - Cách sử dụng đơn giản nhất ⭐
- `chatgpt_automation.py` - Chương trình chính
- `demo.py` - Script demo với menu tương tác
- `test_chromedriver.py` - Kiểm tra ChromeDriver hoạt động
- `fix_chromedriver.py` - Tự động fix lỗi ChromeDriver
- `install_chromedriver.bat` - Batch script cài ChromeDriver (Windows)
- `requirements.txt` - Danh sách dependencies
- `README.md` - Hướng dẫn chi tiết
- `QUICK_FIX.md` - Hướng dẫn fix lỗi nhanh

## Tính năng

- ✅ Tự động mở ChatGPT
- ✅ Xử lý đăng nhập (hỗ trợ đăng nhập thủ công)
 - ✅ Tự động chọn mô hình GPT-4o
- ✅ Gửi câu hỏi tự động
- ✅ Đợi phản hồi từ ChatGPT
- ✅ Lấy câu trả lời và copy vào clipboard
- ✅ Logging chi tiết
- ✅ Xử lý lỗi robust
- ✅ Tự động fix lỗi ChromeDriver
- ✅ Nhiều fallback methods cho WebDriver

## Sử dụng nâng cao

### Tạo instance và sử dụng:
```python
from chatgpt_automation import ChatGPTAutomation

# Tạo instance
chatgpt = ChatGPTAutomation(headless=False)

# Chạy automation
response = chatgpt.run_automation("Bạn có thể giải thích về AI không?")

# In kết quả
print(response)

# Đóng browser
chatgpt.close()
```

### Chạy nhiều câu hỏi:
```python
questions = [
    "Giới thiệu về Python",
    "Selenium là gì?",
    "Cách tối ưu hóa code Python"
]

chatgpt = ChatGPTAutomation()

for question in questions:
    response = chatgpt.run_automation(question)
    print(f"Câu hỏi: {question}")
    print(f"Trả lời: {response}\n")
    
chatgpt.close()
```

## Lưu ý quan trọng

1. **Headless Mode**: Chương trình mặc định chạy headless (không hiển thị UI) để tối ưu hiệu suất.

2. **Profile Riêng**: Tự động tạo thư mục profile riêng cho automation để tránh xung đột với Chrome đang chạy.

3. **Đăng nhập**: Chương trình sẽ copy cookies/login từ Chrome chính, hoặc yêu cầu đăng nhập nếu cần.

4. **Mô hình GPT-4o**: Nếu không tìm thấy mô hình GPT-4o, chương trình sẽ sử dụng mô hình mặc định.

5. **Rate limiting**: Tránh gửi quá nhiều request trong thời gian ngắn để tránh bị giới hạn.

6. **Chrome driver**: Chương trình sẽ tự động tải ChromeDriver phù hợp với nhiều fallback methods.

## Xử lý lỗi

- Nếu không tìm thấy element, chương trình sẽ thử nhiều selector khác nhau
- Timeout được thiết lập 60 giây cho mỗi phản hồi
- Logging chi tiết giúp debug

## Kết quả

Câu trả lời từ ChatGPT sẽ được:
- In ra console
- Copy vào clipboard
- Trả về dưới dạng string

## Cấu hình

Có thể tùy chỉnh các thông số trong class `ChatGPTAutomation`:

- `headless`: Chạy ẩn browser
- `timeout`: Thời gian chờ phản hồi
- `wait_time`: Thời gian chờ giữa các thao tác

## Xử lý lỗi ChromeDriver

Nếu gặp lỗi `[WinError 193] %1 is not a valid Win32 application` hoặc các lỗi ChromeDriver khác:

### Cách 1: Sử dụng script tự động fix
```bash
python fix_chromedriver.py
```

### Cách 2: Sử dụng batch script (Windows)
```bash
install_chromedriver.bat
```

### Cách 3: Xử lý thủ công
1. Xóa cache webdriver-manager:
   ```bash
   # Windows
   rmdir /s "%USERPROFILE%\.wdm"
   
   # Linux/Mac
   rm -rf ~/.wdm
   ```

2. Tải ChromeDriver thủ công từ [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)

3. Giải nén và thêm vào PATH

## Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra Chrome đã cài đặt
2. Chạy `python fix_chromedriver.py` để tự động fix lỗi ChromeDriver
3. Kiểm tra kết nối internet
4. Xem log để debug
5. Đảm bảo ChatGPT có thể truy cập từ trình duyệt thông thường 