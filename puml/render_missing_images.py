from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render missing SVG and PNG images for PUML files in this folder."
    )
    parser.add_argument(
        "--jar",
        default=r"c:\Users\chattinr\.vscode\extensions\jebbs.plantuml-2.18.1\plantuml.jar",
        help="Path to plantuml.jar",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-render even if output image already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without rendering files.",
    )
    parser.add_argument(
        "--no-update-index",
        action="store_true",
        help="Do not update puml/index.html references after rendering.",
    )
    parser.add_argument(
        "--github-base-url",
        default=None,
        metavar="URL",
        help=(
            "When set, index.html image src and source href attributes are rewritten to "
            "absolute GitHub raw/blob URLs instead of local relative paths. "
            "Example: https://raw.githubusercontent.com/indraykk83/dre-design/main/puml"
        ),
    )
    return parser.parse_args()


def render_one(puml_path: Path, out_path: Path, jar_path: Path, mode: str, scale: str | None = None) -> tuple[bool, str]:
    cmd = [
        "java",
        "-DPLANTUML_LIMIT_SIZE=8192",
        "-jar",
        str(jar_path),
        mode,
        "-pipe",
    ]
    if scale is not None:
        cmd.extend(["-scale", scale])

    proc = subprocess.run(
        cmd,
        input=puml_path.read_bytes(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return False, proc.stderr.decode("utf-8", errors="ignore").strip()

    out_path.write_bytes(proc.stdout)
    return True, ""


def update_index_references(
    index_path: Path,
    puml_dir: Path,
    out_png_dir: Path,
    dry_run: bool,
    github_base_url: str | None = None,
) -> tuple[int, int, int]:
    """Update index.html image src and source href attributes.

    When github_base_url is provided (e.g. 'https://raw.githubusercontent.com/owner/repo/main/puml'),
    references are rewritten to absolute GitHub raw/blob URLs so the page works when
    committed and viewed on GitHub or GitHub Pages.

    Without github_base_url, references are rewritten to local relative paths.

    Returns tuple: (source_links_updated, image_links_updated, unchanged_or_missing)
    """
    if not index_path.exists():
        return (0, 0, 0)

    available = {p.name for p in puml_dir.glob("*.puml")}
    available_png_stems = {p.stem for p in out_png_dir.glob("*.png")}
    html = index_path.read_text(encoding="utf-8")

    source_updates = 0
    image_updates = 0
    missing_or_unchanged = 0

    def _source_href(name: str) -> str:
        """Return the target href for a .puml source link."""
        if github_base_url:
            # GitHub blob URL so the source renders with syntax highlighting
            blob_base = github_base_url.replace(
                "raw.githubusercontent.com", "github.com"
            ).replace("/main/", "/blob/main/").replace("/refs/heads/", "/blob/")
            # Ensure /blob/ is present
            if "/blob/" not in blob_base:
                blob_base = blob_base.rstrip("/")
            return f"{blob_base.rstrip('/')}/{name}"
        return f"./{name}"

    def _img_src(stem: str) -> str:
        """Return the target src for a rendered PNG image."""
        if github_base_url:
            return f"{github_base_url.rstrip('/')}/{stem}.png"
        return f"./png/{stem}.png"

    def _replace_source(match: re.Match) -> str:
        nonlocal source_updates, missing_or_unchanged
        prefix, name, suffix = match.group(1), match.group(2), match.group(3)
        if name in available:
            new_href = _source_href(name)
            if f'{prefix}{new_href}{suffix}' == match.group(0):
                missing_or_unchanged += 1
                return match.group(0)
            source_updates += 1
            return f'{prefix}{new_href}{suffix}'
        missing_or_unchanged += 1
        return match.group(0)

    def _replace_img_puml(match: re.Match) -> str:
        nonlocal image_updates, missing_or_unchanged
        prefix, stem, suffix = match.group(1), match.group(2), match.group(3)
        if stem in available_png_stems:
            new_src = _img_src(stem)
            if f'{prefix}{new_src}{suffix}' == match.group(0):
                missing_or_unchanged += 1
                return match.group(0)
            image_updates += 1
            return f'{prefix}{new_src}{suffix}'
        missing_or_unchanged += 1
        return match.group(0)

    def _replace_img_png(match: re.Match) -> str:
        nonlocal image_updates, missing_or_unchanged
        prefix, stem, suffix = match.group(1), match.group(2), match.group(3)
        if stem in available_png_stems:
            new_src = _img_src(stem)
            if f'{prefix}{new_src}{suffix}' == match.group(0):
                missing_or_unchanged += 1
                return match.group(0)
            image_updates += 1
            return f'{prefix}{new_src}{suffix}'
        missing_or_unchanged += 1
        return match.group(0)

    # Convert raw GitHub PUML source links to local ./<name>.puml
    html = re.sub(
        r'(href=")https?://raw\.githubusercontent\.com/[^"]*/([^"/]+\.puml)(")',
        _replace_source,
        html,
        flags=re.IGNORECASE,
    )

    # Convert GitHub blob PUML source links to local ./<name>.puml
    html = re.sub(
        r'(href=")https?://github\.com/[^"]*/blob/[^"]*/([^"/]+\.puml)(")',
        _replace_source,
        html,
        flags=re.IGNORECASE,
    )

    # Convert PlantUML proxy image URLs that reference .../puml/<name>.puml to local rendered png.
    html = re.sub(
        r'(<img[^>]*\ssrc=")[^"]*?([^"/]+)\.puml[^"]*(")',
        _replace_img_puml,
        html,
        flags=re.IGNORECASE,
    )

    # Convert /puml/<name>.png to local rendered png path.
    html = re.sub(
        r'(<img[^>]*\ssrc=")(?:\./|\.\./)?/?puml/([^"/]+)\.png(")',
        _replace_img_png,
        html,
        flags=re.IGNORECASE,
    )

    # Convert raw GitHub PNG image links to local rendered png path.
    html = re.sub(
        r'(<img[^>]*\ssrc=")https?://raw\.githubusercontent\.com/[^"]*/([^"/]+)\.png(")',
        _replace_img_png,
        html,
        flags=re.IGNORECASE,
    )

    # Convert existing local relative PNG paths (../diagrams/rendered/png/NAME.png or ./png/NAME.png).
    html = re.sub(
        r'(<img[^>]*\ssrc=")[^"]*(?:diagrams/rendered/png|(?:\./)?png)/([^"/]+)\.png(")',
        _replace_img_png,
        html,
        flags=re.IGNORECASE,
    )

    # Convert existing local relative PUML source hrefs (./NAME.puml).
    html = re.sub(
        r'(href=")\./([^"/]+\.puml)(")',
        _replace_source,
        html,
        flags=re.IGNORECASE,
    )

    if not dry_run:
        index_path.write_text(html, encoding="utf-8")

    return source_updates, image_updates, missing_or_unchanged


def main() -> int:
    args = parse_args()

    puml_dir = Path(__file__).resolve().parent
    out_svg = puml_dir / "svg"
    out_png = puml_dir / "png"
    index_html = puml_dir / "index.html"
    out_svg.mkdir(parents=True, exist_ok=True)
    out_png.mkdir(parents=True, exist_ok=True)

    jar = Path(args.jar)
    if not jar.exists():
        print(f"ERROR: PlantUML jar not found: {jar}")
        return 1

    pumls = sorted(puml_dir.glob("*.puml"))
    if not pumls:
        print(f"No PUML files found in: {puml_dir}")
        return 0

    created_svg = 0
    created_png = 0
    skipped_svg = 0
    skipped_png = 0
    failed = 0

    for puml in pumls:
        stem = puml.stem
        svg_path = out_svg / f"{stem}.svg"
        png_path = out_png / f"{stem}.png"

        if args.overwrite or not svg_path.exists():
            if args.dry_run:
                print(f"DRY-RUN SVG: {puml.name} -> {svg_path}")
                created_svg += 1
            else:
                ok, err = render_one(puml, svg_path, jar, "-tsvg")
                if ok:
                    created_svg += 1
                else:
                    failed += 1
                    print(f"SVG FAIL: {puml.name}: {err}")
        else:
            skipped_svg += 1

        if args.overwrite or not png_path.exists():
            if args.dry_run:
                print(f"DRY-RUN PNG: {puml.name} -> {png_path}")
                created_png += 1
            else:
                ok, err = render_one(puml, png_path, jar, "-tpng", scale="2")
                if ok:
                    created_png += 1
                else:
                    failed += 1
                    print(f"PNG FAIL: {puml.name}: {err}")
        else:
            skipped_png += 1

    print("DONE")
    print(f"PUML files: {len(pumls)}")
    print(f"SVG created: {created_svg}, skipped(existing): {skipped_svg}")
    print(f"PNG created: {created_png}, skipped(existing): {skipped_png}")
    print(f"Failures: {failed}")
    print(f"SVG out: {out_svg}")
    print(f"PNG out: {out_png}")

    if not args.no_update_index:
        src_u, img_u, miss = update_index_references(
            index_html, puml_dir, out_png, args.dry_run, args.github_base_url
        )
        mode_label = f"github ({args.github_base_url})" if args.github_base_url else "local relative"
        print(f"Index updated: {index_html}")
        print(f"Index ref mode: {mode_label}")
        print(f"Index refs updated - sources: {src_u}, images: {img_u}, missing/unchanged: {miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
