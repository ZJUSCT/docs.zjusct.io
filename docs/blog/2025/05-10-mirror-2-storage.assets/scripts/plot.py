import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import glob
import numpy as np


def read_log_file(filepath, log_type):
    # Read log into dataframe
    cols = ['time_ms', 'value', 'direction',
            'bs', 'offset', 'prio', 'issue_time']
    df = pd.read_csv(filepath, comment='#', names=cols)

    # Convert time to seconds
    df['time_sec'] = df['time_ms'] / 1000

    # Add label for log type
    if log_type == 'bw':
        df['value_kbps'] = df['value']  # already in KiB/sec
    elif log_type == 'iops':
        df['value_iops'] = df['value']
    elif log_type == 'lat':
        df['value_ms'] = df['value'] / 1000000  # Convert nsec to msec

    return df


def parse_summary_from_json(json_data, metric_type):
    """Extract summary statistics from FIO JSON output"""
    total = 0
    count = 0
    for job in json_data['jobs']:
        if metric_type == 'bw':
            # 累加所有作业的带宽平均值
            total += job.get('write', {}).get('bw_mean', 0) + \
                job.get('read', {}).get('bw_mean', 0)
        elif metric_type == 'iops':
            # 累加所有作业的IOPS平均值
            total += job.get('write', {}).get('iops_mean', 0) + \
                job.get('read', {}).get('iops_mean', 0)
        elif metric_type == 'lat':
            # 计算延迟的平均值
            write_data = job.get('write', {}).get(f'{metric_type}_ns', {})
            read_data = job.get('read', {}).get(f'{metric_type}_ns', {})

            if 'mean' in write_data:
                # Convert ns to ms
                total += write_data['mean'] / 1000000
                count += 1
            if 'mean' in read_data:
                # Convert ns to ms
                total += read_data['mean'] / 1000000
                count += 1

    if metric_type == 'lat':
        return total / count if count > 0 else 0
    return total


def plot_metric_over_time(dfs, log_type, jobnames, outfile_base, device):
    plt.figure(figsize=(15, 6))

    # 打开并解析JSON文件
    json_file = os.path.join(os.path.dirname(outfile_base), 'mix.json')
    with open(json_file) as f:
        json_data = json.load(f)

    # 创建统一的时间索引
    start_time = max(df['time_sec'].min() for df in dfs)
    end_time = min(df['time_sec'].max() for df in dfs)
    time_points = np.arange(start_time, end_time, 1)  # 1秒间隔

    values = []
    labels = []
    max_value = 0
    summary_values = []

    for i, df in enumerate(dfs):
        # 创建时间序列并重采样
        if log_type == 'bw':
            series = pd.Series(index=df['time_sec'],
                               data=df['value_kbps'].values / 1024)
        elif log_type == 'iops':
            series = pd.Series(index=df['time_sec'],
                               data=df['value_iops'].values)
        elif log_type == 'lat':
            series = pd.Series(index=df['time_sec'],
                               data=df['value_ms'].values)

        # 重采样到统一的时间点
        resampled = np.interp(time_points, df['time_sec'], series.values)
        values.append(resampled)
        labels.append(f'{jobnames[i]}')

    if log_type == 'lat':
        # 对于延迟指标使用折线图
        for i, value in enumerate(values):
            plt.plot(time_points, value, label=f'{labels[i]} (real-time)')
        # 添加平均延迟线
        summary = parse_summary_from_json(json_data, log_type)
        plt.axhline(y=summary, color='r', linestyle='--',
                    label=f'Overall mean: {summary:.3f}ms')
    else:
        # 对于带宽和IOPS使用堆积图
        plt.stackplot(time_points, values, labels=[
                      f'{l} (real-time)' for l in labels])
        # 添加总计值线
        summary = parse_summary_from_json(json_data, log_type)
        if log_type == 'bw':
            summary = summary / 1024  # Convert to MB/s
        plt.axhline(y=summary, color='r', linestyle='--',
                    label=f'Total avg: {summary:.1f}')

    # 设置y轴标签
    if log_type == 'bw':
        ylabel = 'Bandwidth (MB/s)'
    elif log_type == 'iops':
        ylabel = 'IOPS'
    elif log_type == 'lat':
        ylabel = 'Latency (ms)'

    plt.xlabel('Time (s)')
    plt.ylabel(ylabel)
    plt.title(f'{log_type.upper()} Over Time - {device}')
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    plt.tight_layout()

    outfile = f'{outfile_base}_{log_type}_{"line" if log_type == "lat" else "stacked"}.png'
    plt.savefig(outfile, bbox_inches='tight')
    plt.close()
    print(
        f'✅ Saved {"line" if log_type == "lat" else "stacked"} plot: {outfile}')


def parse_json_jobs(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return [job['jobname'] for job in data['jobs']]


def get_job_files(directory):
    # 获取所有日志文件并按类型分组
    files = {}
    for log_type in ['bw', 'iops', 'lat']:
        pattern = os.path.join(directory, f'job_*_{log_type}.*.log')
        matching_files = sorted(glob.glob(pattern))
        if matching_files:
            files[log_type] = matching_files
    return files


def process_fio_logs(directory):
    json_file = os.path.join(directory, 'mix.json')
    if not os.path.exists(json_file):
        print(f"Report file {json_file} does not exist.")
        return

    jobnames = parse_json_jobs(json_file)
    device = os.path.basename(directory)

    # 获取所有日志文件
    log_files = get_job_files(directory)

    # 处理每种类型的日志
    for log_type, files in log_files.items():
        dfs = []
        thread_jobnames = []

        for log_file in files:
            # 从文件名中提取作业名称
            filename = os.path.basename(log_file)
            # job_type_size_metric.number.log
            parts = filename.split('_')
            if len(parts) >= 3:
                jobname = f"{parts[1]}_{parts[2]}"  # 组合type_size作为作业名称
                df = read_log_file(log_file, log_type)
                dfs.append(df)
                thread_jobnames.append(jobname)

        if dfs:
            outfile_base = os.path.join(directory, os.path.basename(directory))
            plot_metric_over_time(
                dfs, log_type, thread_jobnames, outfile_base, device)


def main():
    parser = argparse.ArgumentParser(
        description='Process FIO log files and generate plots')
    parser.add_argument('directory', help='Directory containing FIO log files')
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print(f"Directory {args.directory} does not exist.")
        exit(1)

    process_fio_logs(args.directory)


if __name__ == "__main__":
    main()
