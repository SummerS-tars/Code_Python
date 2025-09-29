#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
prompt1: please help me develop an easy program, 
which can take the user input(year as number, e.g. 2025) 
and then output happy new year in the form like "二零二五年新年快乐"

prompt2: please help me improve the program to 
enable it to handle more abnormal or incorrect input

改进内容:
1. 增强输入验证 - 检查空输入、非数字字符、年份范围(1-9999)
2. 自动处理前导零和空白字符
3. 支持多次重试输入 (最多3次)
4. 更详细的错误提示信息
5. 添加测试模式来验证各种输入场景
6. 增强异常处理和错误恢复机制
7. 改进用户体验，提供清晰的操作指导
"""

"""
新年祝福程序
接受用户输入的年份数字，输出中文形式的新年祝福
"""

def number_to_chinese(year_str):
    """
    将数字字符串转换为中文数字
    例如: "2025" -> "二零二五"
    """
    # 验证输入
    if not isinstance(year_str, str):
        raise TypeError("输入必须是字符串类型")
    
    if not year_str:
        raise ValueError("输入字符串不能为空")
    
    chinese_digits = {
        '0': '零',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九'
    }
    
    chinese_year = ""
    for i, digit in enumerate(year_str):
        if digit not in chinese_digits:
            raise ValueError(f"在位置{i+1}发现无效字符'{digit}'，只允许数字0-9")
        chinese_year += chinese_digits[digit]
    
    return chinese_year

def validate_year(year_input):
    """
    验证年份输入的有效性
    返回: (is_valid, cleaned_year, error_message)
    """
    # 去除前后空白字符
    year_input = year_input.strip()
    
    # 检查是否为空
    if not year_input:
        return False, "", "输入不能为空"
    
    # 移除可能的前导零（除了全为零的情况）
    year_input = year_input.lstrip('0') or '0'
    
    # 检查是否包含非数字字符
    if not year_input.isdigit():
        return False, "", "输入包含非数字字符"
    
    # 转换为整数进行范围检查
    try:
        year_int = int(year_input)
    except ValueError:
        return False, "", "无法转换为有效数字"
    
    # 检查年份范围（合理的年份范围）
    if year_int < 1:
        return False, "", "年份必须大于0"
    elif year_int > 9999:
        return False, "", "年份不能超过9999"
    
    # 补齐到4位数（用于显示）
    formatted_year = str(year_int).zfill(4)
    
    return True, formatted_year, ""

def get_year_input():
    """
    获取用户输入的年份，支持多次重试
    """
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        try:
            year_input = input(f"请输入年份（例如：2025）[第{attempt + 1}/{max_attempts}次尝试]: ")
            
            is_valid, cleaned_year, error_msg = validate_year(year_input)
            
            if is_valid:
                return cleaned_year
            else:
                print(f"❌ 输入错误: {error_msg}")
                if attempt < max_attempts - 1:
                    print("💡 提示：请输入1-9999之间的数字年份")
                attempt += 1
        
        except EOFError:
            print("\n❌ 检测到输入结束，程序退出")
            return None
        except KeyboardInterrupt:
            print("\n👋 用户中断程序")
            return None
    
    print(f"❌ 已达到最大尝试次数({max_attempts})，程序退出")
    return None

def main():
    """主程序"""
    print("🎉 新年祝福程序 🎉")
    print("=" * 30)
    print("💡 支持输入1-9999之间的年份数字")
    print("💡 程序会自动处理前导零和空白字符")
    print("=" * 30)
    
    try:
        # 获取有效的年份输入
        year = get_year_input()
        
        if year is None:
            print("😢 未能获取有效输入，程序结束")
            return
        
        # 转换为中文数字
        try:
            chinese_year = number_to_chinese(year)
        except Exception as e:
            print(f"❌ 转换中文数字时发生错误: {e}")
            return
        
        # 输出新年祝福
        greeting = f"{chinese_year}年新年快乐！"
        print(f"\n🎊 {greeting} 🎊")
        print("🧧 祝您新年快乐，万事如意！🧧")
        
        # 显示原始输入和格式化后的年份
        if year != year.lstrip('0'):
            print(f"📋 格式化后的年份: {year}")
        
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出，祝您新年快乐！")
    except Exception as e:
        print(f"❌ 程序运行时发生未预期的错误: {e}")
        print("🔧 请检查程序代码或联系开发者")

def test_program():
    """
    测试程序的各种输入场景
    """
    test_cases = [
        ("2025", "正常4位年份"),
        ("25", "2位年份"),
        ("0025", "带前导零的年份"),
        ("999", "3位年份"),
        (" 2025 ", "带空白字符的年份"),
        ("", "空输入"),
        ("abc", "字母输入"),
        ("20abc", "混合字符"),
        ("0", "零"),
        ("10000", "超出范围的年份"),
        ("-2025", "负数"),
    ]
    
    print("\n🧪 测试模式 - 各种输入场景:")
    print("=" * 40)
    
    for test_input, description in test_cases:
        print(f"\n测试: {description}")
        print(f"输入: '{test_input}'")
        
        is_valid, cleaned_year, error_msg = validate_year(test_input)
        
        if is_valid:
            try:
                chinese_year = number_to_chinese(cleaned_year)
                print(f"✅ 结果: {chinese_year}年新年快乐！")
            except Exception as e:
                print(f"❌ 转换错误: {e}")
        else:
            print(f"❌ 验证失败: {error_msg}")

if __name__ == "__main__":
    import sys
    
    # 检查是否有命令行参数用于测试
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_program()
    else:
        main()

