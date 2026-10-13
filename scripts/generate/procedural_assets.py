"""Create original procedural 2D cartoon scene art without any paid AI service."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw


W, H = 1080, 1920


def palette(index: int):
    sets = [
        ("#DDF4FF", "#8ED0FF", "#FFD66B", "#6BBF59"),
        ("#FFF1D6", "#FFC47A", "#FF8FA3", "#72C7A3"),
        ("#E9E1FF", "#BCA7FF", "#FFD166", "#6CC5D9"),
        ("#E8F7E8", "#9AD9A1", "#FFCB77", "#F28F8F"),
    ]
    return sets[index % len(sets)]


def draw_character(draw, x, y, scale, body, accent, facing=1, wave=False):
    s = scale
    # shadow
    draw.ellipse((x-95*s, y+175*s, x+95*s, y+225*s), fill="#00000020")
    # legs
    draw.rounded_rectangle((x-55*s, y+110*s, x-10*s, y+205*s), radius=18*s, fill="#5B6573")
    draw.rounded_rectangle((x+10*s, y+110*s, x+55*s, y+205*s), radius=18*s, fill="#5B6573")
    # body
    draw.ellipse((x-105*s, y-10*s, x+105*s, y+170*s), fill=body, outline="#344054", width=max(2, int(5*s)))
    # ears
    draw.ellipse((x-105*s, y-95*s, x-25*s, y-15*s), fill=accent, outline="#344054", width=max(2, int(5*s)))
    draw.ellipse((x+25*s, y-95*s, x+105*s, y-15*s), fill=accent, outline="#344054", width=max(2, int(5*s)))
    # head
    draw.ellipse((x-125*s, y-125*s, x+125*s, y+95*s), fill=accent, outline="#344054", width=max(2, int(5*s)))
    # eyes
    eye_dx = 42*s
    draw.ellipse((x-eye_dx-13*s, y-45*s, x-eye_dx+13*s, y-19*s), fill="#263238")
    draw.ellipse((x+eye_dx-13*s, y-45*s, x+eye_dx+13*s, y-19*s), fill="#263238")
    # smile
    draw.arc((x-48*s, y-5*s, x+48*s, y+55*s), 10, 170, fill="#263238", width=max(2, int(5*s)))
    # arms
    if wave:
        draw.line((x+85*s, y+55*s, x+150*s, y-15*s), fill=body, width=max(8, int(25*s)))
        draw.ellipse((x+138*s, y-38*s, x+170*s, y-6*s), fill=accent)
        draw.line((x-85*s, y+65*s, x-150*s, y+100*s), fill=body, width=max(8, int(25*s)))
    else:
        draw.line((x-85*s, y+65*s, x-150*s, y+100*s), fill=body, width=max(8, int(25*s)))
        draw.line((x+85*s, y+65*s, x+150*s, y+100*s), fill=body, width=max(8, int(25*s)))



def draw_bibi_details(draw, x, y, s):
    """Bibi: the channel's mint-green bunny kid with golden ears and teal overalls."""
    draw.ellipse((x-82*s, y-78*s, x-53*s, y-27*s), fill="#FF8EAB")
    draw.ellipse((x+53*s, y-78*s, x+82*s, y-27*s), fill="#FF8EAB")
    draw.rounded_rectangle((x-76*s, y+48*s, x+76*s, y+151*s),
                           radius=20*s, fill="#20A9A0", outline="#176F70", width=max(2, int(4*s)))
    draw.rounded_rectangle((x-59*s, y+23*s, x-35*s, y+72*s),
                           radius=8*s, fill="#20A9A0")
    draw.rounded_rectangle((x+35*s, y+23*s, x+59*s, y+72*s),
                           radius=8*s, fill="#20A9A0")
    draw.ellipse((x-15*s, y+78*s, x+15*s, y+108*s), fill="#FFD34D")
    draw.ellipse((x-78*s, y+1*s, x-49*s, y+21*s), fill="#FF9DAF")
    draw.ellipse((x+49*s, y+1*s, x+78*s, y+21*s), fill="#FF9DAF")


