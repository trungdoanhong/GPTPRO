#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script để kiểm tra ChromeDriver hoạt động
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_webdriver():
    """Test cơ bản WebDriver"""
    print("🧪 Test 1: Kiểm tra WebDriver cơ bản")
    
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Thử với webdriver-manager
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print("   ✅ WebDriver với webdriver-manager: OK")
        except Exception as e:
            print(f"   ❌ WebDriver với webdriver-manager: {e}")
            # Thử với driver mặc định
            driver = webdriver.Chrome(options=options)
            print("   ✅ WebDriver mặc định: OK")
        
        # Test truy cập Google
        driver.get("https://www.google.com")
        title = driver.title
        print(f"   ✅ Truy cập Google: {title}")
        
        # Test tìm element
        search_box = driver.find_element(By.NAME, "q")
        print("   ✅ Tìm element: OK")
        
        driver.quit()
        print("   ✅ Đóng browser: OK")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        return False

def test_chatgpt_access():
    """Test truy cập ChatGPT"""
    print("\n🧪 Test 2: Kiểm tra truy cập ChatGPT")
    
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Thử với webdriver-manager
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception:
            driver = webdriver.Chrome(options=options)
        
        print("   📝 Đang truy cập ChatGPT...")
        driver.get("https://chatgpt.com")
        
        # Đợi trang load
        time.sleep(5)
        
        title = driver.title
        print(f"   ✅ Truy cập ChatGPT: {title}")
        
        # Kiểm tra có blocked không
        if "blocked" in title.lower() or "access denied" in title.lower():
            print("   ⚠️ ChatGPT có thể bị blocked")
        else:
            print("   ✅ ChatGPT truy cập được")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        return False

def test_selenium_features():
    """Test các tính năng Selenium"""
    print("\n🧪 Test 3: Kiểm tra tính năng Selenium")
    
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Thử với webdriver-manager
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception:
            driver = webdriver.Chrome(options=options)
        
        # Test JavaScript
        driver.get("https://www.google.com")
        result = driver.execute_script("return document.title")
        print(f"   ✅ JavaScript: {result}")
        
        # Test tìm element theo XPath
        try:
            element = driver.find_element(By.XPATH, "//input[@name='q']")
            print("   ✅ XPath selector: OK")
        except Exception:
            print("   ❌ XPath selector: Lỗi")
        
        # Test nhập text
        try:
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys("test")
            print("   ✅ Nhập text: OK")
        except Exception:
            print("   ❌ Nhập text: Lỗi")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        return False

def main():
    """Chạy tất cả tests"""
    print("🚀 ChromeDriver Test Suite")
    print("=" * 40)
    
    results = []
    
    # Test 1: WebDriver cơ bản
    results.append(test_basic_webdriver())
    
    # Test 2: ChatGPT access
    results.append(test_chatgpt_access())
    
    # Test 3: Selenium features
    results.append(test_selenium_features())
    
    # Kết quả
    print("\n📊 Kết quả:")
    print("=" * 40)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 Tất cả tests đều PASS!")
        print("   ChromeDriver đã sẵn sàng cho ChatGPT automation.")
    else:
        print("\n⚠️ Một số tests FAILED!")
        print("   Vui lòng chạy fix_chromedriver.py để khắc phục.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 