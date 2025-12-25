"""
示例：API开发实战演示

包含演示：
- HTTP请求基础（GET/POST）
- 请求头配置与User-Agent伪装
- 超时与重试机制
- 会话保持与Cookie管理
- SSL证书验证
- JSON数据解析与处理
- 异常处理与错误恢复
- 安全实践与API密钥管理

运行：
    python api_development_demo.py

依赖：
    pip install requests

注意：
    本示例使用公开API进行演示，不会产生实际费用
    如需测试私有API，请替换相应的URL和认证信息

作者：自动生成示例（中文注释）
"""

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from requests.exceptions import RequestException
    REQUESTS_AVAILABLE = True
except ImportError:
    print("警告：requests 未安装，跳过API演示")
    REQUESTS_AVAILABLE = False
    # 不设置 requests = None，避免 Pylance 类型推断问题

import json
import time
import os
from datetime import datetime

# 设置API密钥（实际使用时应该从环境变量读取）
# NEVER hardcode API keys in your code!
API_KEY = os.getenv('DEMO_API_KEY', 'demo_key_replace_with_real_key')


def demo_basic_http_requests():
    """演示基础HTTP请求"""
    print('--- 基础HTTP请求 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过HTTP请求演示（需要 requests）')
        return

    try:
        # GET请求示例 - 获取JSONPlaceholder的示例数据
        print('1. GET请求示例：')
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        print(f'状态码: {response.status_code}')
        print(f'响应头: {dict(response.headers)}')
        print(f'响应内容: {response.json()}')
        print()

        # POST请求示例 - 创建新资源
        print('2. POST请求示例：')
        new_post = {
            'title': '示例标题',
            'body': '这是通过API创建的示例内容',
            'userId': 1
        }
        response = requests.post('https://jsonplaceholder.typicode.com/posts',
                               json=new_post)
        print(f'POST状态码: {response.status_code}')
        print(f'创建的资源: {response.json()}')
        print()

    except Exception as e:
        print(f'请求错误: {e}')