def draw_tiko_details(draw, x, y, s):
    """Tiko: the sky-blue turtle kid with a leafy shell and a sunny orange cap."""
    draw.ellipse((x-83*s, y-145*s, x+83*s, y-91*s), fill="#FF9A45", outline="#A95425", width=max(2, int(4*s)))
    draw.rounded_rectangle((x-96*s, y-112*s, x+96*s, y-94*s),
                           radius=8*s, fill="#F47C35")
    draw.rounded_rectangle((x-72*s, y+34*s, x+72*s, y+143*s),
                           radius=28*s, fill="#7BCB78", outline="#39865A", width=max(2, int(5*s)))
    draw.arc((x-48*s, y+47*s, x+48*s, y+125*s), 180, 360,
             fill="#39865A", width=max(2, int(4*s)))
    draw.line((x, y+42*s, x, y+137*s), fill="#39865A", width=max(2, int(4*s)))
    draw.rounded_rectangle((x+75*s, y+45*s, x+110*s, y+113*s),
                           radius=10*s, fill="#FFB34F", outline="#B96C30", width=max(2, int(3*s)))



def draw_momo(draw, x, y, s):
    """Momo: a peach-colored bird friend with a lilac cap and a sunny beak."""
    draw.ellipse((x-76*s, y-70*s, x-48*s, y-20*s), fill="#FFD16A")
    draw.ellipse((x+48*s, y-70*s, x+76*s, y-20*s), fill="#FFD16A")
    draw.ellipse((x-85*s, y-132*s, x+85*s, y+32*s), fill="#FFB18F", outline="#9A6657", width=max(2, int(4*s)))
    draw.ellipse((x-54*s, y-76*s, x-30*s, y-50*s), fill="#263238")
    draw.ellipse((x+30*s, y-76*s, x+54*s, y-50*s), fill="#263238")
    draw.arc((x-32*s, y-43*s, x+32*s, y-5*s), 5, 175, fill="#7A4A42", width=max(2, int(4*s)))
    draw.polygon([(x-9*s, y-35*s), (x+9*s, y-35*s), (x, y-18*s)], fill="#FFD34D")
    draw.ellipse((x-67*s, y-38*s, x-42*s, y-22*s), fill="#FF8FA3")
    draw.ellipse((x+42*s, y-38*s, x+67*s, y-22*s), fill="#FF8FA3")
    draw.ellipse((x-70*s, y-157*s, x+70*s, y-112*s), fill="#BCA7FF", outline="#7965B2", width=max(2, int(3*s)))
    draw.rounded_rectangle((x-82*s, y-125*s, x+82*s, y-111*s), radius=6*s, fill="#9D87E8")
    draw.ellipse((x-17*s, y-155*s, x+17*s, y-135*s), fill="#FFD34D")


def scene_background(draw, kind, sky, ground, accent):
    draw.rectangle((0, 0, W, H), fill=sky)
    if kind == "night":
        draw.ellipse((760, 150, 900, 290), fill="#FFF4B0")
        for px, py in [(120,180),(300,110),(540,230),(900,360),(690,90)]:
            draw.ellipse((px, py, px+14, py+14), fill="#FFFFFF")
        draw.rectangle((0, 1250, W, H), fill="#466B5B")
    elif kind == "water":
        draw.rectangle((0, 1150, W, H), fill="#62BCE8")
        for yy in range(1210, 1850, 100):
            for xx in range(40, W, 180):
                draw.arc((xx, yy, xx+100, yy+35), 180, 360, fill="#D8F4FF", width=5)
    elif kind == "home":
        draw.rectangle((0, 1250, W, H), fill=ground)
        draw.rectangle((170, 700, 910, 1420), fill="#FFF4D6", outline="#7B5E57", width=10)
        draw.polygon([(110,700),(540,300),(970,700)], fill=accent, outline="#7B5E57")
        draw.rectangle((460, 1050, 620, 1420), fill="#9A6B4F")
        draw.rectangle((250, 850, 430, 1030), fill="#BDE7FF")
        draw.rectangle((650, 850, 830, 1030), fill="#BDE7FF")
    elif kind == "garden":
        draw.rectangle((0, 1250, W, H), fill=ground)
        for x in [100, 900]:
            draw.rectangle((x, 820, x+40, 1300), fill="#7B5E57")
            draw.ellipse((x-90, 700, x+140, 920), fill="#65B85B")
            draw.ellipse((x-30, 620, x+190, 850), fill="#79C965")
        for x in range(80, 1000, 170):
            draw.ellipse((x, 1500, x+40, 1540), fill="#FF8FA3")
            draw.ellipse((x+35, 1480, x+75, 1520), fill="#FFD166")
    else:
        draw.rectangle((0, 1250, W, H), fill=ground)
        draw.ellipse((70, 220, 300, 450), fill="#FFFFFFAA")
        draw.ellipse((720, 300, 1000, 500), fill="#FFFFFFAA")


