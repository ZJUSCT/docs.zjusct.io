"""FIO Benchmark Results Parser and HTML Report Generator

This script processes FIO benchmark test results and generates an HTML report with performance metrics.

Usage:
    python diskbench_html.py <folder_path>

Arguments:
    folder_path: Path to the directory containing FIO JSON result files.
                Will recursively scan all .json files in this directory.

Input Format:
    Expects FIO JSON output files containing disk performance test results.
    Each file should contain results for:
    - Sequential 1M (Queue=8, Thread=1) Read/Write
    - Sequential 128K (Queue=32, Thread=1) Read/Write
    - Random 4K (Queue=32, Thread=16) Read/Write
    - Random 4K (Queue=1, Thread=1) Read/Write

Output:
    Generates a results.html file in the input folder containing three tables:
    1. Bandwidth (MB/s)
    2. IOPS (IO operations per second)
    3. Latency (milliseconds)

Example:
    python diskbench_html.py /path/to/fio/results/

Notes:
    - Disk names are extracted from the 'filename' field in FIO's global options
    - Bandwidth is converted from KB/s to MB/s
    - Latency is converted from nanoseconds to milliseconds
"""

import json
import os
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional


class TestResult(NamedTuple):
    bw: float  # Bandwidth in MB/s
    iops: float  # IO Operations per second
    lat: float  # Average latency in milliseconds


class DiskResult(NamedTuple):
    seq1m_q8t1_read: Optional[TestResult]
    seq1m_q8t1_write: Optional[TestResult]
    seq128k_q32t1_read: Optional[TestResult]
    seq128k_q32t1_write: Optional[TestResult]
    rnd4k_q32t16_read: Optional[TestResult]
    rnd4k_q32t16_write: Optional[TestResult]
    rnd4k_q1t1_read: Optional[TestResult]
    rnd4k_q1t1_write: Optional[TestResult]


def parse_job_data(job: Dict) -> Optional[TestResult]:
    """Extract test metrics from a FIO job section.

    Args:
        job: Dictionary containing FIO job results
             Must have 'read' and 'write' sections with bw, iops, and lat_ns data

    Returns:
        TestResult object with normalized values (MB/s, IOPS, ms) or None if invalid
    """
    if 'read' not in job or 'write' not in job:
        return None

    op = job['read'] if job['jobname'].endswith('READ') else job['write']

    # Convert bandwidth from KB/s to MB/s
    bw = op.get('bw', 0) / 1024.0

    # Get IOPS
    iops = op.get('iops', 0)

    # Get average latency and convert to ms
    lat = op.get('lat_ns', {}).get('mean', 0) / 1000000.0

    return TestResult(bw, iops, lat)


def get_disk_name(data: Dict) -> Optional[str]:
    """Extract disk name from FIO test data.

    Args:
        data: Dictionary containing FIO test results with global options

    Returns:
        Device name (e.g., 'sda', 'nvme0n1') or None if not found

    Example:
        If filename is '/dev/sda', returns 'sda'
    """
    try:
        filename = data.get('global options', {}).get('filename')
        if not filename:
            return None
        # Extract the last part of the device path (e.g., 'sdo' from '/dev/sdo')
        return filename.split('/')[-1]
    except Exception:
        return None


def parse_report(filepath: Path) -> Optional[DiskResult]:
    """Parse FIO JSON report and extract standardized test results.

    Processes the following test patterns:
    - SEQ1M_Q8T1: Sequential 1M, Queue=8, Thread=1
    - SEQ128K_Q32T1: Sequential 128K, Queue=32, Thread=1
    - RND4K_Q32T16: Random 4K, Queue=32, Thread=16
    - RND4K_Q1T1: Random 4K, Queue=1, Thread=1

    Each pattern should have both READ and WRITE results.

    Args:
        filepath: Path to FIO JSON result file

    Returns:
        DiskResult object containing all test results or None if parsing fails
    """
    try:
        with open(filepath) as f:
            data = json.load(f)

        # Skip if not a valid fio test result
        if 'jobs' not in data or 'fio version' not in data:
            return None

        jobs = data.get('jobs', [])
        results = {}

        for job in jobs:
            name = job.get('jobname', '')
            if not name:
                continue

            result = parse_job_data(job)
            if result:
                results[name] = result

        return DiskResult(
            results.get('SEQ1M_Q8T1_READ'),
            results.get('SEQ1M_Q8T1_WRITE'),
            results.get('SEQ128K_Q32T1_READ'),
            results.get('SEQ128K_Q32T1_WRITE'),
            results.get('RND4K_Q32T16_READ'),
            results.get('RND4K_Q32T16_WRITE'),
            results.get('RND4K_Q1T1_READ'),
            results.get('RND4K_Q1T1_WRITE'),
        )

    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None


def _generate_table_header() -> str:
    """Generate common table header"""
    return """
        <tr>
            <th>Disk</th>
            <th colspan="2">SEQ1M_Q8T1</th>
            <th colspan="2">SEQ128K_Q32T1</th>
            <th colspan="2">RND4K_Q32T16</th>
            <th colspan="2">RND4K_Q1T1</th>
        </tr>
        <tr>
            <th></th>
            <th>READ</th>
            <th>WRITE</th>
            <th>READ</th>
            <th>WRITE</th>
            <th>READ</th>
            <th>WRITE</th>
            <th>READ</th>
            <th>WRITE</th>
        </tr>
    """


def _generate_metric_table(results: Dict[str, DiskResult], metric: str, format_str: str) -> str:
    """Generate table for a specific metric"""
    html = f"""
    <h3>{metric}</h3>
    <table>
        {_generate_table_header()}
    """

    for disk_name, disk_result in results.items():
        html += f"""
        <tr>
            <td class="disk-name">{disk_name}</td>"""
        for result in disk_result:
            value = format_str.format(
                getattr(result, metric.lower())) if result else "N/A"
            html += f"<td>{value}</td>"
        html += "</tr>"

    html += "</table><br>"
    return html


def generate_html_table(results: Dict[str, DiskResult]) -> str:
    """Generate HTML tables from disk results"""
    html = """
    <style>
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid black; padding: 8px; text-align: right; }
        th { background-color: #f2f2f2; }
        .disk-name { text-align: left; }
        h3 { margin-top: 20px; }
    </style>
    """

    # Generate bandwidth table (MB/s)
    html += _generate_metric_table(results, "bw", "{:.1f}")

    # Generate IOPS table
    html += _generate_metric_table(results, "iops", "{:.0f}")

    # Generate latency table (ms)
    html += _generate_metric_table(results, "lat", "{:.2f}")

    return html


def main(folder_path: str):
    """Process FIO test results and generate HTML report.

    Workflow:
    1. Recursively scan input folder for .json files
    2. For each file:
       - Extract disk name from global options
       - Parse performance metrics
       - Collect results by disk
    3. Generate HTML tables for bandwidth, IOPS, and latency
    4. Write results to results.html in input folder

    Args:
        folder_path: Directory containing FIO JSON result files
    """
    results = {}
    folder = Path(folder_path)
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

    html = generate_html_table(results)

    output_path = folder / "results.html"
    with open(output_path, "w") as f:
        f.write(html)
    print(f"Results written to {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python diskbench_html.py <folder_path>")
        sys.exit(1)
    main(sys.argv[1])
