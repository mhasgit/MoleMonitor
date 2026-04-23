import unittest

import numpy as np

from compare.decision import Action, decide
from compare.measure import compare_metrics
from compare.scale import calibrate_px_per_mm
from compare.segment import segment_phase1_heuristic


class ComparePipelineTests(unittest.TestCase):
    def test_segmentation_prefers_mole_not_coin(self):
        img = np.full((300, 300, 3), 220, dtype=np.uint8)
        yy, xx = np.ogrid[:300, :300]
        # Coin-like bright circle in top-left
        coin = (xx - 70) ** 2 + (yy - 70) ** 2 <= 35 ** 2
        img[coin] = np.array([190, 190, 190], dtype=np.uint8)
        # Mole-like darker, more saturated region near center
        mole = (xx - 160) ** 2 + (yy - 170) ** 2 <= 22 ** 2
        img[mole] = np.array([110, 55, 45], dtype=np.uint8)

        mask, quality = segment_phase1_heuristic(img)
        self.assertGreater(int(np.sum(mask > 0)), 0)
        self.assertGreater(mask[170, 160], 0)
        self.assertEqual(mask[70, 70], 0)
        self.assertIn("candidate_count", quality)

    def test_coin_calibration_detects_circle(self):
        img = np.full((256, 256, 3), 110, dtype=np.uint8)
        yy, xx = np.ogrid[:256, :256]
        coin = (xx - 128) ** 2 + (yy - 128) ** 2 <= 48 ** 2
        img[coin] = np.array([235, 235, 235], dtype=np.uint8)
        px_per_mm, diag = calibrate_px_per_mm(img, coin_diameter_mm=18.0)
        self.assertIsNotNone(px_per_mm)
        self.assertTrue(diag.get("coin_detected"))
        self.assertGreater(px_per_mm or 0.0, 1.0)

    def test_compare_metrics_mm_conversion(self):
        m_a = {"area_px": 1000, "diam_px": 35.68, "irregularity": 10.0, "mean_L": 100, "mean_A": 140, "mean_B": 140}
        m_b = {"area_px": 1300, "diam_px": 40.67, "irregularity": 13.0, "mean_L": 112, "mean_A": 136, "mean_B": 145}
        out = compare_metrics(m_a, m_b, px_per_mm=4.0)
        self.assertTrue(out["scale_available"])
        self.assertIsNotNone(out["diam_change_mm"])
        self.assertIsNotNone(out["area_change_mm2"])
        self.assertGreater(out["color_deltaE"], 0)

    def test_low_confidence_keeps_triggered_changes(self):
        metrics = {
            "area_change_percent": 40.0,
            "diam_change_px": 5.0,
            "diam_change_mm": None,
            "irregularity_delta": 0.1,
            "color_deltaE": 9.0,
            "scale_available": False,
        }
        quality_bad = {"low_sharpness": True, "exposure_warning": False}
        seg_ok = {"too_small": False, "suspect_component": False}
        decision = decide(metrics, quality_bad, quality_bad, seg_ok, seg_ok)
        self.assertIn("area_change_percent", decision.triggered_rules)
        self.assertIn("color_deltaE", decision.triggered_rules)
        self.assertIn(decision.action, (Action.MONITOR, Action.RECOMMEND_REVIEW))


if __name__ == "__main__":
    unittest.main()
