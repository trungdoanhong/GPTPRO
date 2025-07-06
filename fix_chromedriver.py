#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để tự động fix lỗi ChromeDriver
"""

import os
import sys
import subprocess
import platform
import requests
import zipfile
import json
import shutil
from pathlib import Path

def get_chrome_version():
    """Lấy phiên bản Chrome hiện tại"""
    try:
        if platform.system() == "Windows":
            # Thử các đường dẫn Chrome thông thường
            chrome_paths = [
                "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
                f"C:/Users/{os.environ.get('USERNAME', '')}/AppData/Local/Google/Chrome/Application/chrome.exe"
            ]
            
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    # Lấy version từ file properties
                    try:
                        import win32api
                        info = win32api.GetFileVersionInfo(chrome_path, "\\")
                        ms = info['FileVersionMS']
                        ls = info['FileVersionLS']
                        version = f"{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}"
                        return version
                    except ImportError:
                        # Nếu không có win32api, dùng subprocess
                        try:
                            result = subprocess.run([chrome_path, "--version"], 
                                                 capture_output=True, text=True, timeout=5)
                            if result.returncode == 0:
                                version = result.stdout.strip().split()[-1]
                                return version
                        except:
                            pass
                        break
                        
        # Thử dùng subprocess cho Linux/Mac
        result = subprocess.run(["google-chrome", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip().split()[-1]
            
    except Exception as e:
        print(f"Không thể lấy phiên bản Chrome: {e}")
        
    return None

def get_compatible_chromedriver_version(chrome_version):
    """Lấy phiên bản ChromeDriver tương thích"""
    try:
        if not chrome_version:
            return None
            
        # Lấy major version
        major_version = chrome_version.split('.')[0]
        
        # API để lấy danh sách ChromeDriver
        url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Tìm phiên bản tương thích
            for version_info in reversed(data['versions']):
                if version_info['version'].startswith(major_version + '.'):
                    downloads = version_info.get('downloads', {})
                    if 'chromedriver' in downloads:
                        return version_info['version']
                        
    except Exception as e:
        print(f"Không thể lấy phiên bản ChromeDriver: {e}")
        
    return None

def download_chromedriver(version, download_dir):
    """Tải xuống ChromeDriver"""
    try:
        system = platform.system().lower()
        arch = "win64" if platform.machine().endswith('64') else "win32"
        
        if system == "windows":
            platform_name = arch
            file_name = f"chromedriver-{platform_name}.zip"
        else:
            platform_name = "linux64" if system == "linux" else "mac64"
            file_name = f"chromedriver-{platform_name}.zip"
            
        url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/{platform_name}/{file_name}"
        
        print(f"Đang tải ChromeDriver {version} cho {platform_name}...")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        zip_path = os.path.join(download_dir, file_name)
        with open(zip_path, 'wb') as f:
            f.write(response.content)
            
        print(f"Đã tải xuống thành công: {zip_path}")
        return zip_path
        
    except Exception as e:
        print(f"Lỗi khi tải ChromeDriver: {e}")
        return None

def extract_chromedriver(zip_path, extract_dir):
    """Giải nén ChromeDriver"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        # Tìm file chromedriver.exe
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.startswith("chromedriver") and (file.endswith(".exe") or not file.endswith(".exe")):
                    chromedriver_path = os.path.join(root, file)
                    print(f"Tìm thấy ChromeDriver: {chromedriver_path}")
                    
                    # Copy về thư mục chính
                    final_path = os.path.join(extract_dir, "chromedriver.exe" if platform.system() == "Windows" else "chromedriver")
                    shutil.copy2(chromedriver_path, final_path)
                    
                    # Cấp quyền thực thi trên Linux/Mac
                    if platform.system() != "Windows":
                        os.chmod(final_path, 0o755)
                        
                    return final_path
                    
        return None
        
    except Exception as e:
        print(f"Lỗi khi giải nén ChromeDriver: {e}")
        return None

