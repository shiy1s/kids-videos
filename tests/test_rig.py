import json, shutil, tempfile, unittest
from pathlib import Path
from render.rig import load_config, render_demo, CONFIG

class RigTests(unittest.TestCase):
    def test_all_rigs_have_layers_pivots_and_parent_integrity(self):
        cfg=load_config()
        self.assertEqual(set(cfg["characters"]), {"Bibi","Tiko","Momo"})
        for name,rig in cfg["characters"].items():
            self.assertTrue(rig["placeholder"], name+" must disclose placeholder art")
            self.assertGreaterEqual(len(rig["layers"]), 6)
            self.assertTrue(all(len(layer["pivot"])==2 for layer in rig["layers"]))

    def test_missing_pivot_fails_loudly(self):
        cfg=json.loads(CONFIG.read_text())
        del cfg["characters"]["Bibi"]["layers"][0]["pivot"]
        with tempfile.NamedTemporaryFile("w",suffix=".json",delete=False) as f:
            json.dump(cfg,f); path=Path(f.name)
        try:
            with self.assertRaisesRegex(ValueError,"LAYER_OR_PIVOT_MISSING"):
                load_config(path)
        finally: path.unlink(missing_ok=True)

    @unittest.skipUnless(shutil.which("ffmpeg"),"ffmpeg not installed")
    def test_renders_five_second_demo_for_each_character(self):
        cfg=load_config()
        with tempfile.TemporaryDirectory() as d:
            for name,rig in cfg["characters"].items():
                out=render_demo(name,rig,d,seconds=5,fps=cfg["canvas"]["fps"])
                self.assertTrue(out.exists() and out.stat().st_size>1000)
if __name__=="__main__": unittest.main()
