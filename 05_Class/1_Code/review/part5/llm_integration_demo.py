"""
示例：大模型开发实战演示

包含演示：
- Ollama本地模型基础调用
- messages结构与角色系统
- 流式响应与推理过程显示
- 问卷自动分析实践案例
- 代码伦理与安全性考虑

运行：
    python llm_integration_demo.py

依赖：
    pip install ollama pandas

注意：
    需要先安装并运行Ollama：
    1. 下载安装Ollama：https://ollama.ai
    2. 拉取模型：ollama pull qwen3:0.6b
    3. 启动Ollama服务

作者：自动生成示例（中文注释）
"""

try:
    import ollama
    import pandas as pd
    import json
    import time
    from datetime import datetime
    OLLAMA_AVAILABLE = True
except ImportError as e:
    print(f"警告：缺少依赖包 - {e}")
    print("请运行：pip install ollama pandas")
    OLLAMA_AVAILABLE = False


def demo_basic_ollama_chat():
    """演示Ollama基础聊天调用"""
    print('--- 基础Ollama聊天调用 ---')

    if not OLLAMA_AVAILABLE:
        print('跳过Ollama演示（需要 ollama 和 pandas）')
        return

    try:
        # 基础对话
        print('1. 基础对话示例：')
        messages = [
            {
                'role': 'user',
                'content': '你好，请介绍一下自己。'
            }
        ]

        response = ollama.chat(
            model='qwen3:0.6b',
            messages=messages
        )

        print(f'用户: {messages[0]["content"]}')
        print(f'助手: {response["message"]["content"]}')
        print()

        # 包含系统角色的对话
        print('2. 带系统角色的对话：')
        system_messages = [
            {
                'role': 'system',
                'content': '你是一个专业的Python编程助手，请用简洁的技术术语回答问题。'
            },
            {
                'role': 'user',
                'content': '解释一下什么是装饰器？'
            }
        ]

        response = ollama.chat(
            model='qwen3:0.6b',
            messages=system_messages
        )

        print(f'系统: {system_messages[0]["content"]}')
        print(f'用户: {system_messages[1]["content"]}')
        print(f'助手: {response["message"]["content"]}')
        print()

    except Exception as e:
        print(f'Ollama调用错误: {e}')
        print('请确保Ollama已安装并运行，且已拉取qwen3:0.6b模型')


def demo_streaming_response():
    """演示流式响应"""
    print('--- 流式响应演示 ---')

    if not OLLAMA_AVAILABLE:
        print('跳过流式响应演示（需要 ollama）')
        return

    try:
        print('流式响应（打字机效果）：')
        messages = [
            {
                'role': 'user',
                'content': '请写一段关于Python的简短介绍。'
            }
        ]

        # 启用流式响应
        stream = ollama.chat(
            model='qwen3:0.6b',
            messages=messages,
            stream=True
        )

        print('助手: ', end='', flush=True)
        full_response = ''

        for chunk in stream:
            if chunk['message']['content']:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
                time.sleep(0.05)  # 模拟打字机效果

        print('\n')
        print(f'完整响应长度: {len(full_response)} 字符')
        print()

    except Exception as e:
        print(f'流式响应错误: {e}')


def demo_reasoning_process():
    """演示推理过程显示"""
    print('--- 推理过程显示 ---')

    if not OLLAMA_AVAILABLE:
        print('跳过推理过程演示（需要 ollama）')
        return

    try:
        print('启用推理过程显示：')
        messages = [
            {
                'role': 'user',
                'content': '如果一个班有30个学生，其中20个喜欢数学，15个喜欢物理，10个两个都喜欢，问有多少学生不喜欢数学也不喜欢物理？'
            }
        ]

        # 启用推理过程显示
        response = ollama.chat(
            model='qwen3:0.6b',
            messages=messages,
            options={'think': True}  # 注意：实际参数可能因模型而异
        )

        print(f'问题: {messages[0]["content"]}')
        print(f'推理过程: {response.get("thinking", "无推理过程")}')
        print(f'最终答案: {response["message"]["content"]}')
        print()

    except Exception as e:
        print(f'推理过程演示错误: {e}')
        print('注意：推理过程显示功能可能需要特定模型支持')


