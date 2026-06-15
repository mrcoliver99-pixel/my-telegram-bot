import os
import sys
import subprocess
import threading
import time
import http.server
import socketserver

# 1. سيرفر ويب خفيف جداً لإرضاء منصة Render وإبقائها مستيقظة 24 ساعة
class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Athar Bot Engine is Active via Main Core!")

def run_health_server():
    # جلب المنفذ تلقائياً من نظام ريندر (الافتراضي 8080 أو حسب البيئة)
    PORT = int(os.environ.get("PORT", 8080))
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        print(f"[INFO] Health server started on port {PORT}", flush=True)
        httpd.serve_forever()

if __name__ == "__main__":
    # أ) تشغيل سيرفر الويب في الخلفية كسطر مستقل (Thread)
    threading.Thread(target=run_health_server, daemon=True).start()
    
    print("[SYSTEM] Launching your original run_bot.py...", flush=True)
    time.sleep(2)
    
    # ب) تشغيل ملفك الأصلي رغماً عن السيرفر وبشكل مستمر
    try:
        # هذا الأمر يعادل تماماً فتح الـ CMD وكتابة python run_bot.py على لابتوبك
        process = subprocess.Popen([sys.executable, "run_bot.py"])
        
        # إبقاء الملف الرئيسي حياً لمراقبة البوت وحمايته من التوقف
        process.wait()
    except Exception as e:
        print(f"[FATAL ERROR] {e}", file=sys.stderr, flush=True)
        while True:
            time.sleep(3600)
