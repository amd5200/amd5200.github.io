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

## 最近更新 (Recent Updates)
**1. 蜂鳴器聲音改為工業蜂鳴器/真實 IPSC 手持計時器聲音**  
   - 修改 `playBuzzerSound()` 使用 2850Hz 方波，模擬真實射擊計時器的尖銳聲音。

**2. 修正相機拍攝後畫面消失問題**  
   - 新增 `captureCameraSnapshot()` 函式，拍攝後將畫面定格為靜態圖像（`frozenTargetImage`），使得標記不會因畫面重繪而消失，可連續標記多個彈孔。

**3. 加入手動選擇標記區域功能**  
   - 增加區域選擇按鈕（A、C、D、M、NS），點擊即切換當前標記類型。  
   - 標記時只記錄在定格圖片上的點擊，並依所選區域增加對應計數（`hitCounts`），未標記則不計分。  
   - 提供復原最後一標記與清空所有標記按鈕。

**4. 客製化計分公式與設定記憶**  
   - 在計分頁面顯示确切計分公式：`Points = (A×Pa) + (C×Pc) + (D×Pd) - (M×Pm) - (NS×Pns) - (P×Pp)`  
   - Hit Factor 公式：`Hit Factor (HF) = Total Points / Time (秒)`  
   - 提開公式設定視窗，可自訂每個區域的分值（含倒扣分），並提供 Minor/Major 預設快速套用。  
   - 設定會儲存至 `localStorage`（key: `ipsc_scoring_rules`），下次開啟程式時自動載入。  
   - 同時將門檻值（threshold）也記憶於 localStorage（key: `ipsc_threshold`）。

**5. 增加紀錄署名，可記錄不同人員的成績**  
   - 在計分頁面頂部新增射手姓名/代號輸入框。  
   - 儲存紀錄時會將該姓名與成績一起寫入 localStorage 歷史紀錄，支援多射手切換記錄。

**6. 最後儲存的練習紀錄可以匯出.csv檔案**  
   - 在歷史頁面提供「匯出 CSV 檔案」按鈕。  
   - 匯出內容含有：射手姓名、日期時間、賽制分級、總用時、總擊發數、A/C/D/Miss/No-Shoot/Procedural 數量、總得分、Hit Factor。  
   - 檔案使用 UTF-8 BOM，可直接在 Excel 中正確顯示中文。

## 參考 / Reference
請參閱 `references/ipsc_tactical_shot_timer_scoring.html` 以取得完整原始碼。
