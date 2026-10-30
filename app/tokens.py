"""Validation for palette and font tokens (FR-11, FR-12).

The real palettes and font list live in the private repo; this module only knows the rules,
so the private repo's CI can run the same checks the engine relies on.
"""
from app.contrast import contrast_ratio

ROLES = ("bg", "surface", "ink", "muted", "accent", "accent2", "deep")

# (foreground role, background role, minimum ratio). accent is used as large text (3:1);
# accent2 is decorative and must read on the dark "deep" sections.
CONTRAST_RULES = (
    ("ink", "bg", 7.0),
    ("ink", "surface", 4.5),
    ("muted", "bg", 4.5),
    ("accent", "bg", 3.0),
    ("accent2", "deep", 3.0),
)

ALLOWED_FONT_LICENSES = {"OFL-1.1", "Apache-2.0", "TW-OGDL-1.0"}
MIN_FONTS = 10


def validate_palette(palette: dict) -> list[str]:
    pid = palette.get("id", "?")
    colors = palette.get("colors", {})
    errors = [f"{pid}: 缺少顏色角色 {r}" for r in ROLES if r not in colors]
    errors += [f"{pid}: 不認得的顏色角色 {r}" for r in colors if r not in ROLES]
    if errors:
        return errors
    for fg, bg, minimum in CONTRAST_RULES:
        ratio = contrast_ratio(colors[fg], colors[bg])
        if ratio < minimum:
            errors.append(f"{pid}: {fg}/{bg} 對比 {ratio:.2f} 低於 {minimum}")
    # Text on dark sections: the light text colour must stay readable on "deep".
    light_text = colors["bg"] if palette.get("kind") == "light" else colors["ink"]
    ratio = contrast_ratio(light_text, colors["deep"])
    if ratio < 7.0:
        errors.append(f"{pid}: deep 區塊上的文字對比 {ratio:.2f} 低於 7.0")
    return errors


def validate_fonts(fonts: list[dict]) -> list[str]:
    errors = []
    if len(fonts) < MIN_FONTS:
        errors.append(f"字體只有 {len(fonts)} 種，至少要 {MIN_FONTS} 種")
    seen: set[str] = set()
    for f in fonts:
        fid = f.get("id", "?")
        if fid in seen:
            errors.append(f"字體 id 重複：{fid}")
        seen.add(fid)
        if f.get("license") not in ALLOWED_FONT_LICENSES:
            errors.append(f"{fid}: 授權 {f.get('license')!r} 不在允許清單")
    return errors
