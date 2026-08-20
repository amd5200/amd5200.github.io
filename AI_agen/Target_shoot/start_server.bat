@echo off
echo ===================================================
echo 正在啟動 靶紙射擊偵測系統 本機 Web 伺服器...
echo ===================================================
echo 請稍候，瀏覽器將自動開啟 http://localhost:8000/Target_shoot.html
echo (提示：請勿關閉此視窗，關閉視窗即停止網頁服務)
echo ===================================================

start http://localhost:8000/Target_shoot.html
python -m http.server 8000
pause
