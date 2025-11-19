"""
Component xuất dữ liệu sang các format khác nhau
"""
import streamlit as st
import pandas as pd
import json
from typing import Any, List, Dict
from io import StringIO


def export_to_csv(data: List[Dict], filename: str = "export.csv"):
    """
    Xuất dữ liệu sang CSV
    
    Args:
        data: List of dictionaries
        filename: Tên file xuất
    """
    try:
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Tải CSV",
            data=csv,
            file_name=filename,
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Lỗi xuất CSV: {e}")


def export_to_json(data: Any, filename: str = "export.json"):
    """
    Xuất dữ liệu sang JSON
    
    Args:
        data: Dữ liệu cần xuất (dict, list, etc.)
        filename: Tên file xuất
    """
    try:
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="📥 Tải JSON",
            data=json_str,
            file_name=filename,
            mime="application/json",
        )
    except Exception as e:
        st.error(f"Lỗi xuất JSON: {e}")


def export_to_markdown(content: str, filename: str = "export.md"):
    """
    Xuất nội dung sang Markdown
    
    Args:
        content: Nội dung text/markdown
        filename: Tên file xuất
    """
    try:
        st.download_button(
            label="📥 Tải Markdown",
            data=content,
            file_name=filename,
            mime="text/markdown",
        )
    except Exception as e:
        st.error(f"Lỗi xuất Markdown: {e}")


def show_export_options(
    data_csv: List[Dict] = None,
    data_json: Any = None,
    content_md: str = None,
    prefix: str = "export"
):
    """
    Hiển thị các tuỳ chọn xuất dữ liệu
    
    Args:
        data_csv: Dữ liệu cho CSV export
        data_json: Dữ liệu cho JSON export
        content_md: Nội dung cho Markdown export
        prefix: Prefix cho tên file
    """
    st.markdown("#### 📤 Xuất dữ liệu")
    
    cols = st.columns(3)
    
    with cols[0]:
        if data_csv is not None:
            export_to_csv(data_csv, f"{prefix}.csv")
    
    with cols[1]:
        if data_json is not None:
            export_to_json(data_json, f"{prefix}.json")
    
    with cols[2]:
        if content_md is not None:
            export_to_markdown(content_md, f"{prefix}.md")


def format_table_for_copy(df: pd.DataFrame) -> str:
    """
    Format DataFrame thành bảng text để copy
    
    Args:
        df: DataFrame cần format
        
    Returns:
        Chuỗi text đã format
    """
    return df.to_string(index=False)


def format_dict_for_copy(data: Dict, indent: int = 2) -> str:
    """
    Format dictionary thành chuỗi dễ đọc
    
    Args:
        data: Dictionary cần format
        indent: Số space indent
        
    Returns:
        Chuỗi đã format
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)
