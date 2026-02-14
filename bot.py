import os
import telebot
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from datetime import datetime

# --- CẤU HÌNH ---
# Thay Token nhận được từ @BotFather vào đây
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN' 
CHAT_ID = '7346983056'
VN_TZ = timezone('Asia/Ho_Chi_Minh')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Trang chủ hiển thị trạng thái
@app.route('/')
def home():
    return "<h1>Bot Nhắc Nhở Học Tập Khối A</h1><p>Trạng thái: Đang hoạt động 24/7</p>", 200

# Trang Ping để giữ bot luôn thức (Dùng URL này cho UptimeRobot)
@app.route('/ping')
def ping():
    now_vn = datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        "status": "alive",
        "timezone": "Asia/Ho_Chi_Minh",
        "current_time_vn": now_vn
    }), 200

def send_remind(content):
    now_vn = datetime.now(VN_TZ).strftime("%H:%M")
    message = f"🔔 *[NHẮC NHỞ HỌC TẬP - {now_vn}]*\n\n{content}"
    try:
        bot.send_message(CHAT_ID, message, parse_mode='Markdown')
        print(f"[{now_vn}] Đã gửi thông báo.")
    except Exception as e:
        print(f"Lỗi gửi tin nhắn: {e}")

# Khởi tạo bộ lập lịch chạy ngầm
scheduler = BackgroundScheduler(timezone=VN_TZ)

# LỊCH TRÌNH CHI TIẾT
tasks = [
    ("05:00", "🌅 BẮT ĐẦU: Ôn nhanh công thức Toán/Lý/Hóa."),
    ("06:45", "☕ GIẢI LAO (15P): Nghỉ ngơi, chuẩn bị ăn sáng."),
    ("08:00", "📐 CA TOÁN (CHUYÊN ĐỀ): Học kỹ năng mới."),
    ("09:30", "🍎 GIẢI LAO (15P): Rời bàn học ngay."),
    ("09:45", "📝 CA TOÁN (LUYỆN ĐỀ): Giải đề 90 phút."),
    ("11:15", "🍱 NGHỈ TRƯA: Ăn cơm và NGỦ TRƯA ít nhất 30-45p."),
    ("12:45", "⚡ CA VẬT LÝ: Giải bài tập chương."),
    ("14:15", "🥤 GIẢI LAO (15P): Nghỉ ngơi nhẹ."),
    ("14:30", "🧪 CA HÓA HỌC: Luyện bảo toàn, quy đổi."),
    ("16:00", "📖 GIẢI LAO (15P): Vận động chuẩn bị tổng ôn."),
    ("16:15", "✍️ TỔNG ÔN LỖI SAI: Ghi vào sổ tay."),
    ("17:30", "🏐 BÓNG CHUYỀN: Đi đánh bóng thôi! Xả stress."),
    ("19:45", "🤝 HỌC NHÓM/ONLINE: Trao đổi bài khó."),
    ("21:30", "☕ GIẢI LAO (15P): Nghỉ ngơi chuẩn bị cày đêm."),
    ("21:45", "📄 LUYỆN ĐỀ TỔNG HỢP: Làm đề Lý hoặc Hóa."),
    ("23:15", "🥪 GIẢI LAO (15P): Ăn nhẹ."),
    ("23:30", "🔥 VẬN DỤNG CAO: Chinh phục điểm 9-10!"),
    ("01:30", "😴 ĐI NGỦ: Chúc bạn ngủ ngon!")
]

for time_str, content in tasks:
    h, m = map(int, time_str.split(':'))
    scheduler.add_job(send_remind, 'cron', hour=h, minute=m, args=[content])

scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
