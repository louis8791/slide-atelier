# AGENTS.md：slide-atelier（公開引擎 repo）

這份文件寫給在這個 repo 寫程式的 AI 助手（Claude Code、Antigravity 等）。

> **最高權限文件**：本專案的 AGENTS、PRD、ROADMAP、TDD、SPEC 五份文件是最高權限，正本由專案負責人保管，副本在私人 repo `slide-atelier-private/docs/`。**執行每一個步驟前，都要先把這五份讀過一次。** 本檔與五份文件衝突時，以五份文件為準。

## 這個 repo 的界線

- 只放引擎：Python app、pipeline、渲染器骨架、基本版型、Schema、測試。授權 MIT。
- **絕對不放**：品味規則、正式版型、色票、Skill、講稿、照片、AI 帳號憑證、`.env`、模型權重、訓練資料。
- CI 會跑 `python -m app.hygiene .` 擋下這些東西（TDD O-04、O-05）。

## 工作方式

1. 只做目前 ROADMAP 階段的工作；跨階段或換選型先問專案負責人。
2. 測試先行：先寫會失敗的測試，再寫程式碼。測試名稱帶需求編號（例如 `test_u10_...`、`test_o04_...`）。
3. 不能為了讓測試通過而跳過、停用或刪除測試。
4. 不確定的事標成「待驗證」，實測後才寫成確定。
5. 和專案負責人溝通用繁體中文。

## 絕對不能做的事

- 不用 `--dangerously-skip-permissions` 或任何跳過權限的參數。
- 不建立常駐程式（launchd、登入項目、cron）；模型不常駐記憶體。
- 不裁切使用者照片；照片一律完整顯示。
- 服務不綁定 `0.0.0.0`。
- 不用付費 API。
- Node 套件安裝一律 `pnpm install --ignore-scripts`。

## 新增相依套件

授權須為 MIT、Apache-2.0、BSD、ISC；近 12 個月有發布；不會在安裝時自動執行程式；能在 Apple Silicon 執行。能自己寫幾十行解決的就不加套件。PR 說明要列出檢查結果。

## 指令

```bash
uv sync
uv run pytest            # CI 會跑的部分
uv run pytest -m mac     # 需要模型，只在 Mac 上跑
uv run pytest -m live    # 會消耗 AI 額度，執行前先問
uv run ruff check .
uv run python -m app.hygiene .
```
