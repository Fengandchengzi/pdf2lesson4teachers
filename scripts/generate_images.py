#!/usr/bin/env python3
"""
pdf2lesson4teachers AI 图片生成脚本

按需替换用户不满意的图片，每次只处理一张。
支持传入教材截图作为参考图，使生成图与教材风格一致。

用法:
    # 从大纲条目自动拼 prompt 生成
    python3 generate_images.py --id img_hand_up --desc "student raising hand" --usage "规则主图"

    # 附带教材截图作为风格参考
    python3 generate_images.py --id img_hand_up --desc "student raising hand" --usage "规则主图" \
        --reference ~/pdf2lesson4teachers/input/U1P1.jpg

    # 加用户反馈（覆盖默认风格）
    python3 generate_images.py --id img_hand_up --desc "student raising hand" --usage "规则主图" \
        --feedback "要真实照片风格，不要卡通"

    # 自定义 prompt（跳过模板）
    python3 generate_images.py --id img_hand_up --prompt "A real photo of a student raising hand"

    # 用户满意后，确认覆盖原图
    python3 generate_images.py --confirm --confirm-id img_hand_up

流程: 生成到 images_preview/ → 用户查看 → 满意则 --confirm 覆盖到 images/
"""

import argparse
import base64
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen  # noqa: S310

API_URL = "https://api.laozhang.ai/v1/chat/completions"
MODEL = "gemini-3-pro-image-preview"
DEFAULT_OUTPUT_DIR = Path.home() / "pdf2lesson4teachers" / "output" / "images"
DEFAULT_PREVIEW_DIR = Path.home() / "pdf2lesson4teachers" / "output" / "images_preview"
MAX_RETRIES = 2

# usage → 尺寸映射
USAGE_SIZE_MAP = {
    "词汇主图": "square format, 1:1 aspect ratio",
    "规则主图": "square format, 1:1 aspect ratio",
    "全屏背景图": "wide format, 16:9 aspect ratio",
    "封面背景": "wide format, 16:9 aspect ratio",
    "情景图": "landscape format, 4:3 aspect ratio",
    "背景图": "wide format, 16:9 aspect ratio",
    "网格缩略图": "square format, 1:1 aspect ratio",
}

DEFAULT_STYLE = (
    "Style: bright, clean, child-friendly illustration "
    "suitable for elementary school ESL classroom. "
    "White or simple background. No text in the image."
)


def build_prompt(desc: str, usage: str, feedback: str = "",
                 style_dna: str = "") -> str:
    """从大纲字段 + 风格DNA/用户反馈拼接完整 prompt"""
    size_hint = USAGE_SIZE_MAP.get(usage, "square format, 1:1 aspect ratio")

    parts = [f"Generate an image: {desc}."]

    if feedback:
        # 用户反馈最高优先级
        parts.append(f"Style requirements: {feedback}")
    elif style_dna:
        # 教材视觉DNA风格定调
        parts.append(style_dna)
    else:
        parts.append(DEFAULT_STYLE)

    parts.append(f"NOT photorealistic. No text in the image.")
    parts.append(f"Format: {size_hint}")
    return "\n".join(parts)


