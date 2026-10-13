"""Config-driven rig demo renderer. Placeholder geometry is labelled and never treated as approved art."""
from __future__ import annotations
import argparse, json, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/"render/config/rig.json"

def load_config(path=CONFIG):
    cfg=json.loads(Path(path).read_text(encoding="utf-8"))
    if not cfg.get("characters"): raise ValueError("RIG_CONFIG_HAS_NO_CHARACTERS")
    for name,rig in cfg["characters"].items():
        if not rig.get("layers"): raise ValueError(f"{name}:RIG_LAYERS_MISSING")
        for layer in rig["layers"]:
            if not layer.get("name") or not layer.get("pivot") or len(layer["pivot"])!=2:
                raise ValueError(f"{name}:LAYER_OR_PIVOT_MISSING:{layer}")
            if layer.get("file") not in ("PLACEHOLDER_GENERATED",) and not (ROOT/layer["file"]).is_file():
                raise FileNotFoundError(f"{name}:LAYER_FILE_MISSING:{layer.get('file')}")
        names={x["name"] for x in rig["layers"]}
        for layer in rig["layers"]:
            if layer.get("parent") and layer["parent"] not in names:
                raise ValueError(f"{name}:PARENT_MISSING:{layer['parent']}")
    return cfg

def draw_frame(name, rig, frame, fps, out):
    w,h=rig["canvas"]["width"],rig["canvas"]["height"]
    im=Image.new("RGBA",(w,h),(255,247,224,255)); d=ImageDraw.Draw(im)
    # Three explicit parallax bands, intentionally simple placeholder scenery.
    d.ellipse((350-frame*2,100,510-frame*2,260),fill=(255,221,117,255))
    d.rectangle((0,620,w,h),fill=(169,220,154,255))
    d.ellipse((-70+frame*1.5,530,180+frame*1.5,760),fill=(120,190,105,255))
    t=frame/fps; bob=8*math.sin(t*2.8); x=270+18*math.sin(t*0.9)
    gesture=(frame//max(1,fps))%4
    body={"Bibi":(83,199,166,255),"Tiko":(255,177,143,255),"Momo":(255,177,143,255)}[name]
    accent={"Bibi":(255,211,77,255),"Tiko":(255,154,69,255),"Momo":(188,167,255,255)}[name]
    # Body/head are distinct draw groups; limbs pivot at body anchors.
    d.ellipse((x-75,570+bob,x+75,730+bob),fill=body,outline=(52,64,83,255),width=5)
    # legs walk by swapping offsets
    stride=16*math.sin(t*6) if gesture==3 else 0
    d.rounded_rectangle((x-48,700+bob+stride,x-10,795+bob+stride),radius=15,fill=(91,101,115,255))
    d.rounded_rectangle((x+10,700+bob-stride,x+48,795+bob-stride),radius=15,fill=(91,101,115,255))
    # Arms rotate around body pivots for named gestures.
    if gesture==0: # wave
        d.line((x-58,620+bob,x-112,570+bob),fill=body,width=24)
        d.line((x+58,620+bob,x+115,535+bob+20*math.sin(t*5)),fill=body,width=24)
    elif gesture==1: # point
        d.line((x-58,620+bob,x-112,650+bob),fill=body,width=24)
        d.line((x+58,620+bob,x+132,610+bob),fill=body,width=24)
    elif gesture==2: # clap, hands approach center
        d.line((x-58,620+bob,x-18,645+bob),fill=body,width=24)
        d.line((x+58,620+bob,x+18,645+bob),fill=body,width=24)
    else:
        d.line((x-58,620+bob,x-105,650+bob),fill=body,width=24)
        d.line((x+58,620+bob,x+105,650+bob),fill=body,width=24)
    head_y=490+bob
    if name=="Bibi":
        d.ellipse((x-70,head_y-125,x-20,head_y-10),fill=accent,outline=(52,64,83,255),width=4)
        d.ellipse((x+20,head_y-125,x+70,head_y-10),fill=accent,outline=(52,64,83,255),width=4)
    else:
        d.ellipse((x-88,head_y-90,x+88,head_y+65),fill=accent,outline=(52,64,83,255),width=4)
    d.ellipse((x-95,head_y-100,x+95,head_y+65),fill=accent,outline=(52,64,83,255),width=5)
    blink=(frame%(fps*4))<2
    for ex in (x-32,x+32):
        if blink: d.line((ex-9,head_y-15,ex+9,head_y-15),fill=(38,50,56,255),width=4)
        else: d.ellipse((ex-8,head_y-26,ex+8,head_y-5),fill=(38,50,56,255))
    d.arc((x-27,head_y+5,x+27,head_y+40),10,170,fill=(38,50,56,255),width=4)
    label=f"PLACEHOLDER RIG • {name} • gesture {['wave','point','clap','walk'][gesture]}"
    d.rounded_rectangle((25,35,w-25,90),radius=16,fill=(255,255,255,235))
    d.text((40,53),label,fill=(65,65,65,255))
    Path(out).parent.mkdir(parents=True,exist_ok=True); im.convert("RGB").save(out)

def render_demo(name, rig, outdir, seconds=5, fps=12):
    if not shutil.which("ffmpeg"): raise RuntimeError("FFMPEG_NOT_INSTALLED")
    outdir=Path(outdir); frames=outdir/f"rig_frames_{name}"; frames.mkdir(parents=True,exist_ok=True)
    for i in range(seconds*fps): draw_frame(name,rig,i,fps,frames/f"frame_{i:04d}.png")
    output=outdir/f"rig_demo_{name}.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(output)],check=True)
    return output

def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",type=Path,default=CONFIG); p.add_argument("--output-dir",type=Path,default=ROOT/"artifacts"); p.add_argument("--demo",action="store_true")
    a=p.parse_args(); cfg=load_config(a.config)
    if a.demo:
        for name,rig in cfg["characters"].items(): print(render_demo(name,rig,a.output_dir,cfg["canvas"]["demoSeconds"],cfg["canvas"]["fps"]))
    else: print("RIG_CONFIG_VALID",", ".join(cfg["characters"]))
if __name__=="__main__": main()
