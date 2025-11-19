"""
Component hỗ trợ copy nội dung vào clipboard
"""
import streamlit as st
import streamlit.components.v1 as components


def copy_to_clipboard(text: str, label: str = "📋 Copy", button_key: str = None):
    """
    Tạo nút copy nội dung vào clipboard sử dụng JavaScript
    
    Args:
        text: Nội dung cần copy
        label: Nhãn hiển thị trên nút
        button_key: Key duy nhất cho nút (tránh trùng lặp)
    """
    # Escape các ký tự đặc biệt trong JavaScript
    safe_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    safe_text = safe_text.replace('\n', '\\n').replace('\r', '\\r').replace('"', '\\"')
    
    # Tạo unique key nếu không có
    if button_key is None:
        button_key = f"copy_{hash(text) % 100000}"
    
    html_code = f"""
    <div style="margin: 10px 0;">
        <button onclick="copyToClipboard{button_key}()" 
                id="btn_{button_key}"
                style="
                    padding: 6px 12px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    background: white;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.3s;
                ">
            {label}
        </button>
        <span id="msg_{button_key}" style="margin-left: 10px; color: green; font-size: 12px;"></span>
    </div>
    <script>
        function copyToClipboard{button_key}() {{
            const text = `{safe_text}`;
            navigator.clipboard.writeText(text).then(function() {{
                document.getElementById('msg_{button_key}').textContent = '✓ Đã copy!';
                setTimeout(function() {{
                    document.getElementById('msg_{button_key}').textContent = '';
                }}, 2000);
            }}, function(err) {{
                document.getElementById('msg_{button_key}').textContent = '✗ Lỗi copy';
                console.error('Copy failed:', err);
            }});
        }}
    </script>
    """
    components.html(html_code, height=60)


def copy_section(title: str, text: str, show_preview: bool = True, key_suffix: str = ""):
    """
    Hiển thị một section với tiêu đề, preview (tuỳ chọn) và nút copy
    
    Args:
        title: Tiêu đề section
        text: Nội dung cần copy
        show_preview: Có hiển thị preview không
        key_suffix: Suffix cho key (tránh trùng lặp)
    """
    st.markdown(f"#### {title}")
    
    if show_preview:
        with st.expander("Xem trước nội dung", expanded=False):
            st.text_area(
                "Nội dung", 
                text, 
                height=150, 
                key=f"preview_{title}_{key_suffix}",
                label_visibility="collapsed"
            )
    
    copy_to_clipboard(text, label=f"📋 Copy {title}", button_key=f"copy_{title}_{key_suffix}")


def copy_page_content(content: str, label: str = "📄 Copy toàn trang"):
    """
    Nút copy toàn bộ nội dung trang
    
    Args:
        content: Nội dung toàn trang
        label: Nhãn hiển thị
    """
    st.markdown("---")
    st.markdown("### Xuất nội dung")
    copy_to_clipboard(content, label=label, button_key="copy_full_page")
