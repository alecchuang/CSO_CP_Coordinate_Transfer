import streamlit as st

# --- 建立 ATK 字元與數字的對應表 ---
atk_chars = ['0','1','2','3','4','5','6','7','8','9','A','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S']
atk_values = list(range(26))

# 將字元轉為數字 (輸入時用)
atk_char_to_int = {str(c): v for c, v in zip(atk_chars, atk_values)}
# 將數字轉為字元 (輸出時用)
atk_int_to_char = {v: str(c) for c, v in zip(atk_chars, atk_values)}

# 取得一般數字輸入值的輔助函數
def get_numeric_value(val_str):
    val = val_str.strip()
    if val == "":
        return None
    try:
        return float(val)
    except ValueError:
        return "ERROR"

# 取得 ATK 特殊字元輸入值的輔助函數
def get_atk_value(val_str):
    # 轉換為大寫以支援使用者輸入小寫字母
    val = val_str.strip().upper() 
    if val == "":
        return None
    if val in atk_char_to_int:
        return atk_char_to_int[val]
    else:
        return "ERROR"

# 將計算結果轉回 ATK 字元的輔助函數
def format_atk_output(val):
    # 如果計算出來的數字超出 0-25 的範圍，顯示 Out of Range，否則顯示對應字元
    return atk_int_to_char.get(val, f"超出範圍({val})")

# === Streamlit 頁面設定 ===
st.set_page_config(page_title="Coordinate Transfer", layout="centered")
st.title("Coordinate Transfer")
st.markdown("**(CP Prober / CP Fuse / ATT AOI / ATK)**")
st.divider()

# --- 建立輸入區塊 (使用雙欄排版) ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### X Coordinate Input")
    probe_x_input = st.text_input("CP Prober X:")
    fuse_x_input = st.text_input("CP Fuse X:")
    aoi_x_input = st.text_input("ATT AOI X:")
    atk_x_input = st.text_input("ATK X:", help="支援的字元: 0-9, A, C-H, J-N, P-S")

with col2:
    st.markdown("### Y Coordinate Input")
    probe_y_input = st.text_input("CP Prober Y:")
    fuse_y_input = st.text_input("CP Fuse Y:")
    aoi_y_input = st.text_input("ATT AOI Y:")
    atk_y_input = st.text_input("ATK Y:", help="支援的字元: 0-9, A, C-H, J-N, P-S")

st.markdown("") # 產生一點空隙

