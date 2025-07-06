#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cách sử dụng đơn giản nhất cho ChatGPT Automation
"""

from chatgpt_automation import ChatGPTAutomation

def main():
    # Câu hỏi mặc định
    question = "Xin chào! Bạn có thể giải thích về Python không?"
    
    # Cho phép người dùng tùy chỉnh câu hỏi
    user_input = input(f"Câu hỏi (Enter để dùng câu hỏi mặc định): ")
    if user_input.strip():
        question = user_input.strip()
    
    print(f"\n📝 Câu hỏi: {question}")
    print("🚀 Đang khởi động ChatGPT automation...")
    
    # Tạo instance và chạy
    chatgpt = ChatGPTAutomation(headless=True)
    
    try:
        # Chạy automation
        response = chatgpt.run_automation(question)
        
        if response:
            print("\n" + "="*50)
            print("🤖 PHẢN HỒI TỪ CHATGPT:")
            print("="*50)
            print(response)
            print("="*50)
            print("\n📋 Đã copy câu trả lời vào clipboard!")
            
            # Lưu vào file
            with open("chatgpt_response.txt", "w", encoding="utf-8") as f:
                f.write(f"Câu hỏi: {question}\n\n")
                f.write(f"Trả lời: {response}\n")
            print("💾 Đã lưu vào file: chatgpt_response.txt")
            
        else:
            print("❌ Không thể lấy phản hồi từ ChatGPT")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("💡 Thử chạy: python fix_chromedriver.py")
    finally:
        chatgpt.close()

if __name__ == "__main__":
    main() 