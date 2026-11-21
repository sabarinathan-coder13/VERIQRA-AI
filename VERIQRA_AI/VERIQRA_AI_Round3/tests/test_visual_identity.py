import os
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from checks.logo_check import run_logo_check
from checks.color_check import run_color_check
from checks.font_check import run_font_check


ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "assets" / "brand_logos" / "primary_logo.png"


class VisualIdentityTests(unittest.TestCase):
    def test_official_logo_detected_when_embedded_at_reduced_scale(self):
        self.assertTrue(LOGO.is_file())
        with tempfile.TemporaryDirectory() as tmp:
            reference = Image.open(LOGO).convert("RGB")
            creative = Image.new("RGB", (1200, 900), "#F5F6FA")
            creative.paste(reference.resize((768, 512)), (216, 194))
            path = Path(tmp) / "creative.png"
            creative.save(path)
            result = run_logo_check(str(path), {
                "logo": {"reference_path": str(LOGO), "min_width_px": 80,
                         "clear_space_px": 40}
            })
            self.assertTrue(result["automated"])
            self.assertTrue(result["passed"], result)
            self.assertGreaterEqual(result["inlier_matches"], 8)

    def test_missing_reference_is_reported_gracefully(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "creative.png"
            Image.new("RGB", (300, 200), "white").save(image)
            result = run_logo_check(str(image), {"logo": {"reference_path": str(Path(tmp) / "missing.png")}})
            self.assertFalse(result["passed"])
            self.assertFalse(result["automated"])
            self.assertIn("missing", result["issues"][0]["message"].lower())

    def test_profile_palette_is_used_for_color_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "brand.png"
            Image.new("RGB", (200, 200), "#0A3D62").save(image)
            result = run_color_check(str(image), {"colors": ["#0A3D62"], "delta_e_max": 5})
            self.assertTrue(result["passed"], result)

    def test_pdf_font_checker_uses_selected_profile(self):
        from reportlab.pdfgen import canvas
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "creative.pdf"
            c = canvas.Canvas(str(pdf))
            c.setFont("Helvetica", 12)
            c.drawString(40, 700, "Brand creative")
            c.save()
            approved = run_font_check(str(pdf), {"fonts": ["Helvetica"]})
            rejected = run_font_check(str(pdf), {"fonts": ["Poppins"]})
            self.assertTrue(approved["automated"])
            self.assertTrue(approved["passed"], approved)
            self.assertFalse(rejected["passed"], rejected)

    def test_unrelated_image_does_not_match_official_logo(self):
        import numpy as np
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "unrelated.png"
            rng = np.random.default_rng(7)
            Image.fromarray(rng.integers(0, 256, (900, 1200, 3), dtype=np.uint8)).save(image)
            result = run_logo_check(str(image), {
                "logo": {"reference_path": str(LOGO), "min_width_px": 80,
                         "clear_space_px": 40}
            })
            self.assertFalse(result["passed"], result)


if __name__ == "__main__":
    unittest.main()
