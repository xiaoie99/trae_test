import os
import time
from datetime import datetime, timedelta
def main():
    # 1. 确定备份目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(base_dir, 'backup')
    # 如果目录不存在则创建
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    print(f"开始模拟备份，目录: {backup_dir}")
    print("按 Ctrl+C 停止并清理...")
    try:
        while True:
            # 2. 获取当前时间并生成备份文件
            now = datetime.now()
            now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
            filename = f"backup_{now_str}.txt"
            filepath = os.path.join(backup_dir, filename)
            # 创建空文件模拟备份
            with open(filepath, 'w') as f:
                f.write(f"模拟备份时间: {now_str}")
            print(f"\n[+] 创建备份: {filename}")
            # 3. 计算 15 秒前的时间基准
            expire_time = now - timedelta(seconds=15)
            # 4. 遍历备份目录，找出过期文件并删除
            current_files = []
            for file in os.listdir(backup_dir):
                if file.startswith('backup_') and file.endswith('.txt'):
                    # 从文件名提取时间字符串
                    time_str = file.replace('backup_', '').replace('.txt', '')
                    # 将字符串转换回 datetime 对象进行比较
                    file_time = datetime.strptime(time_str, '%Y-%m-%d_%H-%M-%S')
                    # 比较时间，如果过期则删除，否则加入 current_files 列表
                    if file_time < expire_time:
                        file_path = os.path.join(backup_dir, file)
                        os.remove(file_path)
                        print(f"[-] 删除过期: {file}")
                    else:
                        current_files.append(file)
            # 额外限制：最多保留5个文件（删除多余的最旧文件）
            if len(current_files) > 5:
                # 按文件名排序（即按时间排序）
                current_files.sort()
                files_to_remove = current_files[:-5]  # 保留最后5个
                for file in files_to_remove:
                    file_path = os.path.join(backup_dir, file)
                    os.remove(file_path)
                    print(f"[-] 删除多余: {file}")
                current_files = current_files[-5:]  # 更新当前列表
            # 5. 打印当前保留的所有备份文件
            print(f"[*] 当前保留的备份 ({len(current_files)}个):")
            for f in sorted(current_files):
                print(f"    - {f}")
            # 6. 休眠 3 秒
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n\n收到停止信号，正在清理所有备份文件...")
        # 遍历目录，删除所有 backup_ 开头的 txt 文件
        if os.path.exists(backup_dir):
            for file in os.listdir(backup_dir):
                if file.startswith('backup_') and file.endswith('.txt'):
                    file_path = os.path.join(backup_dir, file)
                    os.remove(file_path)
                    print(f"[-] 已清理: {file}")
            # 删除 backup_dir 目录本身
            os.rmdir(backup_dir)
            print(f"[-] 已删除 backup 目录")
        print("清理完成，程序退出。")
if __name__ == '__main__':
    main()