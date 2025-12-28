import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ================= 配置部分 =================
FILE_PATH = 'data.txt'  # 你的数据文件名
# ===========================================

def parse_ping_data(filename):
    """
    解析 ping -D 输出的文件。
    返回: 
        packets: 包含 (seq, timestamp, rtt) 的列表，仅包含收到的包
        start_time: 第一个包的时间戳
    """
    packets = []
    # 正则表达式匹配: [时间戳] ... icmp_seq=数字 ... time=数字 ms
    # 示例: [1703768321.123] 64 bytes from ... icmp_seq=1 ttl=96 time=228 ms
    pattern = re.compile(r'\[(\d+\.\d+)\] .* icmp_seq=(\d+) .* time=(\d+\.?\d*) ms')
    
    with open(filename, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                ts = float(match.group(1))
                seq = int(match.group(2))
                rtt = float(match.group(3))
                packets.append({'seq': seq, 'ts': ts, 'rtt': rtt})
    
    return packets

def analyze_loss_and_bursts(packets):
    """
    分析丢包、连通性以及条件概率
    """
    if not packets:
        return None

    # 按 seq 排序，防止乱序
    packets.sort(key=lambda x: x['seq'])
    
    # 构建完整的序列状态 (1=收到, 0=丢失)
    min_seq = packets[0]['seq']
    max_seq = packets[-1]['seq']
    total_sent = max_seq - min_seq + 1
    received_count = len(packets)
    
    # 创建一个查找集
    received_seqs = set(p['seq'] for p in packets)
    
    # 生成状态列表：按顺序每一跳的状态
    status_stream = []
    for seq in range(min_seq, max_seq + 1):
        if seq in received_seqs:
            status_stream.append(1) # Success
        else:
            status_stream.append(0) # Loss

    # 1. 总体投递率
    delivery_rate = received_count / total_sent

    # 2. 最长连续成功 (Longest consecutive successful pings)
    max_success_burst = 0
    current_success = 0
    for s in status_stream:
        if s == 1:
            current_success += 1
            max_success_burst = max(max_success_burst, current_success)
        else:
            current_success = 0

    # 3. 最长连续丢包 (Longest burst of losses)
    max_loss_burst = 0
    current_loss = 0
    for s in status_stream:
        if s == 0:
            current_loss += 1
            max_loss_burst = max(max_loss_burst, current_loss)
        else:
            current_loss = 0

    # 4. 条件概率 (Conditional Probability)
    # P(Success | Success) = S->S / (S->S + S->L)
    # P(Success | Loss)    = L->S / (L->S + L->L)
    
    ss_count = 0 # Success -> Success
    sl_count = 0 # Success -> Loss
    ls_count = 0 # Loss -> Success
    ll_count = 0 # Loss -> Loss

    for i in range(len(status_stream) - 1):
        curr = status_stream[i]
        next_val = status_stream[i+1]
        
        if curr == 1 and next_val == 1: ss_count += 1
        elif curr == 1 and next_val == 0: sl_count += 1
        elif curr == 0 and next_val == 1: ls_count += 1
        elif curr == 0 and next_val == 0: ll_count += 1

    # 防止除以零
    p_s_given_s = ss_count / (ss_count + sl_count) if (ss_count + sl_count) > 0 else 0
    p_s_given_l = ls_count / (ls_count + ll_count) if (ls_count + ll_count) > 0 else 0

    return {
        'total_sent': total_sent,
        'received': received_count,
        'delivery_rate': delivery_rate,
        'max_success_burst': max_success_burst,
        'max_loss_burst': max_loss_burst,
        'p_s_given_s': p_s_given_s,
        'p_s_given_l': p_s_given_l
    }

def plot_graphs(packets):
    if not packets:
        print("没有数据，无法绘图")
        return

    # 准备数据
    timestamps = [datetime.fromtimestamp(p['ts']) for p in packets]
    rtts = [p['rtt'] for p in packets]
    
    # 图表 1: RTT vs Time
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, rtts, marker='.', linestyle='None', markersize=2, alpha=0.5)
    plt.title('RTT vs Time of Day')
    plt.xlabel('Time')
    plt.ylabel('RTT (ms)')
    plt.grid(True)
    plt.gcf().autofmt_xdate() # 自动旋转日期标签
    plt.savefig('graph1_rtt_time.png')
    plt.show()

    # 图表 2: Histogram / CDF
    plt.figure(figsize=(10, 6))
    # 绘制直方图
    plt.hist(rtts, bins=50, density=True, alpha=0.6, color='g', label='Histogram')
    # 绘制 CDF
    sorted_rtts = np.sort(rtts)
    yvals = np.arange(len(sorted_rtts)) / float(len(sorted_rtts) - 1)
    plt.plot(sorted_rtts, yvals, color='b', linewidth=2, label='CDF')
    plt.title('Distribution of RTTs (Histogram & CDF)')
    plt.xlabel('RTT (ms)')
    plt.ylabel('Probability / Density')
    plt.legend()
    plt.grid(True)
    plt.savefig('graph2_rtt_dist.png')
    plt.show()

    # 图表 3: Correlation (RTT_N vs RTT_N+1)
    # 我们只关心连续收到的包
    rtt_x = []
    rtt_y = []
    
    # 转换为字典以便快速查找: seq -> rtt
    seq_map = {p['seq']: p['rtt'] for p in packets}
    
    # 遍历所有 seq，如果在 map 中找到了 seq 和 seq+1，则加入数据点
    min_seq = packets[0]['seq']
    max_seq = packets[-1]['seq']
    
    for s in range(min_seq, max_seq):
        if s in seq_map and (s + 1) in seq_map:
            rtt_x.append(seq_map[s])
            rtt_y.append(seq_map[s+1])

    plt.figure(figsize=(8, 8))
    plt.scatter(rtt_x, rtt_y, alpha=0.1, s=3)
    plt.title('Correlation: RTT(#N) vs RTT(#N+1)')
    plt.xlabel('RTT of ping #N (ms)')
    plt.ylabel('RTT of ping #N+1 (ms)')
    plt.grid(True)
    # 画一条 y=x 的参考线
    lims = [
        np.min([plt.xlim(), plt.ylim()]),  # min of both axes
        np.max([plt.xlim(), plt.ylim()]),  # max of both axes
    ]
    plt.plot(lims, lims, 'r--', alpha=0.75, zorder=0)
    plt.savefig('graph3_correlation.png')
    plt.show()

