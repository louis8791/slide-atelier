"""Repo hygiene scan (O-04, O-05): no user data, secrets, weights or install-time scripts.

Run in CI on both repos: `python -m app.hygiene <path>` exits non-zero on any finding.
"""
import json
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "dist"}
FORBIDDEN_DIRS = {"test-materials", "SlideAtelierData", "agy-home", "training"}
FORBIDDEN_NAMES = {".env", "credentials.json", "token.json", "oauth_creds.json"}
FORBIDDEN_SUFFIXES = {".safetensors", ".ckpt", ".gguf", ".pt", ".bin", ".onnx", ".pem", ".key"}
PHOTO_SUFFIXES = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".tif", ".tiff"}
# Images are allowed only where they are project assets, never user material.
PHOTO_ALLOWED_PREFIXES = ("tests/fixtures/synthetic/", "renderer/public/", "docs/assets/", "tests/visual-baseline/")
INSTALL_HOOKS = {"preinstall", "install", "postinstall", "prepare"}


def scan(root: Path) -> list[str]:
    root = Path(root)
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        rel_parts = path.relative_to(root).parts
        if any(p in SKIP_DIRS for p in rel_parts):
            continue
        rel = "/".join(rel_parts)
        if path.is_dir():
            if path.name in FORBIDDEN_DIRS:
                findings.append(f"不能進 repo 的資料夾：{rel}")
            continue
        if any(p in FORBIDDEN_DIRS for p in rel_parts[:-1]):
            continue  # already reported via its folder
        if path.name in FORBIDDEN_NAMES or path.name.startswith(".env."):
            findings.append(f"機密檔案：{rel}")
        elif path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"模型權重或金鑰：{rel}")
        elif path.suffix.lower() in PHOTO_SUFFIXES and not rel.startswith(PHOTO_ALLOWED_PREFIXES):
            findings.append(f"照片不能放在這裡：{rel}")
        elif path.name == "package.json":
            findings += _check_package_json(path, rel)
    return findings


def _check_package_json(path: Path, rel: str) -> list[str]:
    try:
        scripts = json.loads(path.read_text(encoding="utf-8")).get("scripts", {})
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [f"無法解析：{rel}"]
    return [f"安裝時會自動執行的腳本 {k}：{rel}" for k in scripts if k in INSTALL_HOOKS]


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    findings = scan(root)
    for f in findings:
        print(f)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
