import uiautomator2 as u2
import time
import os
import config # 接入朱文凯的动态配置

def capture_current_screen(device, filename_prefix="app"):
    """抓取截图和XML，存入对应的 data_collection_xxx 目录"""
    save_path = config.SAVE_DIR
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_name = f"{filename_prefix}_{timestamp}"
    
    # 1. 保存 XML (View Hierarchy)
    try:
        xml_content = device.dump_hierarchy()
        xml_path = os.path.join(save_path, f"{base_name}.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"[Success] XML saved: {xml_path}")
    except Exception as e:
        print(f"[Error] Failed to dump XML: {e}")
        return

    # 2. 保存截图
    try:
        img_path = os.path.join(save_path, f"{base_name}.jpg")
        device.screenshot(img_path)
        print(f"[Success] Screenshot saved: {img_path}")
    except Exception as e:
        print(f"[Error] Failed to take screenshot: {e}")

def main():
    print(f"Connecting to STF Device: {config.DEVICE_ADDR}...")
    try:
        d = u2.connect(config.DEVICE_ADDR)
        print(f"Connected! Current App Target: {config.APP_NAME}")
        
        while True:
            cmd = input(f"\n👉 [{config.APP_NAME}] Press Enter to capture, or 'q' to quit: ")
            if cmd.lower() == 'q':
                break
            prefix = cmd if cmd.strip() else config.APP_NAME
            capture_current_screen(d, prefix)
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")

if __name__ == "__main__":
    main()