def demo_request_headers():
    """演示请求头配置"""
    print('--- 请求头配置 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过请求头演示（需要 requests）')
        return

    try:
        # 自定义请求头
        headers = {
            'User-Agent': 'Python-API-Demo/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        print('1. 自定义请求头示例：')
        response = requests.get('https://httpbin.org/headers', headers=headers)
        print(f'发送的请求头: {response.json()["headers"]}')
        print()

        # 模拟浏览器User-Agent
        print('2. 浏览器User-Agent伪装：')
        browser_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get('https://httpbin.org/user-agent', headers=browser_headers)
        print(f'伪装的User-Agent: {response.json()["user-agent"]}')
        print()

    except Exception as e:
        print(f'请求错误: {e}')


def demo_timeout_and_retry():
    """演示超时与重试机制"""
    print('--- 超时与重试机制 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过超时重试演示（需要 requests）')
        return

    try:
        # 配置重试策略
        retry_strategy = Retry(
            total=3,  # 总重试次数
            status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的状态码
            allowed_methods=["HEAD", "GET", "OPTIONS"],  # 需要重试的方法
            backoff_factor=1  # 重试间隔倍数
        )

        # 创建带有重试机制的会话
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        print('1. 超时设置示例：')
        # 设置5秒超时
        start_time = time.time()
        try:
            response = requests.get('https://httpbin.org/delay/2', timeout=5)
            elapsed = time.time() - start_time
            print(f'请求成功，耗时: {elapsed:.2f}秒')
        except Exception as e:
            elapsed = time.time() - start_time
            print(f'请求超时或其他错误，耗时: {elapsed:.2f}秒, 错误: {e}')
        print()

        print('2. 重试机制示例：')
        # 测试重试（使用可能不稳定的端点）
        try:
            response = session.get('https://httpbin.org/status/200')  # 改用成功的端点
            print(f'重试后状态码: {response.status_code}')
        except Exception as e:
            print(f'重试请求错误: {e}')
        print()

    except Exception as e:
        print(f'请求错误: {e}')


def demo_session_management():
    """演示会话管理和Cookie保持"""
    print('--- 会话管理和Cookie保持 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过会话管理演示（需要 requests）')
        return

    try:
        # 创建会话对象
        session = requests.Session()

        print('1. 会话保持示例：')
        # 第一次请求
        response1 = session.get('https://httpbin.org/cookies/set/session_id/12345')
        print(f'第一次请求Cookie: {response1.json()}')

        # 第二次请求（会自动携带Cookie）
        response2 = session.get('https://httpbin.org/cookies')
        print(f'第二次请求Cookie: {response2.json()}')
        print()

        print('2. 自定义Cookie示例：')
        # 设置自定义Cookie
        session.cookies.set('user_preference', 'dark_mode', domain='httpbin.org')
        response = session.get('https://httpbin.org/cookies')
        print(f'自定义Cookie: {response.json()}')
        print()

    except Exception as e:
        print(f'请求错误: {e}')


def demo_ssl_verification():
    """演示SSL证书验证"""
    print('--- SSL证书验证 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过SSL验证演示（需要 requests）')
        return

    try:
        print('1. 默认SSL验证（推荐）：')
        response = requests.get('https://httpbin.org/get', timeout=10)
        print(f'HTTPS请求成功: {response.status_code}')
        print()

        print('2. 禁用SSL验证（仅测试环境使用）：')
        # 注意：生产环境中不推荐禁用SSL验证
        response = requests.get('https://httpbin.org/get', verify=False, timeout=10)
        print(f'禁用验证请求成功: {response.status_code}')
        print('⚠️  警告：生产环境应始终启用SSL验证')
        print()

    except Exception as e:
        print(f'请求错误: {e}')


def demo_json_processing():
    """演示JSON数据解析与处理"""
    print('--- JSON数据解析与处理 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过JSON处理演示（需要 requests）')
        return

    try:
        # 获取GitHub API数据 - 获取最近的几个releases
        response = requests.get('https://api.github.com/repos/microsoft/vscode/releases?per_page=3',
                              headers={'Accept': 'application/vnd.github.v3+json'},
                              timeout=10)

        if response.status_code == 200:
            releases = response.json()

            print('1. 列表数据处理 - 多个Release：')
            print(f'获取到 {len(releases)} 个发布版本')
            print()

            # 处理每个release
            for i, release in enumerate(releases[:2], 1):  # 只处理前2个release
                print(f'Release {i}:')
                print(f'  版本名称: {release.get("name", "N/A")}')
                print(f'  标签: {release.get("tag_name", "N/A")}')
                print(f'  发布时间: {release.get("published_at", "N/A")[:10]}')  # 只显示日期部分

                # 处理assets列表
                assets = release.get('assets', [])
                if assets:
                    print(f'  附件数量: {len(assets)}')
                    print('  附件列表:')
                    for asset in assets[:2]:  # 只显示前2个附件
                        print(f'    - {asset.get("name", "N/A")}: {asset.get("download_count", 0)} 次下载')
                else:
                    print('  附件数量: 0 (无附件)')

                print()

            print('2. 嵌套数据安全访问：')
            if releases:
                first_release = releases[0]
                author = first_release.get('author', {})
                print(f'最新版本发布者: {author.get("login", "N/A")}')
                print(f'发布者类型: {author.get("type", "N/A")}')
                print(f'是否为预发布: {first_release.get("prerelease", False)}')
            print()

            print('3. 数据聚合统计：')
            total_reactions = 0
            reaction_types = {}
            prerelease_count = 0
            draft_count = 0

            for release in releases:
                # 统计reactions
                reactions = release.get('reactions', {})
                total_count = reactions.get('total_count', 0)
                total_reactions += total_count

                # 统计各种reaction类型
                for reaction_type in ['+1', 'laugh', 'hooray', 'heart', 'rocket', 'eyes']:
                    count = reactions.get(reaction_type, 0)
                    reaction_types[reaction_type] = reaction_types.get(reaction_type, 0) + count

                # 统计发布类型
                if release.get('prerelease', False):
                    prerelease_count += 1
                if release.get('draft', False):
                    draft_count += 1

            print(f'总反应数: {total_reactions}')
            print(f'预发布版本数: {prerelease_count}')
            print(f'草稿版本数: {draft_count}')
            print('各类型反应统计:')
            for reaction_type, count in reaction_types.items():
                if count > 0:  # 只显示有反应的类型
                    emoji_map = {
                        '+1': '👍',
                        'laugh': '😄',
                        'hooray': '🎉',
                        'heart': '❤️',
                        'rocket': '🚀',
                        'eyes': '👀'
                    }
                    emoji = emoji_map.get(reaction_type, reaction_type)
                    print(f'  {emoji} {reaction_type}: {count}')
            print()

            print('4. 时间戳转换：')
            if releases:
                published_at = releases[0].get('published_at')
                if published_at:
                    # 移除时区信息进行解析
                    dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    print(f'最新版本发布日期: {dt.strftime("%Y年%m月%d日 %H:%M:%S")}')
            print()

    except Exception as e:
        print(f'请求或解析错误: {e}')


def demo_error_handling():
    """演示异常处理与错误恢复"""
    print('--- 异常处理与错误恢复 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过异常处理演示（需要 requests）')
        return

    def safe_api_call(url, max_retries=3, backoff_factor=1):
        """安全的API调用函数"""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=5)

                # 检查状态码
                response.raise_for_status()  # 抛出HTTPError异常如果状态码不是2xx

                return response.json()

            except RequestException as e:
                print(f'尝试 {attempt + 1}/{max_retries}: {type(e).__name__}: {e}')
                # 对于某些错误码，不需要重试
                if hasattr(e, 'response') and e.response and e.response.status_code in [400, 401, 403, 404]:
                    break
            except Exception as e:
                print(f'尝试 {attempt + 1}/{max_retries}: {type(e).__name__}: {e}')
                # 对于其他异常，继续重试

            if attempt < max_retries - 1:
                wait_time = backoff_factor * (2 ** attempt)  # 指数退避
                print(f'等待 {wait_time} 秒后重试...')
                time.sleep(wait_time)

        return None

    print('1. 安全的API调用示例：')
    result = safe_api_call('https://jsonplaceholder.typicode.com/posts/1')
    if result:
        print(f'成功获取数据: {result.get("title", "N/A")}')
    else:
        print('所有重试都失败了')
    print()

    print('2. 错误状态码处理：')
    result = safe_api_call('https://httpbin.org/status/404')
    if result is None:
        print('正确处理了404错误')
    print()