def clear_webdriver_cache():
    """Xóa cache của webdriver-manager"""
    try:
        cache_dirs = [
            os.path.join(os.path.expanduser("~"), ".wdm"),
            os.path.join(os.path.expanduser("~"), ".cache", "selenium"),
        ]
        
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                print(f"Đã xóa cache: {cache_dir}")
                
    except Exception as e:
        print(f"Lỗi khi xóa cache: {e}")

def test_chromedriver():
    """Kiểm tra ChromeDriver hoạt động"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ ChromeDriver hoạt động tốt! Tiêu đề trang: {title}")
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver không hoạt động: {e}")
        return False

def main():
    """Hàm main để fix ChromeDriver"""
    print("🔧 ChromeDriver Fix Tool")
    print("=" * 40)
    
    # Kiểm tra Chrome version
    print("1. Kiểm tra phiên bản Chrome...")
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"   ✅ Chrome version: {chrome_version}")
    else:
        print("   ❌ Không tìm thấy Chrome. Vui lòng cài đặt Google Chrome trước.")
        return
    
    # Lấy phiên bản ChromeDriver tương thích
    print("2. Tìm phiên bản ChromeDriver tương thích...")
    driver_version = get_compatible_chromedriver_version(chrome_version)
    if driver_version:
        print(f"   ✅ ChromeDriver version: {driver_version}")
    else:
        print("   ❌ Không tìm thấy phiên bản ChromeDriver tương thích.")
        return
    
    # Xóa cache cũ
    print("3. Xóa cache cũ...")
    clear_webdriver_cache()
    
    # Tạo thư mục tải xuống
    download_dir = os.path.join(os.path.expanduser("~"), "chromedriver_fix")
    os.makedirs(download_dir, exist_ok=True)
    
    # Tải xuống ChromeDriver
    print("4. Tải xuống ChromeDriver...")
    zip_path = download_chromedriver(driver_version, download_dir)
    if not zip_path:
        print("   ❌ Không thể tải xuống ChromeDriver.")
        return
    
    # Giải nén ChromeDriver
    print("5. Giải nén ChromeDriver...")
    chromedriver_path = extract_chromedriver(zip_path, download_dir)
    if not chromedriver_path:
        print("   ❌ Không thể giải nén ChromeDriver.")
        return
    
    print(f"   ✅ ChromeDriver đã được cài đặt: {chromedriver_path}")
    
    # Thêm vào PATH
    print("6. Thêm vào PATH...")
    try:
        current_path = os.environ.get('PATH', '')
        if download_dir not in current_path:
            if platform.system() == "Windows":
                # Windows
                subprocess.run(['setx', 'PATH', f"{current_path};{download_dir}"], check=True)
            else:
                # Linux/Mac
                bashrc_path = os.path.join(os.path.expanduser("~"), ".bashrc")
                with open(bashrc_path, "a") as f:
                    f.write(f"\nexport PATH=$PATH:{download_dir}\n")
                    
            print(f"   ✅ Đã thêm {download_dir} vào PATH")
        else:
            print("   ✅ Đã có trong PATH")
    except Exception as e:
        print(f"   ⚠️ Không thể thêm vào PATH: {e}")
    
    # Test ChromeDriver
    print("7. Kiểm tra ChromeDriver...")
    if test_chromedriver():
        print("\n🎉 ChromeDriver đã được cài đặt và hoạt động tốt!")
        print("   Bạn có thể chạy lại chương trình ChatGPT automation.")
    else:
        print("\n❌ ChromeDriver vẫn chưa hoạt động.")
        print("   Vui lòng khởi động lại Command Prompt và thử lại.")
    
    # Dọn dẹp
    try:
        os.remove(zip_path)
        print(f"\n🧹 Đã dọn dẹp file tạm: {zip_path}")
    except:
        pass

if __name__ == "__main__":
    main() 