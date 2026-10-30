"""O-04：repo 不能有使用者資料或機密；O-05：不能有安裝時自動執行的腳本（NFR-03、NFR-04）。"""
import json
from pathlib import Path

from app.hygiene import scan

REPO_ROOT = Path(__file__).resolve().parents[1]


def write(root: Path, rel: str, content: str = "x") -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_o04_clean_tree_has_no_findings(tmp_path):
    write(tmp_path, "app/main.py")
    write(tmp_path, "README.md")
    assert scan(tmp_path) == []


def test_o04_env_and_credentials_are_flagged(tmp_path):
    write(tmp_path, ".env", "KEY=1")
    write(tmp_path, "config/credentials.json", "{}")
    found = "\n".join(scan(tmp_path))
    assert ".env" in found and "credentials.json" in found


def test_o04_model_weights_are_flagged(tmp_path):
    write(tmp_path, "models/style.safetensors")
    assert any("safetensors" in f for f in scan(tmp_path))


def test_o04_user_material_folders_are_flagged(tmp_path):
    write(tmp_path, "test-materials/talk.md")
    write(tmp_path, "SlideAtelierData/users/u1/a.json")
    found = "\n".join(scan(tmp_path))
    assert "test-materials" in found and "SlideAtelierData" in found


def test_o04_photos_outside_allowed_folders_are_flagged(tmp_path):
    write(tmp_path, "uploads/IMG_0001.jpg")
    write(tmp_path, "tests/fixtures/synthetic/square.png")
    found = scan(tmp_path)
    assert any("IMG_0001.jpg" in f for f in found)
    assert not any("square.png" in f for f in found)


def test_o05_install_scripts_are_flagged(tmp_path):
    write(tmp_path, "renderer/package.json", json.dumps({"scripts": {"postinstall": "node x.js"}}))
    assert any("postinstall" in f for f in scan(tmp_path))


def test_o05_normal_scripts_are_fine(tmp_path):
    write(tmp_path, "renderer/package.json", json.dumps({"scripts": {"dev": "open-slide dev"}}))
    assert scan(tmp_path) == []


def test_o04_this_repository_is_clean():
    assert scan(REPO_ROOT) == []