def main():
    print(f"正在读取 {FILE_PATH}...")
    try:
        packets = parse_ping_data(FILE_PATH)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {FILE_PATH}。请确认文件名正确。")
        return

    if not packets:
        print("错误: 文件中没有解析到有效的 ping 数据。")
        return

    print(f"成功读取 {len(packets)} 个数据包。正在分析...")
    
    # 基础统计
    rtts = [p['rtt'] for p in packets]
    min_rtt = np.min(rtts)
    max_rtt = np.max(rtts)
    
    # 丢包和概率分析
    stats = analyze_loss_and_bursts(packets)
    
    print("\n" + "="*30)
    print("      实验报告统计数据")
    print("="*30)
    print(f"1. 总体投递率 (Delivery Rate): {stats['delivery_rate']*100:.4f}%")
    print(f"   (发送: {stats['total_sent']}, 接收: {stats['received']})")
    print(f"2. 最长连续成功 (Longest Success Burst): {stats['max_success_burst']}")
    print(f"3. 最长连续丢包 (Longest Loss Burst): {stats['max_loss_burst']}")
    print("-" * 30)
    print(f"4. 条件概率 (Conditional Probabilities):")
    print(f"   P(成功 | 上一次成功): {stats['p_s_given_s']*100:.4f}%")
    print(f"   P(成功 | 上一次失败): {stats['p_s_given_l']*100:.4f}%")
    print(f"   *对比总体成功率: {stats['delivery_rate']*100:.4f}%")
    print("-" * 30)
    print(f"5. 最小 RTT: {min_rtt} ms")
    print(f"6. 最大 RTT: {max_rtt} ms")
    print("="*30)
    
    print("\n正在生成图表...")
    plot_graphs(packets)
    print("完成！图表已保存为 PNG 文件。")

if __name__ == "__main__":
    main()