def choose_kind(prompt: str, order: int) -> str:
    p = prompt.lower()
    for word, kind in [("home","home"),("house","home"),("living room","home"),("bedroom","home"),
                       ("kitchen","home"),("playroom","home"),("table","home"),("reading nook","home"),
                       ("garden","garden"),("flower","garden"),("park","garden"),("playground","garden"),
                       ("field","garden"),("meadow","garden"),("neighborhood","garden"),("sidewalk","garden"),
                       ("beach","water"),("pond","water"),("water","water"),("river","water"),
                       ("night","night"),("moon","night"),("bed","home")]:
        if word in p:
            return kind
    return ["garden","home","water","garden","home","night"][max(0, order-1) % 6]


def make_scene(scene: dict, index: int, output: Path) -> None:
    bg, sky2, accent, ground = palette(index)
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    kind = choose_kind(scene.get("visualPrompt",""), int(scene.get("order", index + 1)))
    scene_background(draw, kind, bg, ground, accent)

    # Original recurring characters: round-eared friends, not based on an existing franchise.
    draw_character(draw, 360, 1050, 1.22, "#53C7A6", "#FFD34D", wave=index % 2 == 0)
    draw_bibi_details(draw, 360, 1050, 1.22)
    draw_character(draw, 730, 1110, 1.02, "#57BCEB", "#FFD0A8", wave=index % 2 == 1)
    draw_tiko_details(draw, 730, 1110, 1.02)

    # Simple scene prop selected from keywords.
    p = scene.get("visualPrompt","").lower()
    if "momo" in p.lower() or "new friend" in p.lower():
        draw_momo(draw, 930, 1190, 0.58)

    if any(k in p for k in ("ball", "play")):
        draw.ellipse((465, 1270, 600, 1405), fill="#FF6B6B", outline="#7A3E3E", width=6)
    elif any(k in p for k in ("flower", "garden")):
        draw.line((540, 1240, 540, 1440), fill="#4D8C42", width=14)
        for dx, dy in [(-35,-20),(35,-20),(0,-55)]:
            draw.ellipse((540+dx-35,1240+dy-35,540+dx+35,1240+dy+35), fill="#FF9FB0")
    elif any(k in p for k in ("book", "learn")):
        draw.rounded_rectangle((470, 1280, 610, 1395), radius=10, fill="#7D8FEA", outline="#39456B", width=6)
        draw.line((540,1290,540,1385), fill="#FFFFFF", width=5)

    # Keep the picture clean: no generic scene labels across the artwork.
    caption = re.sub(r"[^A-Za-z0-9 '!?.,-]", "", scene.get("caption", "")).strip()
    if caption:
        draw.rounded_rectangle((65, 80, 1015, 175), radius=30, fill="#FFFFFF")
        draw.text((95, 105), caption[:42], fill="#344054")

    img.save(output, "PNG")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    make_scene({"visualPrompt": args.prompt, "order": args.order, "sceneId": f"scene_{args.order:02d}"}, args.order - 1, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