# --- 建立 Start 按鈕 ---
if st.button("Start Transfer", type="primary", use_container_width=True):
    
    # 讀取輸入框的內容並解析
    probe_x = get_numeric_value(probe_x_input)
    probe_y = get_numeric_value(probe_y_input)
    fuse_x = get_numeric_value(fuse_x_input)
    fuse_y = get_numeric_value(fuse_y_input)
    aoi_x = get_numeric_value(aoi_x_input)
    aoi_y = get_numeric_value(aoi_y_input)
    atk_x = get_atk_value(atk_x_input)
    atk_y = get_atk_value(atk_y_input)

    # 檢查是否有輸入錯誤
    if "ERROR" in (probe_x, probe_y, fuse_x, fuse_y, aoi_x, aoi_y):
        st.error("[錯誤] CP Prober / CP Fuse / ATT AOI 請確保輸入有效的數字！")
        st.stop()
    
    if "ERROR" in (atk_x, atk_y):
        st.error("[錯誤] ATK 請確保輸入支援的字元 (0-9, A, C-H, J-N, P-S)！")
        st.stop()

    # 用來收集輸出訊息的清單
    log_messages = ["--- Transfer result ---"]

    # --- CP Prober 轉換邏輯 ---
    if probe_x is not None and probe_y is not None:
        out_fuse_x = int(probe_y)
        out_fuse_y = int(25 - probe_x)
        out_aoi_x = int(probe_y)
        out_aoi_y = int(probe_x)
        
        out_atk_x_char = format_atk_output(int(probe_y))
        out_atk_y_char = format_atk_output(int(25 - probe_x))
        
        log_messages.append(f"[Input CP Prober XY] -> CP Fuse [X,Y]: [ {out_fuse_x} , {out_fuse_y} ]") 
        log_messages.append(f"[Input CP Prober XY] -> ATT AOI [X,Y]: [ {out_aoi_x} , {out_aoi_y} ]") 
        log_messages.append(f"[Input CP Prober XY] -> ATK     [X,Y]: [ {out_atk_x_char} , {out_atk_y_char} ]") 
    elif probe_x is not None or probe_y is not None:
        log_messages.append("[Input CP Prober XY] Fail：Need input CP Prober X and CP Prober Y together。")
    else:
        log_messages.append("[Input CP Prober XY] No input，Skip。")
    
    log_messages.append("- - - - - - - - -")

    # --- CP Fuse 轉換邏輯 ---
    if fuse_x is not None and fuse_y is not None:
        out_probe_x = int(25 - fuse_y)
        out_probe_y = int(fuse_x)
        out_aoi_x = int(fuse_x)
        out_aoi_y = int(25 - fuse_y)
        
        out_atk_x_char = format_atk_output(int(fuse_x))
        out_atk_y_char = format_atk_output(int(fuse_y))
        
        log_messages.append(f"[Input CP Fuse XY]   -> CP Prober[X,Y]: [ {out_probe_x} , {out_probe_y} ]")
        log_messages.append(f"[Input CP Fuse XY]   -> ATT AOI  [X,Y]: [ {out_aoi_x} , {out_aoi_y} ]")
        log_messages.append(f"[Input CP Fuse XY]   -> ATK      [X,Y]: [ {out_atk_x_char} , {out_atk_y_char} ]")
    elif fuse_x is not None or fuse_y is not None:
        log_messages.append("[Input CP Fuse XY] Fail：Need input CP Fuse X and CP Fuse Y together。")
    else:
        log_messages.append("[Input CP Fuse XY] No input，Skip。")

    log_messages.append("- - - - - - - - -")
    
    # --- ATT AOI 轉換邏輯 ---
    if aoi_x is not None and aoi_y is not None:
        out_probe_x = int(aoi_y)
        out_probe_y = int(aoi_x)
        out_fuse_x = int(out_probe_y)
        out_fuse_y = int(25 - out_probe_x)
        
        out_atk_x_char = format_atk_output(out_fuse_x)
        out_atk_y_char = format_atk_output(out_fuse_y)
        
        log_messages.append(f"[Input ATT AOI XY]   -> CP Prober[X,Y]: [ {out_probe_x} , {out_probe_y} ]")
        log_messages.append(f"[Input ATT AOI XY]   -> CP Fuse  [X,Y]: [ {out_fuse_x} , {out_fuse_y} ]")
        log_messages.append(f"[Input ATT AOI XY]   -> ATK      [X,Y]: [ {out_atk_x_char} , {out_atk_y_char} ]")
    elif aoi_x is not None or aoi_y is not None:
        log_messages.append("[Input ATT AOI XY] Fail：Need input ATT AOI X and ATT AOI Y together。")
    else:
        log_messages.append("[Input ATT AOI XY] No input，Skip。")

    log_messages.append("- - - - - - - - -")

    # --- ATK 轉換邏輯 ---
    if atk_x is not None and atk_y is not None:
        out_probe_x = int(25 - atk_y)
        out_probe_y = int(atk_x)
        out_fuse_x = int(atk_x)
        out_fuse_y = int(atk_y)
        out_aoi_x = int(atk_x)
        out_aoi_y = int(25 - atk_y)
        
        log_messages.append(f"[Input ATK XY]       -> CP Prober[X,Y]: [ {out_probe_x} , {out_probe_y} ]")
        log_messages.append(f"[Input ATK XY]       -> CP Fuse  [X,Y]: [ {out_fuse_x} , {out_fuse_y} ]")
        log_messages.append(f"[Input ATK XY]       -> ATT AOI  [X,Y]: [ {out_aoi_x} , {out_aoi_y} ]")
    elif atk_x is not None or atk_y is not None:
        log_messages.append("[Input ATK XY] Fail：Need input ATK X and ATK Y together。")
    else:
        log_messages.append("[Input ATK XY] No input，Skip。")
        
    log_messages.append("----------------")

    # --- 顯示輸出結果 ---
    st.subheader("輸出訊息:")
    # 將 List 轉換為換行字串，顯示在程式碼區塊內
    st.code("\n".join(log_messages), language="plaintext")
