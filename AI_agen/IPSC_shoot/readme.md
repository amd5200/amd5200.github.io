# IPSC 戰術射擊計時器與計分系統 / IPSC Tactical Shot Timer & Scoring System

此技能提供一個完整的 HTML 網頁應用，用於 IPSC 射擊訓練。它包括：
- 麥克風槍聲偵測，提供精確計時
- 攝像頭或上傳靶紙進行擊中區域標記
- Hit Factor 計算（得分/時間）
- 透過 localStorage 持久化歷史紀錄
- 深色主題戰術 UI

## 使用方法 / Usage
1. 透過本地伺服器提供 HTML（例如 `python -m http.server`）以取得麥克風與相機權限。
2. 系統提示時授予麥克風與相機存取權。
3. 使用「計時器」分頁進行槍聲偵測與分割時間。
4. 使用「計分」分頁在靶紙圖片上標記擊中位置。
5. 在「歷史」分頁檢視過去紀錄。

## 自訂 / Customization
- 在計時器設定中調整槍聲偵測門檻值。
- 編輯 `updateScoringUI()` 與 `calculateHitFactor()` 函式以修改計分規則。
- 修改 HTML 中的 Tailwind 設定來變更 UI 顏色。

## 參考 / Reference
請參閱 `references/ipsc_tactical_shot_timer_scoring.html` 以取得完整原始碼。
