# 🏋️‍♂️ 智能伏地挺身計數器 (MediaPipe Holistic)

> 使用 **MediaPipe Holistic** 進行全身姿勢與左右手部關鍵點偵測，結合手勢辨識（掌心揮動、食指點選、握拳）實現語言切換與計數歸零。介面採用深色玻璃磨砂設計，支援中英雙語切換，適合桌機與行動裝置。

---

## ✨ 功能特色

| 功能 | 說明 |
|------|------|
| **全身姿勢偵測** | MediaPipe Holistic 提供 33 個身體關鍵點（含鼻子、肩膀、手肘、手腕等），用於判斷伏地挺身的上下動作。 |
| **手部關鍵點偵測** | 偵測左右手的 21 個關節（手指尖、指關節、腕部），使得手勢辨識成為可能。 |
| **手勢辨識** | <ul><li>**掌心揮動**（水平滑動）：切換語言（中文/English）</li><li>**食指點選**（食指伸直，其他手指彎曲）：切換語言（同掌心揮動）</li><li>**握拳**（五指彎曲）：計數歸零並以語音報出 “0”</li></ul> |
| **即時語音回報** | 每完成一次標準推舉或觸發歸零手勢，使用 Web Speech API 以當前語言報出數字。 |
| **雙語介面** | 全頁文字（標題、提示、按鈕、Toast）可即時切換中文與英文。 |
| **視覺回饋** | <ul><li>鼻子點顏色：紅色＝下降階段，綠色＝上升階段。</li><li>肩部水平線：黃色虛線作為姿勢基準。</li><li>手肘角度數值顯示於右側儀表板。</li><li>食指游標與停留環（Dwell Ring）顯示點選狀態。</li></ul> |
| **響應式佈局** | 在寬度 ≥ 900px 時採用雙欄（左側畫布，右側資訊欄），較小螢幕則為單欄垂直堆疊。 |
| **零安裝** | 僅需開啟 `push_up_count.html` 即可使用，無需任何本地端安裝或建置步驟。 |

---

## 🚀 快速開始

1. **取得原始碼**  
   - 直接複製本倉庫，或下載 `push_up_count.html` 檔案。

2. **開啟網頁**  
   - 使用現代瀏覽器（Chrome、Edge、Safari、Firefox）開啟 `push_up_count.html`。  
   - 首次載入時瀏覽器會請求攝像頭權限，**請點擊「允許」**。  

3. **使用方式**  
   - 面對攝像頭，確保頭部、肩膀、手肘、手腕全部進鏡。  
   - 畫面左上角會顯示「載入 Holistic 模型…」；載入完成後即可開始做伏地挺身。  
   - 每完成一次正確的下降→上升動作（鼻子低於肩線且手肘伸展 ≥150°），計數器會遞增並以語音報出。  
   - 右側儀表板會即時顯示目前狀態（UP/DOWN）與左右手肘角度。  
   - **手勢操作**：  
     - 揮動手掌（左右水平滑動） → 語言在中文/English 間切換，畫面底部彈出提示 toast。  
     - 食指伸直、其他手指彎曲（點擊手勢） → 同上，切換語言。  
     - 握拳（五指彎曲） → 計數歸零，語音報出「0」，並顯示對應 toast。  
   - 食指游標會跟隨您的食指尖位置；當在同一位置停留約 1.2 秒時，會觸發點選事件（目前亦設為語言切換，可依需求修改）。  

4. **切換語言**  
   - 點擊右上角的 globe 圖示按鈕，亦可透過上述手勢切換中文與英文。

---

## 🛠️ 如何自行修改或擴展

### 變更偵測模型參數
在 `setup()` 函式中，`holistic.setOptions()` 可調整：
- `selfieMode`: 鏡像前鏡頭（預設 true）。
- `upperBodyOnly`: 僅偵測上半身以提升效能（預設 true）。
- `minDetectionConfidence` / `minTrackingConfidence`: 偵測與追蹤門檻（預設 0.5）。

### 調整計數門檻
- **直臂角度門檻**（目前 150°）：修改 `const STRAIGHT_ANGLE = 150;`（單位：度）。
- **鼻子‑肩膀垂直判斷**：目前使用 `noseY > shoulderY + 0.02`（下）與 `noseY < shoulderY - 0.02`（上），可依實際需求調整偏移量。

### 變更手勢行為
所有手勢相關邏輯位於 `processPoseAndGestures(results)` 函式內：
- **掌心揮動**（水平滑動）：透過腕部 x 座標變化量 `dx` 與時間間隔判斷，觸發 `toggleLanguage()`。
- **食指點選**：判斷食指伸直 (`indexTip.y < indexMcp.y`) 且其他手指彎曲，觸發 `toggleLanguage()`。
- **握拳**：所有指尖皆低於對應指關節（捲曲），觸發計數歸零。
- 若想改為其他功能（例如調節音量、切換背景顏色），只需在對應的 `if (isFist) { … }`、`if (isPoint) { … }` 或 swipe 分支內替換為你想執行的程式碼。

