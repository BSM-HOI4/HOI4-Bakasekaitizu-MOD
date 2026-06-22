#!/usr/bin/env python3
"""Generate the prestige rank badge sprite strip as an uncompressed 32-bit TGA."""

from __future__ import annotations

import math
import struct
from pathlib import Path


FRAME_SIZE = 64
FRAME_COUNT = 7
WIDTH = FRAME_SIZE * FRAME_COUNT
HEIGHT = FRAME_SIZE
SS = 4

OUTER_RADIUS = 29.5
INNER_RADIUS = 21.0
CENTER = (FRAME_SIZE - 1) / 2.0

TIERS = [
    {
        "name": "Insignificant",
        "rim_dark": (28, 29, 31),
        "rim": (70, 72, 75),
        "rim_light": (118, 121, 126),
        "center": (17, 18, 20, 218),
        "ornate": 0.00,
    },
    {
        "name": "Minor",
        "rim_dark": (39, 48, 55),
        "rim": (92, 105, 116),
        "rim_light": (151, 164, 176),
        "center": (18, 21, 24, 220),
        "ornate": 0.02,
    },
    {
        "name": "Middle",
        "rim_dark": (30, 58, 82),
        "rim": (65, 113, 154),
        "rim_light": (124, 178, 215),
        "center": (17, 22, 27, 222),
        "ornate": 0.04,
    },
    {
        "name": "Regional",
        "rim_dark": (78, 40, 20),
        "rim": (164, 91, 46),
        "rim_light": (230, 146, 73),
        "center": (24, 18, 15, 224),
        "ornate": 0.06,
    },
    {
        "name": "Major",
        "rim_dark": (78, 84, 91),
        "rim": (179, 188, 197),
        "rim_light": (250, 252, 254),
        "center": (19, 21, 24, 226),
        "ornate": 0.08,
    },
    {
        "name": "Great Power",
        "rim_dark": (108, 73, 10),
        "rim": (215, 168, 43),
        "rim_light": (255, 226, 100),
        "center": (25, 21, 13, 228),
        "ornate": 0.11,
    },
    {
        "name": "Superpower",
        "rim_dark": (143, 124, 61),
        "rim": (235, 226, 184),
        "rim_light": (255, 255, 238),
        "center": (27, 25, 19, 230),
        "ornate": 0.16,
    },
]


def clamp(value: float, lo: float = 0.0, hi: float = 255.0) -> int:
    return int(max(lo, min(hi, round(value))))


def smoothstep(edge0: float, edge1: float, value: float) -> float:
    if value <= edge0:
        return 0.0
    if value >= edge1:
        return 1.0
    x = (value - edge0) / (edge1 - edge0)
    return x * x * (3.0 - 2.0 * x)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[float, float, float]:
    return (
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
    )


def adjust(rgb: tuple[float, float, float], amount: float) -> tuple[float, float, float]:
    return (rgb[0] * amount, rgb[1] * amount, rgb[2] * amount)


def sample_badge(frame: int, x: float, y: float) -> tuple[int, int, int, int]:
    tier = TIERS[frame]
    dx = x - CENTER
    dy = y - CENTER
    radius = math.hypot(dx, dy)
    if radius > OUTER_RADIUS:
        return (0, 0, 0, 0)

    angle = math.atan2(dy, dx)
    # Screen-space upper left highlight direction.
    light_dir = -2.35
    light = (math.cos(angle - light_dir) + 1.0) * 0.5

    if radius >= INNER_RADIUS:
        band = (radius - INNER_RADIUS) / (OUTER_RADIUS - INNER_RADIUS)
        rgb = mix(tier["rim_dark"], tier["rim"], smoothstep(0.02, 0.55, band))
        rgb = mix(tuple(clamp(v) for v in rgb), tier["rim_light"], 0.28 * light)

        facet = max(0.0, math.cos(angle * 12.0)) ** 18.0
        rgb = mix(tuple(clamp(v) for v in rgb), tier["rim_light"], tier["ornate"] * facet)

        if radius > OUTER_RADIUS - 2.0:
            rgb = adjust(rgb, 0.55 + 0.20 * light)
        elif radius < INNER_RADIUS + 1.45:
            rgb = adjust(rgb, 0.62 + 0.22 * light)

        crescent = smoothstep(24.0, 27.0, radius) * (1.0 - smoothstep(27.0, 29.0, radius))
        crescent *= max(0.0, math.cos(angle - light_dir)) ** 8.0
        rgb = mix(tuple(clamp(v) for v in rgb), tier["rim_light"], 0.34 * crescent)
        return (clamp(rgb[0]), clamp(rgb[1]), clamp(rgb[2]), 255)

    center_rgb = tier["center"][:3]
    center_alpha = tier["center"][3]
    vignette = smoothstep(12.0, INNER_RADIUS, radius)
    inner_glow = max(0.0, math.cos(angle - light_dir)) * (1.0 - smoothstep(0.0, 19.0, radius))
    rgb = adjust(center_rgb, 0.92 - 0.22 * vignette + 0.14 * inner_glow)

    # Dark inner edge keeps white GUI numbers readable over every tier color.
    edge_shadow = smoothstep(INNER_RADIUS - 3.5, INNER_RADIUS, radius)
    rgb = adjust(rgb, 1.0 - 0.26 * edge_shadow)
    return (clamp(rgb[0]), clamp(rgb[1]), clamp(rgb[2]), center_alpha)


def render() -> bytearray:
    pixels = bytearray(WIDTH * HEIGHT * 4)
    offsets = [(sx, sy) for sy in range(SS) for sx in range(SS)]
    scale = SS * SS

    for y in range(HEIGHT):
        for x in range(WIDTH):
            frame = x // FRAME_SIZE
            local_x = x % FRAME_SIZE
            sum_r = 0.0
            sum_g = 0.0
            sum_b = 0.0
            sum_a = 0.0

            for sx, sy in offsets:
                sample_x = local_x + (sx + 0.5) / SS
                sample_y = y + (sy + 0.5) / SS
                r, g, b, a = sample_badge(frame, sample_x, sample_y)
                alpha = a / 255.0
                sum_r += r * alpha
                sum_g += g * alpha
                sum_b += b * alpha
                sum_a += a

            avg_a = sum_a / scale
            if avg_a > 0.0:
                alpha_factor = 255.0 / avg_a
                r = clamp((sum_r / scale) * alpha_factor)
                g = clamp((sum_g / scale) * alpha_factor)
                b = clamp((sum_b / scale) * alpha_factor)
                a = clamp(avg_a)
            else:
                r = g = b = a = 0

            offset = (y * WIDTH + x) * 4
            pixels[offset : offset + 4] = bytes((b, g, r, a))

    return pixels


def write_tga(path: Path, bgra_pixels: bytearray) -> None:
    header = struct.pack(
        "<BBBHHBHHHHBB",
        0,  # ID length
        0,  # color map type
        2,  # uncompressed true-color image
        0,
        0,
        0,
        0,
        0,
        WIDTH,
        HEIGHT,
        32,
        0x28,  # top-left origin + 8 alpha bits
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + bgra_pixels)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_path = repo_root / "bakasekai" / "gfx" / "interface" / "bsm_prestige_rank_strip.tga"
    write_tga(out_path, render())
    header = out_path.read_bytes()[:18]
    width, height, depth, descriptor = struct.unpack("<HHBB", header[12:18])
    print(f"{out_path} {width}x{height} depth={depth} descriptor=0x{descriptor:02x}")


if __name__ == "__main__":
    main()
