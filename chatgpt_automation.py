import time
import os
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChatGPTAutomation:
    def __init__(self, headless=True, user_data_dir: str | None = None, profile_directory: str | None = "Default"):
        """
        Khởi tạo ChatGPT Automation
        
        Args:
            headless (bool): Chạy browser ẩn hay hiển thị
            user_data_dir (str | None): Đường dẫn đến thư mục user-data của Chrome
            profile_directory (str | None): Tên của profile để sử dụng
        """
        self.driver = None
        self.wait = None
        self.headless = headless
        self.user_data_dir = user_data_dir or self._get_default_user_data_dir()
        self.profile_directory = profile_directory
        self.setup_driver()
    
    def _get_default_user_data_dir(self):
        """Trả về đường dẫn user-data-dir riêng cho automation."""
        # Tạo thư mục riêng cho automation để tránh xung đột
        if os.name == "nt":  # Windows
            base_dir = os.path.expandvars(r"%LOCALAPPDATA%\\Google\\Chrome\\User Data")
            automation_dir = os.path.join(os.path.dirname(base_dir), "Chrome-Automation")
        else:
            # Linux / macOS
            automation_dir = os.path.expanduser("~/.config/google-chrome-automation")
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(automation_dir, exist_ok=True)
        
        # Copy một số file cần thiết từ profile chính (nếu có)
        self._copy_essential_profile_data(automation_dir)
        
        return automation_dir
    
    def _copy_essential_profile_data(self, automation_dir):
        """Tạo profile cơ bản cho automation (không copy từ Chrome chính để tránh lỗi encryption)."""
        try:
            target_dir = os.path.join(automation_dir, "Default")
            os.makedirs(target_dir, exist_ok=True)
            
            # Tạo file Preferences cơ bản
            preferences = {
                "profile": {
                    "default_content_setting_values": {
                        "notifications": 2,
                        "geolocation": 2,
                        "media_stream": 2
                    },
                    "password_manager_enabled": False,
                    "content_settings": {
                        "exceptions": {}
                    }
                },
                "browser": {
                    "check_default_browser": False
                },
                "distribution": {
                    "skip_first_run_ui": True
                }
            }
            
            import json
            preferences_file = os.path.join(target_dir, "Preferences")
            with open(preferences_file, "w", encoding="utf-8") as f:
                json.dump(preferences, f, indent=2)
            
            logger.info("Đã tạo profile automation cơ bản")
            
            # Tạo Local State cơ bản
            local_state = {
                "browser": {
                    "enabled_labs_experiments": []
                },
                "profile": {
                    "info_cache": {
                        "Default": {
                            "name": "Person 1",
                            "user_name": "Person 1"
                        }
                    }
                }
            }
            
            local_state_file = os.path.join(automation_dir, "Local State")
            with open(local_state_file, "w", encoding="utf-8") as f:
                json.dump(local_state, f, indent=2)
            
            logger.info("Đã tạo Local State cơ bản")
                    
        except Exception as e:
            logger.warning(f"Lỗi khi tạo profile data: {e}")
    
    def clear_webdriver_cache(self):
        """Xóa cache của webdriver-manager"""
        try:
            import shutil
            cache_dir = os.path.join(os.path.expanduser("~"), ".wdm")
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                logger.info("Đã xóa cache webdriver-manager")
        except Exception as e:
            logger.warning(f"Không thể xóa cache webdriver-manager: {str(e)}")
    
    def setup_driver(self):
        """Thiết lập Chrome WebDriver"""
        try:
            chrome_options = Options()
            if self.headless:
                # Sử dụng headless new để tương thích phiên bản mới
                chrome_options.add_argument("--headless=new")
            
            # Sử dụng profile / cache cũ để giữ đăng nhập
            if self.user_data_dir and os.path.exists(self.user_data_dir):
                chrome_options.add_argument(f"--user-data-dir={self.user_data_dir}")
                if self.profile_directory:
                    chrome_options.add_argument(f"--profile-directory={self.profile_directory}")
            
            # Các tùy chọn để tránh bị phát hiện
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent để tránh bị phát hiện
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Thử nhiều cách khởi tạo WebDriver
            self.driver = None
            
            # Cách 1: Sử dụng webdriver-manager
            try:
                logger.info("Đang tải ChromeDriver...")
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("WebDriver đã được khởi tạo thành công với webdriver-manager")
                
            except Exception as e1:
                logger.warning(f"Không thể sử dụng webdriver-manager: {str(e1)}")
                
                # Nếu lỗi liên quan đến kiến trúc, thử xóa cache và tải lại
                if "Win32" in str(e1) or "WinError 193" in str(e1):
                    logger.info("Phát hiện lỗi kiến trúc, đang xóa cache và thử lại...")
                    self.clear_webdriver_cache()
                    
                    try:
                        service = Service(ChromeDriverManager().install())
                        self.driver = webdriver.Chrome(service=service, options=chrome_options)
                        logger.info("WebDriver đã được khởi tạo thành công sau khi xóa cache")
                    except Exception as e_retry:
                        logger.warning(f"Vẫn không thể sử dụng webdriver-manager sau khi xóa cache: {str(e_retry)}")
                
                # Cách 2: Thử sử dụng Chrome driver mặc định
                if not self.driver:
                    try:
                        self.driver = webdriver.Chrome(options=chrome_options)
                        logger.info("WebDriver đã được khởi tạo thành công với Chrome driver mặc định")
                        
                    except Exception as e2:
                        logger.error(f"Không thể khởi tạo Chrome driver mặc định: {str(e2)}")
                        
                        # Nếu lỗi user-data-dir, thử không dùng user-data-dir
                        if "user data directory is already in use" in str(e2).lower():
                            logger.info("Thử khởi tạo Chrome mà không dùng user-data-dir...")
                            try:
                                # Tạo options mới không có user-data-dir
                                clean_options = Options()
                                if self.headless:
                                    clean_options.add_argument("--headless=new")
                                
                                clean_options.add_argument("--no-sandbox")
                                clean_options.add_argument("--disable-dev-shm-usage")
                                clean_options.add_argument("--disable-blink-features=AutomationControlled")
                                clean_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                                clean_options.add_experimental_option('useAutomationExtension', False)
                                clean_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                                
                                self.driver = webdriver.Chrome(options=clean_options)
                                logger.info("WebDriver đã được khởi tạo thành công mà không dùng user-data-dir")
                                
                            except Exception as e_clean:
                                logger.error(f"Không thể khởi tạo Chrome mà không dùng user-data-dir: {str(e_clean)}")
                        
                        # Cách 3: Thử với đường dẫn cụ thể
                        if not self.driver:
                            try:
                                # Tìm Chrome executable
                                chrome_paths = [
                                    "C:/Program Files/Google/Chrome/Application/chrome.exe",
                                    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
                                    "C:/Users/{}/AppData/Local/Google/Chrome/Application/chrome.exe".format(os.environ.get('USERNAME', ''))
                                ]
                                
                                for chrome_path in chrome_paths:
                                    if os.path.exists(chrome_path):
                                        chrome_options.binary_location = chrome_path
                                        break
                                
                                self.driver = webdriver.Chrome(options=chrome_options)
                                logger.info("WebDriver đã được khởi tạo thành công với đường dẫn cụ thể")
                                
                            except Exception as e3:
                                logger.error(f"Tất cả các cách khởi tạo WebDriver đều thất bại")
                                logger.error(f"Lỗi cuối cùng: {str(e3)}")
                                
                                # Cách cuối: Thử tạo user-data-dir với timestamp unique
                                try:
                                    import time
                                    import tempfile
                                    temp_dir = tempfile.mkdtemp(prefix="chrome_automation_")
                                    
                                    unique_options = Options()
                                    if self.headless:
                                        unique_options.add_argument("--headless=new")
                                    
                                    unique_options.add_argument(f"--user-data-dir={temp_dir}")
                                    unique_options.add_argument("--no-sandbox")
                                    unique_options.add_argument("--disable-dev-shm-usage")
                                    unique_options.add_argument("--disable-blink-features=AutomationControlled")
                                    unique_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                                    unique_options.add_experimental_option('useAutomationExtension', False)
                                    unique_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                                    
                                    self.driver = webdriver.Chrome(options=unique_options)
                                    logger.info(f"WebDriver đã được khởi tạo thành công với temp user-data-dir: {temp_dir}")
                                    
                                except Exception as e_final:
                                    logger.error(f"Tất cả các cách khởi tạo WebDriver đều thất bại: {str(e_final)}")
                                    raise Exception("Không thể khởi tạo WebDriver. Vui lòng chạy: python fix_chromedriver.py")
            
            if self.driver:
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.wait = WebDriverWait(self.driver, 20)
                logger.info("WebDriver đã được thiết lập hoàn tất")
            else:
                raise Exception("Không thể khởi tạo WebDriver")
                
        except Exception as e:
            logger.error(f"Lỗi khi khởi tạo WebDriver: {str(e)}")
            raise
    
    def open_chatgpt(self):
        """Mở trang ChatGPT"""
        try:
            logger.info("Đang mở trang ChatGPT...")
            self.driver.get("https://chatgpt.com")
            
            # Đợi trang load
            time.sleep(3)
            logger.info("Đã mở trang ChatGPT thành công")
            
        except Exception as e:
            logger.error(f"Lỗi khi mở trang ChatGPT: {str(e)}")
            raise
    
    def login_if_needed(self):
        """Kiểm tra và đăng nhập nếu cần"""
        try:
            # Kiểm tra xem có cần đăng nhập không
            login_button = None
            try:
                login_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), 'Sign in')]"))
                )
            except TimeoutException:
                logger.info("Không tìm thấy nút đăng nhập, có thể đã đăng nhập")
                return True
            
            if login_button:
                logger.info("Cần đăng nhập. Vui lòng đăng nhập thủ công...")
                login_button.click()
                
                # Đợi người dùng đăng nhập thủ công
                input("Vui lòng đăng nhập vào ChatGPT và nhấn Enter để tiếp tục...")
                
                # Đợi một chút để đảm bảo đã đăng nhập
                time.sleep(5)
                
            return True
            
        except Exception as e:
            logger.error(f"Lỗi trong quá trình đăng nhập: {str(e)}")
            return False
    
    def select_model_o3(self):
        """Chọn mô hình o3"""
        try:
            logger.info("Đang tìm kiếm mô hình o3...")
            
            # Tìm dropdown để chọn mô hình
            model_selectors = [
                "//button[contains(@class, 'model') or contains(@aria-label, 'model')]",
                "//div[contains(@class, 'model-selector')]",
                "//button[contains(text(), 'GPT')]",
                "//div[contains(@class, 'dropdown')]//button",
                "//select[contains(@class, 'model')]"
            ]
            
            model_button = None
            for selector in model_selectors:
                try:
                    model_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logger.info(f"Tìm thấy dropdown mô hình với selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not model_button:
                logger.warning("Không tìm thấy dropdown mô hình. Sử dụng mô hình mặc định.")
                return True
            
            # Click vào dropdown
            model_button.click()
            time.sleep(2)
            
            # Tìm và chọn mô hình o3
            o3_selectors = [
                "//div[contains(text(), 'o3') or contains(text(), 'O3')]",
                "//option[contains(text(), 'o3') or contains(text(), 'O3')]",
                "//li[contains(text(), 'o3') or contains(text(), 'O3')]",
                "//button[contains(text(), 'o3') or contains(text(), 'O3')]"
            ]
            
            o3_option = None
            for selector in o3_selectors:
                try:
                    o3_option = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logger.info(f"Tìm thấy mô hình o3 với selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if o3_option:
                o3_option.click()
                logger.info("Đã chọn mô hình o3 thành công")
                time.sleep(2)
                return True
            else:
                logger.warning("Không tìm thấy mô hình o3. Sử dụng mô hình mặc định.")
                return True
                
        except Exception as e:
            logger.error(f"Lỗi khi chọn mô hình o3: {str(e)}")
            return False
    
    def send_question(self, question):
        """Gửi câu hỏi"""
        try:
            logger.info(f"Đang gửi câu hỏi: {question}")
            
            # Tìm ô input
            input_selectors = [
                "//textarea[contains(@placeholder, 'Message') or contains(@placeholder, 'Send a message')]",
                "//textarea[contains(@class, 'input')]",
                "//div[contains(@contenteditable, 'true')]",
                "//input[contains(@type, 'text')]"
            ]
            
            input_box = None
            for selector in input_selectors:
                try:
                    input_box = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    logger.info(f"Tìm thấy ô input với selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not input_box:
                logger.error("Không tìm thấy ô input")
                return False
            
            # Nhập câu hỏi
            input_box.clear()
            input_box.send_keys(question)
            time.sleep(1)
            
            # Gửi câu hỏi
            input_box.send_keys(Keys.RETURN)
            logger.info("Đã gửi câu hỏi thành công")
            
            return True
            
        except Exception as e:
            logger.error(f"Lỗi khi gửi câu hỏi: {str(e)}")
            return False
    
    def wait_for_response(self, timeout=60):
        """Đợi phản hồi từ ChatGPT"""
        try:
            logger.info("Đang đợi phản hồi từ ChatGPT...")
            
            # Đợi cho đến khi có phản hồi
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    # Kiểm tra xem có đang typing không
                    typing_indicators = [
                        "//div[contains(@class, 'typing')]",
                        "//div[contains(@class, 'loading')]",
                        "//div[contains(@class, 'thinking')]"
                    ]
                    
                    is_typing = False
                    for indicator in typing_indicators:
                        try:
                            self.driver.find_element(By.XPATH, indicator)
                            is_typing = True
                            break
                        except NoSuchElementException:
                            continue
                    
                    if not is_typing:
                        # Đợi thêm một chút để đảm bảo phản hồi hoàn tất
                        time.sleep(3)
                        logger.info("ChatGPT đã hoàn tất phản hồi")
                        return True
                    
                    time.sleep(2)
                    
                except Exception:
                    time.sleep(2)
                    continue
            
            logger.warning("Timeout khi đợi phản hồi")
            return False
            
        except Exception as e:
            logger.error(f"Lỗi khi đợi phản hồi: {str(e)}")
            return False
    
    def get_latest_response(self):
        """Lấy câu trả lời mới nhất"""
        try:
            logger.info("Đang lấy câu trả lời...")
            
            # Tìm tất cả các tin nhắn
            message_selectors = [
                "//div[contains(@class, 'message') and contains(@class, 'assistant')]",
                "//div[contains(@data-message-author-role, 'assistant')]",
                "//div[contains(@class, 'response')]",
                "//div[contains(@class, 'ai-message')]"
            ]
            
            messages = []
            for selector in message_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        messages.extend(elements)
                        logger.info(f"Tìm thấy {len(elements)} tin nhắn với selector: {selector}")
                except Exception:
                    continue
            
            if not messages:
                logger.error("Không tìm thấy tin nhắn nào")
                return None
            
            # Lấy tin nhắn cuối cùng
            latest_message = messages[-1]
            response_text = latest_message.text.strip()
            
            logger.info(f"Đã lấy câu trả lời thành công: {response_text[:100]}...")
            return response_text
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy câu trả lời: {str(e)}")
            return None
    
    def copy_response_to_clipboard(self, response_text):
        """Copy câu trả lời vào clipboard"""
        try:
            if response_text:
                pyperclip.copy(response_text)
                logger.info("Đã copy câu trả lời vào clipboard")
                return True
            else:
                logger.error("Không có câu trả lời để copy")
                return False
                
        except Exception as e:
            logger.error(f"Lỗi khi copy vào clipboard: {str(e)}")
            return False
    
    def run_automation(self, question):
        """Chạy toàn bộ quy trình tự động"""
        try:
            logger.info("Bắt đầu quy trình tự động...")
            
            # Mở ChatGPT
            self.open_chatgpt()
            
            # Đăng nhập nếu cần
            if not self.login_if_needed():
                logger.error("Không thể đăng nhập")
                return None
            
            # Chọn mô hình o3
            self.select_model_o3()
            
            # Gửi câu hỏi
            if not self.send_question(question):
                logger.error("Không thể gửi câu hỏi")
                return None
            
            # Đợi phản hồi
            if not self.wait_for_response():
                logger.error("Không nhận được phản hồi")
                return None
            
            # Lấy câu trả lời
            response = self.get_latest_response()
            if not response:
                logger.error("Không thể lấy câu trả lời")
                return None
            
            # Copy vào clipboard
            self.copy_response_to_clipboard(response)
            
            logger.info("Hoàn tất quy trình tự động!")
            return response
            
        except Exception as e:
            logger.error(f"Lỗi trong quy trình tự động: {str(e)}")
            return None
    
    def close(self):
        """Đóng browser"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Đã đóng browser")
        except Exception as e:
            logger.error(f"Lỗi khi đóng browser: {str(e)}")

def main():
    """Hàm main để chạy chương trình"""
    # Cấu hình
    HEADLESS = True  # Đặt True để chạy ẩn browser
    QUESTION = "Xin chào! Bạn có thể giới thiệu về bản thân không?"
    
    # Tạo instance
    chatgpt = ChatGPTAutomation(headless=HEADLESS)
    
    try:
        # Chạy automation
        response = chatgpt.run_automation(QUESTION)
        
        if response:
            print("\n" + "="*50)
            print("PHẢN HỒI TỪ CHATGPT:")
            print("="*50)
            print(response)
            print("="*50)
            print("\nĐã copy câu trả lời vào clipboard!")
        else:
            print("Không thể lấy phản hồi từ ChatGPT")
            
    except KeyboardInterrupt:
        logger.info("Người dùng dừng chương trình")
    except Exception as e:
        logger.error(f"Lỗi không mong muốn: {str(e)}")
    finally:
        chatgpt.close()

if __name__ == "__main__":
    main() 