def demo_security_practices():
    """演示安全实践"""
    print('--- 安全实践 ---')

    if not REQUESTS_AVAILABLE:
        print('跳过安全实践演示（需要 requests）')
        return

    print('1. API密钥安全管理：')
    print('✅ 使用环境变量存储敏感信息')
    print('✅ 不要在代码中硬编码API密钥')
    print(f'当前API密钥: {"已设置" if API_KEY != "demo_key_replace_with_real_key" else "使用演示密钥"}')
    print()

    print('2. URL参数安全：')
    # 安全的方式：使用params参数
    try:
        params = {'q': 'python tutorial', 'limit': 10}
        response = requests.get('https://httpbin.org/get', params=params)
        print(f'安全参数传递: {response.json()["args"]}')
    except Exception as e:
        print(f'参数传递示例错误: {e}')
    print()

    print('3. 输入验证和清理：')
    def safe_search(query):
        """安全的搜索函数"""
        if not query or len(query) > 100:
            return None

        # 清理输入
        query = query.strip()

        try:
            # 使用params而不是字符串拼接
            response = requests.get('https://httpbin.org/get',
                                  params={'search': query},
                                  timeout=5)
            return response.json()
        except:
            return None

    try:
        result = safe_search('python api')
        if result:
            print(f'安全搜索结果: {result["args"]}')
    except Exception as e:
        print(f'安全搜索示例错误: {e}')
    print()

    print('4. 速率限制意识：')
    print('✅ 实现请求间隔')
    print('✅ 监控API使用量')
    print('✅ 实现指数退避重试')
    print()


def main():
    print('=' * 50)
    print('API开发实战演示')
    print('=' * 50)
    print()

    if not REQUESTS_AVAILABLE:
        print('requests 未安装，无法运行API演示')
        print('请运行：pip install requests')
        return

    try:
        demo_basic_http_requests()
        demo_request_headers()
        demo_timeout_and_retry()
        demo_session_management()
        demo_ssl_verification()
        demo_json_processing()
        demo_error_handling()
        demo_security_practices()

        print('所有API演示已完成')

    except Exception as e:
        print(f'演示过程中发生错误: {e}')


if __name__ == '__main__':
    main()