def load_reference_image(ref_path: str) -> dict | None:
    """加载参考图为 base64，返回 API content 格式"""
    path = Path(ref_path)
    if not path.exists():
        print(f"  警告: 参考图不存在: {path}", file=sys.stderr)
        return None

    with open(path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")

    ext = path.suffix.lower()
    media_type = {"jpg": "image/jpeg", ".jpg": "image/jpeg",
                  ".jpeg": "image/jpeg", ".png": "image/png"}.get(ext, "image/jpeg")

    return {
        "type": "image_url",
        "image_url": {"url": f"data:{media_type};base64,{img_data}"}
    }


def call_image_api(prompt: str, api_key: str,
                    ref_image: dict | None = None) -> tuple[bytes, str]:
    """调用 AI 生图 API，返回 (图片bytes, 格式名如'jpeg')"""
    if ref_image:
        # 图+文多模态输入：参考图 + prompt
        content = [ref_image, {"type": "text", "text": prompt}]
    else:
        content = prompt

    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
    }).encode("utf-8")

    req = Request(
        API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(1 + MAX_RETRIES):
        if attempt > 0:
            print(f"  重试第 {attempt} 次...", file=sys.stderr)
            time.sleep(3)

        try:
            with urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            content = data["choices"][0]["message"]["content"]
            match = re.search(r'data:image/(\w+);base64,(.+?)\)', content)
            if not match:
                print("  警告: API 返回中未找到图片数据", file=sys.stderr)
                print(f"  返回内容前200字: {content[:200]}", file=sys.stderr)
                return b"", ""

            fmt = match.group(1)
            b64_data = match.group(2)
            return base64.b64decode(b64_data), fmt

        except HTTPError as e:
            last_error = e
            error_body = e.read().decode("utf-8", errors="replace")
            if e.code == 401:
                print("错误: API Key 无效或已过期", file=sys.stderr)
                sys.exit(1)
            elif e.code == 402 or "insufficient" in error_body.lower():
                print("错误: API 余额不足，请充值后重试", file=sys.stderr)
                sys.exit(1)
            elif e.code == 429:
                print("  请求频率过高，等待后重试...", file=sys.stderr)
                time.sleep(10)
                continue
            else:
                print(f"  API 错误 (HTTP {e.code}): {error_body[:200]}", file=sys.stderr)

        except (URLError, TimeoutError) as e:
            last_error = e
            print(f"  网络错误: {e}", file=sys.stderr)

    print(f"生成失败，已重试 {MAX_RETRIES} 次: {last_error}", file=sys.stderr)
    return b"", ""


def generate_single(image_id: str, prompt: str, output_dir: Path,
                    api_key: str, ref_image: dict | None = None) -> bool:
    """生成单张图片，返回是否成功"""
    print(f"  生成: {image_id}...", file=sys.stderr)
    print(f"  Prompt: {prompt[:100]}...", file=sys.stderr)
    if ref_image:
        print(f"  参考图: 已附带", file=sys.stderr)

    img_bytes, fmt = call_image_api(prompt, api_key, ref_image)
    if not img_bytes:
        return False

    ext = "jpg" if fmt == "jpeg" else fmt
    out_path = output_dir / f"{image_id}.{ext}"
    out_path.write_bytes(img_bytes)
    print(f"  已保存: {out_path} ({len(img_bytes) / 1024:.0f}KB)", file=sys.stderr)
    return True


def confirm_and_copy(preview_dir: Path, output_dir: Path, image_id: str):
    """将单张预览图覆盖到正式目录"""
    output_dir.mkdir(parents=True, exist_ok=True)
    found = False
    for f in preview_dir.iterdir():
        if f.stem == image_id and f.is_file():
            dest = output_dir / f.name
            shutil.copy2(f, dest)
            print(f"确认: {f.name} → {dest}", file=sys.stderr)
            found = True
            break
    if not found:
        print(f"错误: 预览目录中未找到 {image_id}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="pdf2lesson4teachers AI图片生成：按需生成/替换PPT图片"
    )

    # 生成模式
    parser.add_argument("--id", help="图片 ID（如 img_hand_up）", required=False)
    parser.add_argument("--desc", help="图片描述（大纲 desc 字段）")
    parser.add_argument("--usage", default="词汇主图", help="图片用途（大纲 usage 字段）")
    parser.add_argument("--prompt", help="自定义 prompt（跳过模板拼接）")
    parser.add_argument("--feedback", default="", help="用户反馈（覆盖默认风格）")
    parser.add_argument("--reference", "-r", help="教材截图路径，作为风格参考图传给 API")
    parser.add_argument("--style-dna", default="",
                        help="视觉DNA风格定调句（替代默认风格模板）")

    # 确认模式
    parser.add_argument("--confirm", action="store_true",
                        help="将预览图确认覆盖到正式目录")
    parser.add_argument("--confirm-id", help="要确认的图片 ID")

    # 输出目录
    parser.add_argument("--output-dir", "-o", default=str(DEFAULT_OUTPUT_DIR),
                        help=f"正式图片目录 (默认: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--preview-dir", "-p", default=str(DEFAULT_PREVIEW_DIR),
                        help=f"预览图片目录 (默认: {DEFAULT_PREVIEW_DIR})")

    args = parser.parse_args()

    # --- 确认模式 ---
    if args.confirm:
        if not args.confirm_id:
            print("错误: --confirm 需要搭配 --confirm-id 指定图片 ID", file=sys.stderr)
            sys.exit(1)
        preview_dir = Path(args.preview_dir)
        output_dir = Path(args.output_dir)
        if not preview_dir.exists():
            print(f"错误: 预览目录不存在: {preview_dir}", file=sys.stderr)
            sys.exit(1)
        confirm_and_copy(preview_dir, output_dir, args.confirm_id)
        return

    # --- 生成模式 ---
    if not args.id:
        print("错误: 请提供 --id 指定要生成的图片 ID", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("LAOZHANG_API_KEY", "")
    if not api_key:
        print("错误: 未设置 LAOZHANG_API_KEY 环境变量", file=sys.stderr)
        print("请运行: export LAOZHANG_API_KEY='你的API密钥'", file=sys.stderr)
        sys.exit(1)

    preview_dir = Path(args.preview_dir)
    preview_dir.mkdir(parents=True, exist_ok=True)

    # 加载参考图
    ref_image = None
    if args.reference:
        ref_image = load_reference_image(args.reference)

    if args.prompt:
        prompt = args.prompt
    elif args.desc:
        prompt = build_prompt(args.desc, args.usage, args.feedback,
                              args.style_dna)
    else:
        print("错误: 请提供 --desc 或 --prompt", file=sys.stderr)
        sys.exit(1)

    if generate_single(args.id, prompt, preview_dir, api_key, ref_image):
        print(f"\n预览: {preview_dir}", file=sys.stderr)
        print(f"满意后运行: python3 {__file__} --confirm --confirm-id {args.id}",
              file=sys.stderr)
        print(str(preview_dir))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