def demo_multi_turn_conversation():
    """演示多轮对话"""
    print('--- 多轮对话演示 ---')

    if not OLLAMA_AVAILABLE:
        print('跳过多轮对话演示（需要 ollama）')
        return

    try:
        # 维护对话历史
        conversation_history = [
            {
                'role': 'system',
                'content': '你是一个有帮助的编程助手，请记住我们之前的对话内容。'
            }
        ]

        # 第一轮对话
        user_input1 = '我想学习Python编程，应该从哪里开始？'
        conversation_history.append({
            'role': 'user',
            'content': user_input1
        })

        response1 = ollama.chat(
            model='qwen3:0.6b',
            messages=conversation_history
        )

        assistant_reply1 = response1['message']['content']
        conversation_history.append({
            'role': 'assistant',
            'content': assistant_reply1
        })

        print('第一轮对话：')
        print(f'用户: {user_input1}')
        print(f'助手: {assistant_reply1}')
        print()

        # 第二轮对话（基于历史）
        user_input2 = '那数据结构和算法重要吗？'
        conversation_history.append({
            'role': 'user',
            'content': user_input2
        })

        response2 = ollama.chat(
            model='qwen3:0.6b',
            messages=conversation_history
        )

        assistant_reply2 = response2['message']['content']

        print('第二轮对话（记住上下文）：')
        print(f'用户: {user_input2}')
        print(f'助手: {assistant_reply2}')
        print()

    except Exception as e:
        print(f'多轮对话错误: {e}')


def create_sample_questionnaire_data():
    """创建示例问卷数据"""
    # 模拟问卷数据
    questionnaire_data = [
        {
            'id': 1,
            'age': 25,
            'gender': '女',
            'education': '本科',
            'programming_experience': '1-2年',
            'favorite_language': ['Python', 'JavaScript'],
            'learning_motivation': '我想转行到IT行业，听说编程就业前景好',
            'difficulties': '基础语法理解起来比较吃力，特别是面向对象编程',
            'suggestions': '希望有更多实战项目练习'
        },
        {
            'id': 2,
            'age': 30,
            'gender': '男',
            'education': '硕士',
            'programming_experience': '3-5年',
            'favorite_language': ['Python', 'Java'],
            'learning_motivation': '工作中需要用到编程技能，公司要求学习',
            'difficulties': '时间不够用，工作太忙了',
            'suggestions': '课程内容很不错，但节奏可以稍微慢一点'
        },
        {
            'id': 3,
            'age': 22,
            'gender': '女',
            'education': '大专',
            'programming_experience': '无',
            'favorite_language': ['Python'],
            'learning_motivation': '对编程感兴趣，想自学一些技能',
            'difficulties': '数学基础不好，算法思维跟不上',
            'suggestions': '多一些基础概念的解释视频'
        }
    ]

    return questionnaire_data


def analyze_questionnaire_with_llm(questionnaire_data):
    """使用LLM分析问卷数据"""
    print('--- 问卷自动分析演示 ---')

    if not OLLAMA_AVAILABLE:
        print('跳过问卷分析演示（需要 ollama）')
        return

    try:
        # 1. 统计分析（传统编程）
        print('1. 传统编程统计分析：')

        # 性别统计
        gender_stats = {}
        for record in questionnaire_data:
            gender = record['gender']
            gender_stats[gender] = gender_stats.get(gender, 0) + 1

        print(f'性别分布: {gender_stats}')

        # 年龄统计
        ages = [record['age'] for record in questionnaire_data]
        avg_age = sum(ages) / len(ages)
        print(f'平均年龄: {avg_age:.1f}岁')
        print()

        # 2. LLM情感分析
        print('2. LLM情感分析：')

        for i, record in enumerate(questionnaire_data, 1):
            motivation = record['learning_motivation']

            analysis_prompt = f"""
            请分析以下学习动机的情感倾向：
            "{motivation}"

            请从以下方面进行分析：
            1. 情感倾向（积极/消极/中性）
            2. 主要动机类型
            3. 简要分析理由

            请用JSON格式返回结果，包含字段：sentiment, motivation_type, reason
            """

            messages = [
                {
                    'role': 'system',
                    'content': '你是一个专业的情感分析助手，请准确分析文本情感并返回指定格式的JSON结果。'
                },
                {
                    'role': 'user',
                    'content': analysis_prompt
                }
            ]

            try:
                response = ollama.chat(
                    model='qwen3:0.6b',
                    messages=messages
                )

                result_text = response['message']['content']

                # 尝试解析JSON结果
                try:
                    # 清理可能的markdown代码块标记
                    if '```json' in result_text:
                        result_text = result_text.split('```json')[1].split('```')[0].strip()
                    elif '```' in result_text:
                        result_text = result_text.split('```')[1].split('```')[0].strip()

                    analysis_result = json.loads(result_text)

                    print(f'记录{i}学习动机分析：')
                    print(f'  原文: {motivation}')
                    print(f'  情感倾向: {analysis_result.get("sentiment", "未知")}')
                    print(f'  动机类型: {analysis_result.get("motivation_type", "未知")}')
                    print(f'  分析理由: {analysis_result.get("reason", "无")}')
                    print()

                except json.JSONDecodeError:
                    print(f'记录{i}分析结果解析失败，使用原始文本：')
                    print(f'  原文: {motivation}')
                    print(f'  LLM分析: {result_text[:200]}...')
                    print()

            except Exception as e:
                print(f'记录{i}分析失败: {e}')
                print()

        # 3. 主题提取和建议汇总
        print('3. 主题提取和建议汇总：')

        all_difficulties = [record['difficulties'] for record in questionnaire_data]
        all_suggestions = [record['suggestions'] for record in questionnaire_data]

        combined_text = '学习困难：' + '；'.join(all_difficulties) + '\n建议：' + '；'.join(all_suggestions)

        summary_prompt = f"""
        请分析以下问卷反馈数据，提取主要主题并提供改进建议：

        {combined_text}

        请从以下方面进行分析：
        1. 学习困难的主要类型和频率
        2. 学生建议的主要方向
        3. 对课程改进的具体建议

        请用结构化的方式呈现分析结果。
        """

        messages = [
            {
                'role': 'system',
                'content': '你是一个教育数据分析专家，请专业地分析问卷数据并提供建设性建议。'
            },
            {
                'role': 'user',
                'content': summary_prompt
            }
        ]

        response = ollama.chat(
            model='qwen3:0.6b',
            messages=messages
        )

        print('综合分析结果：')
        print(response['message']['content'])
        print()

    except Exception as e:
        print(f'问卷分析错误: {e}')


