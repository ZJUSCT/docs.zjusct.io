"""
Disk Benchmark Visualization Tool

This script visualizes disk benchmark results by generating heatmaps for:
- Bandwidth (MB/s)
- IOPS (Input/Output Operations Per Second)
- Latency (milliseconds)

Usage:
    python diskbench_visualize.py <folder_path>

Arguments:
    folder_path: Directory containing JSON benchmark result files

Output:
    Creates visualization.png in the input folder containing three heatmaps
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from diskbench_html import parse_report, get_disk_name
import json
from pathlib import Path


def prepare_plot_data(results):
    """
    Prepare data arrays for heatmap visualization.

    Args:
        results: Dictionary of benchmark results keyed by disk name

    Returns:
        Tuple of (bandwidth, IOPS, latency) arrays and axis labels
    """
    disks = list(results.keys())
    test_names = [
        'SEQ1M_Q8T1_READ', 'SEQ1M_Q8T1_WRITE',
        'SEQ128K_Q32T1_READ', 'SEQ128K_Q32T1_WRITE',
        'RND4K_Q32T16_READ', 'RND4K_Q32T16_WRITE',
        'RND4K_Q1T1_READ', 'RND4K_Q1T1_WRITE'
    ]

    # Initialize data arrays
    Z_bw = np.zeros((len(test_names), len(disks)))
    Z_iops = np.zeros((len(test_names), len(disks)))
    Z_lat = np.zeros((len(test_names), len(disks)))

    # Fill in the data
    for i, disk in enumerate(disks):
        result = results[disk]
        metrics = [
            result.seq1m_q8t1_read, result.seq1m_q8t1_write,
            result.seq128k_q32t1_read, result.seq128k_q32t1_write,
            result.rnd4k_q32t16_read, result.rnd4k_q32t16_write,
            result.rnd4k_q1t1_read, result.rnd4k_q1t1_write
        ]
        for j, metric in enumerate(metrics):
            if metric:
                Z_bw[j, i] = metric.bw
                Z_iops[j, i] = metric.iops
                Z_lat[j, i] = metric.lat

    return Z_bw, Z_iops, Z_lat, disks, test_names


def plot_heatmap_results(results, output_path):
    """
    Generate and save heatmap visualizations of benchmark results.

    Args:
        results: Dictionary of benchmark results keyed by disk name
        output_path: Path where the output PNG file should be saved
    """
    Z_bw, Z_iops, Z_lat, disks, test_names = prepare_plot_data(results)

    # Dynamically adjust figure width based on the number of disks
    fig_width = max(10, len(disks))
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(fig_width, 6))

    # Plot Bandwidth
    im1 = ax1.imshow(Z_bw, aspect='auto', cmap='viridis')
    ax1.set_title('Bandwidth (MB/s)')
    ax1.set_xticks(range(len(disks)))
    ax1.set_xticklabels(disks, rotation=90, ha='right')
    ax1.set_yticks(range(len(test_names)))
    ax1.set_yticklabels(test_names)
    plt.colorbar(im1, ax=ax1)

    # Plot IOPS
    im2 = ax2.imshow(Z_iops, aspect='auto', cmap='viridis')
    ax2.set_title('IOPS')
    ax2.set_xticks(range(len(disks)))
    ax2.set_xticklabels(disks, rotation=90, ha='right')
    ax2.set_yticks(range(len(test_names)))
    ax2.set_yticklabels(test_names)
    plt.colorbar(im2, ax=ax2)

    # Plot Latency
    im3 = ax3.imshow(Z_lat, aspect='auto', cmap='viridis')
    ax3.set_title('Latency (ms)')
    ax3.set_xticks(range(len(disks)))
    ax3.set_xticklabels(disks, rotation=90, ha='right')
    ax3.set_yticks(range(len(test_names)))
    ax3.set_yticklabels(test_names)
    plt.colorbar(im3, ax=ax3)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main(folder_path: str):
    """
    Process FIO test results and generate visualization.

    Args:
        folder_path: Directory containing JSON benchmark result files
    """
    results = {}
    folder = Path(folder_path)

    # Parse results (reusing logic from result.py)
    for file in sorted(folder.glob("**/*.json"), key=lambda x: x.name):
        try:
            with open(file) as f:
                data = json.load(f)

            disk_name = get_disk_name(data)
            if not disk_name:
                continue

            result = parse_report(file)
            if result:
                results[disk_name] = result
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue

    if not results:
        print("No valid fio test results found")
        return

    # Generate visualization
    output_path = folder / "visualization.png"
    plot_heatmap_results(results, output_path)
    print(f"Visualization saved to {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python visualize.py <folder_path>")
        sys.exit(1)
    main(sys.argv[1])