### 新增其他運動計數
1. 在 `processPoseAndGestures()` 中，依照你想偵測的關節（例如膝盖、腳踝）計算角度或相對位置。  
2. 加入新的狀態變數（例如 `squatState`）與對應的進入/退出條件。  
3. 當達到次數時，更新 UI (`updateCountUI()`) 並呼叫 `speakCount(count)`。  
4. 在儀表板 (`dashboard`) 新增對應的 `metric-card` 以顯示新計數或角度。

### 改善效能
- 將 `modelConfig.inputResolution` 調低（例如 256）可提升 FPS，但會降低關鍵點精度。  
- 若只需要特定關節（如肩膀、手肘、手腕），在取得 `results.poseLandmarks`、`results.leftHandLandmarks`、`results.rightHandLandmarks` 後，只保留你需要的索引，可減少後續運算量。  
- 開啟 `upperBodyOnly:true`（已預設）可減少不必要的全身關鍵點運算。

### 自訂 UI 主題
- 變更 CSS 變數（如顏色、圓角、陰影）即可快速換膚。  
- 主要顏色變數散見於 `.state-badge.up/.down`、`.metric-value`、手勢點等，統一修改即可。

---

## 🐞 常見問題排除

| 症狀 | 可能原因 | 解決方案 |
|------|----------|----------|
| 沒有啟動攝像頭，畫面保持黑色或灰色 | 瀏覽器未授權攝像頭或 `getUserMedia` 失敗 | 確認瀏覽器已授權該網站使用攝像頭（查看網址左側鎖頭圖示）；在開發者控制台 (F12) 查看 Console 是否有 `NotFoundError` 或 `NotAllowedError`；若是 HTTPS 問題，請確認頁面透過 `https://` 或 `localhost` 存取。 |
| 只有畫面，沒有骨架或手部關鍵點顯示 | 模型尚未載入完成或偵測失敗 | 打開開發者控制台查看 Console 是否有錯誤訊息（例如無法載入 `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/...`）。確認網路可連至 CDN；可嘗試刷新頁面或使用較快的網路。 |
| 手勢沒有反應 | 手勢門檻設定過嚴或關鍵點信心分數過低 | 手勢偵測使用 `LANDMARK_CONFIDENCE = 0.3`，若環境光線不好可調低此值（例如 0.2）於程式碼中；或在畫面上觀察手部關鍵點是否顯示（若未顯示則是偵測問題）。 |
| 語音沒有聲音 | 瀏覽器封鎖自動播放或未授權語音合成 | 點擊頁面任意位置後再嘗試手勢；或在瀏覽器設定中允許該網站使用語音合成（Speech Synthesis）。 |
| 計數不增加或誤判 | 姿勢門檻不適合您的體型或鏡頭角度 | 調整 `STRAIGHT_ANGLE`、鼻子‑肩膀偏移量（`0.02`）或肩部可見度門檻 (`POSE_CONFIDENCE`)。建議先在偵測畫面上打開除錯資訊（可暫時在 `processPoseAndGestures` 中加入 `console.log` 輸出關鍵點 y 座標與角度）以找出合適值。 |
| 在行動裝置上畫面被裁切或只有上半部 | `video.hide()` 後仍有其他元素遮蔽或縮放問題 | 確認 `video.style.display = 'none'` 已正確隱藏 `<video>` 元素；另外可在 `index.html` 最上方加入 `<meta name="viewport" content="width=device-width, initial-scale=1.0">`（已存在），必要時加入 `height: 100vh;` 於 `body`。 |

---

## 📁 檔案結構

```
push_up_count_Hermes/
├─ push_up_count.html    # 主程式（HTML、CSS、JS 全內嵌）
├─ push_up_count_backup.html  # 先前備用版本（可作參考或回溯）
└─ README.md             # 本說明文件
```

> **提示**：若想在本機測試不同版本，只需複製 `push_up_count.html` 為新檔名（例如 `push_up_count_v2.html`），直接用瀏覽器開啟即可。

---

## 📜 授權

本專案採用 **MIT 授權**，您可自由修改、分發及用於商業或非商業用途。  
詳細條款請參閱 `LICENSE` 檔（若未提供，預設為 MIT）。

---

> **祝您運動愉快，程式順利！**  
> 若有任何問題或改進建議，歡迎開啟 Issue 或直接提交 Pull Request。