def demo_ethics_and_security():
    """演示代码伦理与安全性考虑"""
    print('--- 代码伦理与安全性演示 ---')

    print('1. 隐私保护示例：')
    print('✅ 敏感信息脱敏处理')
    print('✅ 本地处理，避免上传敏感数据')
    print()

    print('2. 幻觉问题处理：')
    print('✅ 交叉验证重要信息')
    print('✅ 设置置信度阈值')
    print('✅ 人工审核关键决策')
    print()

    print('3. 学术诚信提醒：')
    print('✅ 标注AI生成内容')
    print('✅ 理解而非抄袭AI输出')
    print('✅ 平衡AI辅助与自主学习')
    print()

    # 演示数据脱敏
    print('4. 数据脱敏示例：')

    sensitive_data = {
        'name': '张三',
        'id_card': '123456789012345678',
        'phone': '13800138000',
        'email': 'zhangsan@example.com',
        'feedback': '我觉得这门课很有帮助'
    }

    def anonymize_data(data):
        """数据脱敏函数"""
        anonymized = data.copy()
        # 脱敏处理
        anonymized['name'] = '学生' + str(hash(data['name']))[:4]
        anonymized['id_card'] = data['id_card'][:6] + '*' * 8 + data['id_card'][-4:]
        anonymized['phone'] = data['phone'][:3] + '*' * 4 + data['phone'][-4:]
        anonymized['email'] = data['email'].split('@')[0][:2] + '*' * 3 + '@' + data['email'].split('@')[1]
        return anonymized

    anonymized_data = anonymize_data(sensitive_data)

    print('原始数据:')
    for key, value in sensitive_data.items():
        print(f'  {key}: {value}')

    print('脱敏后数据:')
    for key, value in anonymized_data.items():
        print(f'  {key}: {value}')

    print('✅ 敏感信息已保护，同时保留分析价值')
    print()


def main():
    print('=' * 50)
    print('大模型开发实战演示')
    print('=' * 50)
    print()

    if not OLLAMA_AVAILABLE:
        print('ollama 或 pandas 未安装，无法运行完整演示')
        print('请运行：pip install ollama pandas')
        print('并确保Ollama已安装并运行')
        return

    try:
        demo_basic_ollama_chat()
        demo_streaming_response()
        demo_reasoning_process()
        demo_multi_turn_conversation()

        # 创建并分析问卷数据
        questionnaire_data = create_sample_questionnaire_data()
        analyze_questionnaire_with_llm(questionnaire_data)

        demo_ethics_and_security()

        print('所有大模型演示已完成')

    except Exception as e:
        print(f'演示过程中发生错误: {e}')
        print('请检查Ollama服务是否正常运行')


if __name__ == '__main__':
    main()