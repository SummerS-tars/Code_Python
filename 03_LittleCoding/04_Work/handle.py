import pandas as pd
import numpy as np
import os
import warnings

# 忽略 openpyxl 的样式警告
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def process_cafe_data_xlsx():
    """
    根据咖啡厅座位表的信息，更新中控联动表的座位号、昵称和qq号。
    直接操作 .xlsx 文件，并处理复杂的表头结构。
    """
    # ==================== 配置区域 ====================
    # Excel文件所在的文件夹路径
    # 可以使用绝对路径，例如: r'E:\_ComputerLearning\7_Programming_Python\Code_Python\03_LittleCoding\04_Work'
    # 或者使用相对路径，例如: '.' 表示当前目录
    # 留空 '' 表示使用脚本所在的目录
    EXCEL_FOLDER = r'E:\_ComputerLearning\7_Programming_Python\Code_Python\03_LittleCoding\04_Work'
    
    # 如果EXCEL_FOLDER为空，使用脚本所在目录
    if not EXCEL_FOLDER:
        EXCEL_FOLDER = os.path.dirname(os.path.abspath(__file__))
    
    # 输入文件名和工作表名
    FILE_联动表 = '25仆咖中控联动表-第一场.xlsx'
    SHEET_联动表 = '工作表1'
    
    # 座位表改用CSV文件（更稳定，无样式问题）
    FILE_座位表 = '咖啡厅座位表-第一场.csv'  # 或者 '咖啡厅座位表-第二场.csv'
    
    # 输出文件名
    OUTPUT_联动表 = '更新后的25仆咖中控联动表.xlsx'
    OUTPUT_未匹配表 = '座位表-未匹配核销码.xlsx'
    OUTPUT_异常核销码 = '座位表-异常核销码待处理.xlsx'
    # ==================== 配置区域结束 ====================
    
    # 构建完整的文件路径
    FILE_联动表 = os.path.join(EXCEL_FOLDER, FILE_联动表)
    FILE_座位表 = os.path.join(EXCEL_FOLDER, FILE_座位表)
    OUTPUT_联动表 = os.path.join(EXCEL_FOLDER, OUTPUT_联动表)
    OUTPUT_未匹配表 = os.path.join(EXCEL_FOLDER, OUTPUT_未匹配表)
    OUTPUT_异常核销码 = os.path.join(EXCEL_FOLDER, OUTPUT_异常核销码)

    print(f"--- 开始处理 XLSX 数据 ---")
    
    # --- 1. 读取目标表格 (联动表) ---
    # 联动表结构复杂，我们采用分步读取：先读取表头，再读取数据。
    try:
        # 步骤 1a: 读取前2行作为表头（headers）
        # 这样可以原样保留原始的复杂表头格式。
        df_header = pd.read_excel(
            FILE_联动表, 
            sheet_name=SHEET_联动表,
            header=None, 
            nrows=2, 
            engine='openpyxl'
        )

        # 步骤 1b: 读取数据部分，跳过前2行表头
        # 使用 header=None 确保我们通过索引而不是列名来定位数据。
        df_联动表 = pd.read_excel(
            FILE_联动表, 
            sheet_name=SHEET_联动表,
            header=None, 
            skiprows=2, 
            engine='openpyxl'
        )
        
        # 丢弃全是NaN的行（数据清洗）
        df_联动表 = df_联动表.dropna(how='all')
        
        # 根据提供的CSV内容，确定需要操作的列索引 (基于零开始)
        # 索引 1: 昵称, 2: qq号, 4: 座位号, 5: 核销码
        COL_NICKNAME = 1
        COL_QQ = 2
        COL_SEAT = 4
        COL_VERIFY_CODE = 5
        
        # 为方便后续合并，给关键列添加列名
        df_联动表.rename(columns={COL_VERIFY_CODE: '核销码'}, inplace=True)
        
        # 数据预处理：将核销码列转换为字符串、去除空白并统一大写
        df_联动表['核销码'] = df_联动表['核销码'].astype(str).str.strip().str.upper()
        
        print(f"成功加载联动表，表头2行，数据行数: {len(df_联动表)}")

    except FileNotFoundError:
        print(f"错误: 文件 {FILE_联动表} 未找到。请确保文件存在。")
        return
    except Exception as e:
        print(f"错误: 读取联动表时发生错误: {e}")
        return

    # --- 2. 读取源表格 (座位表CSV) ---
    # CSV文件已经清理过，第1行就是列名
    try:
        # 读取CSV文件，第1行作为列名
        df_座位表 = pd.read_csv(
            FILE_座位表, 
            header=0,  # 第1行（索引0）作为列名
            encoding='utf-8-sig'  # 处理可能的BOM字符
        )
        
        # 丢弃全是NaN的行（数据清洗）
        df_座位表 = df_座位表.dropna(how='all')
        
        # 根据CSV内容，列名应该是：座位, cn, qq号, 核销码
        # 打印实际的列名来确认
        print(f"CSV实际列名: {df_座位表.columns.tolist()}")
        
        # 重命名列以方便后续操作
        df_座位表.rename(columns={
            '座位': '新座位号', 
            'cn': '新昵称', 
            'qq号': '新qq号', 
            '核销码': '核销码'
        }, inplace=True)
        
        # 数据预处理：将核销码列转换为字符串、去除空白并统一大写
        df_座位表['核销码'] = df_座位表['核销码'].astype(str).str.strip().str.upper()
        
        # 先打印一些样例数据来调试
        print(f"座位表前5行核销码样例: {df_座位表['核销码'].head(10).tolist()}")
        
        # 分离有效和无效的核销码
        # 有效核销码：长度为4位且为16进制格式（0-9, A-F）
        # 注意：使用 str.fullmatch 或者在正则前后加 ^ $
        valid_mask = (df_座位表['核销码'].str.len() == 4) & (df_座位表['核销码'].str.fullmatch(r'[0-9A-F]{4}', na=False))
        
        # 分离无效核销码的记录（用于异常处理）
        df_异常核销码 = df_座位表[~valid_mask].copy()
        df_异常核销码['异常原因'] = df_异常核销码['核销码'].apply(lambda x: 
            '包含中文或特殊字符' if not x.isalnum() else 
            '长度不符（非4位）' if len(x) != 4 else 
            '格式错误（非16进制）'
        )
        
        # 只保留有效核销码的记录用于后续处理
        df_座位表 = df_座位表[valid_mask].copy()
        
        # 仅保留需要的列
        df_座位表 = df_座位表[['新座位号', '新昵称', '新qq号', '核销码']]
        
        print(f"成功加载座位表CSV，有效记录: {len(df_座位表)} 条")
        if len(df_异常核销码) > 0:
            print(f"发现异常核销码记录: {len(df_异常核销码)} 条（将单独输出）")
        
    except FileNotFoundError:
        print(f"错误: 文件 {FILE_座位表} 未找到。请确保文件存在。")
        return
    except Exception as e:
        print(f"错误: 读取座位表CSV时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # --- 3. 数据合并和更新 ---
    
    # 使用左连接（Left Merge），以联动表为主，根据 '核销码' 合并座位表的信息
    df_merged = df_联动表.merge(
        df_座位表, 
        on='核销码', 
        how='left'
    )

    # 找到成功匹配的行（即 '新座位号' 不为空的行）
    matched_mask = df_merged['新座位号'].notna()

    # 仅更新 '核销码' 匹配成功的行，确保不影响现有其他数据或脚本
    # 注意：这里仍然使用数字索引来更新，因为df_联动表的大部分列还是用索引
    
    # 更新 '座位号' (索引 COL_SEAT)
    df_联动表.loc[matched_mask, COL_SEAT] = df_merged.loc[matched_mask, '新座位号'].values
    
    # 更新 '昵称' (索引 COL_NICKNAME)
    df_联动表.loc[matched_mask, COL_NICKNAME] = df_merged.loc[matched_mask, '新昵称'].values
    
    # 更新 'qq号' (索引 COL_QQ)
    df_联动表.loc[matched_mask, COL_QQ] = df_merged.loc[matched_mask, '新qq号'].values
    
    print(f"成功匹配并更新 {matched_mask.sum()} 条记录到联动表。")
    
    # --- 4. 提取未匹配数据 ---
    
    # 筛选出座位表中 '核销码' 不在 联动表 '核销码' 集合中的行
    # 注意：此时联动表还保持着'核销码'列名
    联动表_核销码_set = set(df_联动表['核销码'].dropna().astype(str).str.upper())
    
    # 排除 '核销码' 不在联动表集合中的行
    unmatched_mask = ~df_座位表['核销码'].isin(联动表_核销码_set)
    df_unmatched = df_座位表[unmatched_mask].copy()
    
    print(f"发现 {len(df_unmatched)} 条座位表信息未在联动表中找到匹配项。")

    # --- 5. 结果输出 ---
    
    # 5a. 输出更新后的联动表 (.xlsx)
    try:
        # 将核销码列名改回数字索引，保持原始结构
        df_联动表.rename(columns={'核销码': COL_VERIFY_CODE}, inplace=True)
        
        # 将原始表头和更新后的数据合并，以保留原始表的复杂结构
        final_df = pd.concat([df_header, df_联动表], ignore_index=True)
        
        # 使用 ExcelWriter 确保一次性写入
        with pd.ExcelWriter(OUTPUT_联动表, engine='openpyxl') as writer:
            # 写入时 header=False 和 index=False 保持原始结构
            final_df.to_excel(writer, sheet_name=SHEET_联动表, index=False, header=False)

        print(f"✅ 更新后的联动表已保存到: {OUTPUT_联动表}")
    except Exception as e:
        print(f"错误: 无法保存更新后的联动表: {e}")

    # 5b. 输出未匹配的座位表信息 (.xlsx)
    try:
        # 重命名列以更清晰地指示它们来自座位表
        df_unmatched.rename(columns={
            '新座位号': '座位号', 
            '新昵称': '昵称', 
            '新qq号': 'qq号'
        }, inplace=True)
        
        df_unmatched.to_excel(OUTPUT_未匹配表, index=False, engine='openpyxl')
        print(f"✅ 未匹配的座位表信息已保存到: {OUTPUT_未匹配表}")
    except Exception as e:
        print(f"错误: 无法保存未匹配数据: {e}")
    
    # 5c. 输出异常核销码信息 (.xlsx)
    if len(df_异常核销码) > 0:
        try:
            # 重命名列并调整顺序，方便人工处理
            df_异常核销码_输出 = df_异常核销码[['新座位号', '新昵称', '新qq号', '核销码', '异常原因']].copy()
            df_异常核销码_输出.rename(columns={
                '新座位号': '座位号', 
                '新昵称': '昵称', 
                '新qq号': 'qq号'
            }, inplace=True)
            
            df_异常核销码_输出.to_excel(OUTPUT_异常核销码, index=False, engine='openpyxl')
            print(f"✅ 异常核销码信息已保存到: {OUTPUT_异常核销码}")
            print(f"   请人工核对并处理这 {len(df_异常核销码)} 条记录")
        except Exception as e:
            print(f"错误: 无法保存异常核销码数据: {e}")
    else:
        print(f"✅ 未发现异常核销码，所有记录格式正常")
        
    print(f"--- 数据处理完成 ---")

if __name__ == "__main__":
    process_cafe_data_xlsx()