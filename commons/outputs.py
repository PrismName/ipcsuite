import os
import json
import csv
from datetime import datetime
from typing import Dict, Any

class OutputFormatter:
    """输出格式化基类"""
    def format(self, data: Dict[str, Any]) -> str:
        raise NotImplementedError

class JsonFormatter(OutputFormatter):
    """JSON格式化器"""
    def format(self, data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False)

class TxtFormatter(OutputFormatter):
    """TXT格式化器"""
    def format(self, data: Dict[str, Any]) -> str:
        result = []
        for key, value in data.items():
            result.append(f"{key}: {value}")
        return "\n".join(result)

class HtmlFormatter(OutputFormatter):
    """HTML格式化器"""
    def format(self, data: Dict[str, Any]) -> str:
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>IPC Suite Scan Result</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>扫描结果</h2>
    <table>
        <tr><th>字段</th><th>值</th></tr>"""
        
        for key, value in data.items():
            html += f"\n        <tr><td>{key}</td><td>{value}</td></tr>"
        
        html += "\n    </table>\n</body>\n</html>"
        return html

class OutputDict(dict):
    """输出字典类，用于存储扫描结果"""
    pass

def save_result(result: Dict[str, Any], output_path: str = None, output_format: str = 'json') -> None:
    """保存扫描结果到指定格式的文件

    Args:
        result: 扫描结果字典
        output_path: 输出文件路径，如果为None则使用默认路径
        output_format: 输出格式，支持'json'、'txt'和'html'
    """
    if not output_path:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'scan_result_{timestamp}.{output_format}')

    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 选择合适的格式化器
    formatters = {
        'json': JsonFormatter(),
        'txt': TxtFormatter(),
        'html': HtmlFormatter()
    }
    formatter = formatters.get(output_format.lower(), JsonFormatter())

    try:
        # 格式化并写入文件
        formatted_result = formatter.format(result)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_result)
        print(f"结果已保存到: {output_path}")
    except Exception as e:
        print(f"保存结果时出错: {str(e)}")
