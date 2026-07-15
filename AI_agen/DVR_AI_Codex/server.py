"""
DVR AI 代理伺服器
功能：
  1. 靜態檔案服務（HTML、JS、模型）
  2. /api/login  — 代為向 DVR 登入並保持 session
  3. /api/snapshot?ch=X — 從 DVR 抓取截圖後回傳給前端（解決 CORS）
啟動方式：
  pip install flask requests
  python server.py
瀏覽器開啟：http://localhost:8000
"""

from flask import Flask, request, Response, send_from_directory, jsonify
import base64
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import os
import re
import warnings

warnings.filterwarnings('ignore')   # 忽略 SSL 憑證警告

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_DIR = os.path.join(BASE_DIR, 'captures')
DVR_BASE = 'http://your_dvr_ip:port'

# 保存 DVR 連線 session（含 cookie / auth）
dvr_session = requests.Session()
dvr_creds = {'username': '', 'password': ''}
is_authenticated = False


# ── 全域 CORS 標頭 ─────────────────────────────────────────────────────────
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# ── 登入 API ──────────────────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def api_login():
    global is_authenticated
    data = request.get_json(force=True)
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    dvr_creds['username'] = username
    dvr_creds['password'] = password

    # 依序嘗試 Basic Auth → Digest Auth
    for auth_cls in (HTTPBasicAuth, HTTPDigestAuth):
        dvr_session.auth = auth_cls(username, password)
        try:
            resp = dvr_session.get(
                f'{DVR_BASE}/m.html?ch=0',
                timeout=8,
                verify=False,
                allow_redirects=True
            )
            if resp.status_code == 200:
                is_authenticated = True
                return jsonify({'success': True, 'message': '登入成功'})
        except Exception as exc:
            return jsonify({'success': False, 'error': str(exc)})

    is_authenticated = False
    return jsonify({'success': False, 'error': '帳號或密碼錯誤，或 DVR 無法連線'})


# ── 截圖代理 API ──────────────────────────────────────────────────────────
@app.route('/api/snapshot')
def api_snapshot():
    if not is_authenticated:
        return Response('尚未登入 DVR', status=401)

    ch = request.args.get('ch', '1')
    ch0 = str(int(ch) - 1)   # 部分 DVR 用 0-based channel index
    u = dvr_creds['username']
    p = dvr_creds['password']

    # 常見 DVR 截圖 URL 樣式（依序嘗試）
    snapshot_candidates = [
        f'{DVR_BASE}/snapshot?ch={ch}&type=0',
        f'{DVR_BASE}/snapshot.cgi?channel={ch}',
        f'{DVR_BASE}/cgi-bin/snapshot.cgi?channel={ch}',
        f'{DVR_BASE}/cgi-bin/currentpic.cgi?channel={ch}',
        f'{DVR_BASE}/cgi-bin/hi3510/snap.cgi?chn={ch0}&u={u}&p={p}',
        f'{DVR_BASE}/snap.cgi?chn={ch0}',
        f'{DVR_BASE}/webcapture.jpg?command=snap&channel={ch}',
        f'{DVR_BASE}/cgi-bin/net_jpeg.cgi?ch={ch0}',
        f'{DVR_BASE}/tmpfs/auto.jpg',
    ]

    for url in snapshot_candidates:
        try:
            resp = dvr_session.get(url, timeout=5, verify=False)
            ct = resp.headers.get('Content-Type', '')
            is_jpeg = resp.content[:3] == b'\xff\xd8\xff'
            if resp.status_code == 200 and ('image' in ct or is_jpeg):
                return Response(
                    resp.content,
                    content_type='image/jpeg',
                    headers={
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0'
                    }
                )
        except Exception:
            continue

    return Response('找不到有效的截圖端點', status=404)


# ── AI 觸發拍照存檔 API ───────────────────────────────────────────────────
@app.route('/api/save-photo', methods=['POST'])
def api_save_photo():
    data = request.get_json(force=True)
    image_data = data.get('image', '')

    match = re.match(r'^data:image/(jpeg|jpg);base64,(.+)$', image_data)
    if not match:
        return jsonify({'success': False, 'error': '圖片格式錯誤'})

    try:
        os.makedirs(CAPTURE_DIR, exist_ok=True)

        existing_numbers = []
        for filename in os.listdir(CAPTURE_DIR):
            file_match = re.match(r'^(\d+)(?:_\d{8}_\d{6})?\.jpg$', filename)
            if file_match:
                existing_numbers.append(int(file_match.group(1)))

        next_number = max(existing_numbers, default=0) + 1
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{next_number}_{timestamp}.jpg'
        save_path = os.path.join(CAPTURE_DIR, filename)

        with open(save_path, 'wb') as photo_file:
            photo_file.write(base64.b64decode(match.group(2)))

        return jsonify({
            'success': True,
            'filename': filename,
            'path': os.path.relpath(save_path, BASE_DIR).replace('\\', '/')
        })
    except Exception as exc:
        return jsonify({'success': False, 'error': str(exc)})


# ── 靜態檔案服務 ───────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'DVR_canvas_AI.html')


@app.route('/<path:path>')
def static_files(path):
    try:
        return send_from_directory(BASE_DIR, path)
    except Exception:
        return Response('Not Found', status=404)


# ── 主程式 ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('=' * 55)
    print('  DVR AI 監視器代理伺服器')
    print('  請在瀏覽器開啟：http://localhost:8000')
    print('=' * 55)
    app.run(host='0.0.0.0', port=8000, debug=False)
