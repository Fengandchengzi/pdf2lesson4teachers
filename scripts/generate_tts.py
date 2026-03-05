#!/usr/bin/env python3
"""
pdf2lesson4teachers TTS 批量生成脚本

调用 laozhang.ai TTS-1 HD API，将 tts_manifest.json 中的文本批量生成为 MP3 文件。

用法:
    python3 generate_tts.py --manifest tts_manifest.json --output-dir ./audio
    python3 generate_tts.py --manifest tts_manifest.json --voice nova --speed 0.85
    cat tts_manifest.json | python3 generate_tts.py --stdin --output-dir ./audio
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://api.laozhang.ai/v1/audio/speech"
DEFAULT_OUTPUT_DIR = Path.home() / "pdf2lesson4teachers" / "output" / "audio"
DEFAULT_VOICE = "shimmer"
DEFAULT_SPEED = 0.9
DEFAULT_SLOW_SPEED = 0.6
MAX_RETRIES = 2


def call_tts(text: str, voice: str, speed: float, api_key: str) -> bytes:
    """调用 TTS-1 HD API，返回 MP3 音频 bytes"""
    body = json.dumps({
        "model": "tts-1-hd",
        "input": text,
        "voice": voice,
        "speed": speed,
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
            time.sleep(2)

        try:
            with urlopen(req, timeout=60) as resp:
                return resp.read()

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
                time.sleep(5)
                continue
            else:
                print(f"  API 错误 (HTTP {e.code}): {error_body[:200]}", file=sys.stderr)

        except (URLError, TimeoutError) as e:
            last_error = e
            print(f"  网络错误: {e}", file=sys.stderr)

    print(f"生成失败，已重试 {MAX_RETRIES} 次: {last_error}", file=sys.stderr)
    return b""


def load_manifest(args: argparse.Namespace) -> list[dict]:
    """从文件或 stdin 加载 manifest"""
    if args.stdin:
        if sys.stdin.isatty():
            print("错误: --stdin 模式但未检测到管道输入", file=sys.stderr)
            sys.exit(1)
        return json.loads(sys.stdin.read())

    if not args.manifest:
        print("错误: 请通过 --manifest 或 --stdin 提供 TTS 清单", file=sys.stderr)
        sys.exit(1)

    path = Path(args.manifest)
    if not path.exists():
        print(f"错误: 清单文件不存在: {path}", file=sys.stderr)
        sys.exit(1)

    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(
        description="pdf2lesson4teachers TTS批量生成：manifest → API → MP3"
    )
    parser.add_argument("--manifest", "-m", help="JSON清单文件路径")
    parser.add_argument("--stdin", action="store_true", help="从stdin读取JSON")
    parser.add_argument(
        "--output-dir", "-o",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"音频输出目录 (默认: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE,
                        choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                        help=f"语音选择 (默认: {DEFAULT_VOICE})")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED,
                        help=f"普通语速 0.25-4.0 (默认: {DEFAULT_SPEED})")
    parser.add_argument("--slow-speed", type=float, default=DEFAULT_SLOW_SPEED,
                        help=f"慢速 0.25-4.0 (默认: {DEFAULT_SLOW_SPEED})")
    parser.add_argument("--force", action="store_true", help="强制重新生成已存在的文件")

    args = parser.parse_args()

    api_key = os.environ.get("LAOZHANG_API_KEY", "")
    if not api_key:
        print("错误: 未设置 LAOZHANG_API_KEY 环境变量", file=sys.stderr)
        print("请运行: export LAOZHANG_API_KEY='你的API密钥'", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(args)
    print(f"清单共 {len(manifest)} 条，输出目录: {output_dir}", file=sys.stderr)

    generated = 0
    skipped = 0
    failed = 0

    for item in manifest:
        name = item["name"]
        text = item["text"]
        speed_type = item.get("speed", "normal")

        out_path = output_dir / f"{name}.mp3"

        if out_path.exists() and not args.force:
            skipped += 1
            continue

        speed = args.slow_speed if speed_type == "slow" else args.speed
        voice = item.get("voice", args.voice)

        print(f"  生成: {name} ({len(text)}字, {speed_type}, {voice})...", file=sys.stderr)
        audio_bytes = call_tts(text, voice, speed, api_key)

        if audio_bytes:
            out_path.write_bytes(audio_bytes)
            generated += 1
        else:
            failed += 1

        # 避免请求过快
        time.sleep(0.3)

    print(f"\n完成: 生成 {generated}, 跳过 {skipped}, 失败 {failed}", file=sys.stderr)
    print(str(output_dir))


if __name__ == "__main__":
    main()
