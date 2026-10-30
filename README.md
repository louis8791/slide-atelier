# slide-atelier

上傳講稿和照片，按一下，自動產出 3 個版本的繁體中文 16:9 簡報（PDF 與可編輯的 PPTX），並且可以逐頁修改。在自己的 Mac 上執行，完全免費。

這個 repo 只放**引擎**（MIT 授權）。版型、色票、品味規則放在私人 repo；沒有私人 repo 時，引擎會使用公開的基本版型。

> 狀態：Phase 0（骨架）。還不能使用。

## 開發

```bash
uv sync
uv run pytest
uv run python -m app.hygiene .   # 檢查 repo 沒有混入使用者資料或機密
```

給 AI 開發助手的規則請看 [AGENTS.md](AGENTS.md)。
