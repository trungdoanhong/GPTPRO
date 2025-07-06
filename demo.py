#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script cho ChatGPT Automation
"""

from chatgpt_automation import ChatGPTAutomation

def demo_single_question():
    """Demo với một câu hỏi"""
    print("=== DEMO: Một câu hỏi ===")
    
    # Tạo instance
    chatgpt = ChatGPTAutomation(headless=True)
    
    try:
        # Câu hỏi demo
        question = "Bạn có thể giải thích ngắn gọn về machine learning không?"
        
        # Chạy automation  
        response = chatgpt.run_automation(question)
        
        if response:
            print(f"\n✅ Thành công!")
            print(f"📝 Câu hỏi: {question}")
            print(f"🤖 Trả lời: {response[:200]}...")
            print(f"📋 Đã copy vào clipboard!")
        else:
            print("❌ Không thể lấy phản hồi")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
    finally:
        chatgpt.close()

def demo_multiple_questions():
    """Demo với nhiều câu hỏi"""
    print("\n=== DEMO: Nhiều câu hỏi ===")
    
    questions = [
        "Python là gì?",
        "Selenium dùng để làm gì?",
        "AI có thể thay thế lập trình viên không?"
    ]
    
    # Tạo instance
    chatgpt = ChatGPTAutomation(headless=True)
    
    try:
        for i, question in enumerate(questions, 1):
            print(f"\n📝 Câu hỏi {i}/{len(questions)}: {question}")
            
            response = chatgpt.run_automation(question)
            
            if response:
                print(f"✅ Thành công: {response[:100]}...")
            else:
                print("❌ Không thể lấy phản hồi")
                
            # Đợi một chút giữa các câu hỏi
            if i < len(questions):
                print("⏳ Đang chờ...")
                import time
                time.sleep(3)
                
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
    finally:
        chatgpt.close()

def demo_custom_question():
    """Demo với câu hỏi tùy chỉnh"""
    print("\n=== DEMO: Câu hỏi tùy chỉnh ===")
    
    # Nhập câu hỏi từ người dùng
    question = input("Nhập câu hỏi của bạn: ")
    
    if not question.strip():
        print("❌ Câu hỏi không được để trống")
        return
    
    # Tạo instance
    chatgpt = ChatGPTAutomation(headless=True)
    
    try:
        response = chatgpt.run_automation(question)
        
        if response:
            print(f"\n✅ Thành công!")
            print(f"📝 Câu hỏi: {question}")
            print(f"🤖 Trả lời: {response}")
            print(f"📋 Đã copy vào clipboard!")
        else:
            print("❌ Không thể lấy phản hồi")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
    finally:
        chatgpt.close()

def main():
    """Hàm main để chạy demo"""
    print("🚀 ChatGPT Automation Demo")
    print("=" * 40)
    
    while True:
        print("\nChọn demo:")
        print("1. Một câu hỏi đơn giản")
        print("2. Nhiều câu hỏi")
        print("3. Câu hỏi tùy chỉnh")
        print("4. Thoát")
        
        choice = input("\nNhập lựa chọn (1-4): ").strip()
        
        if choice == "1":
            demo_single_question()
        elif choice == "2":
            demo_multiple_questions()
        elif choice == "3":
            demo_custom_question()
        elif choice == "4":
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main() 