from __future__ import annotations

from pathlib import Path
import cv2
import numpy as np


def _failure(message: str, *, automated: bool = False) -> dict:
    return {"passed": False, "automated": automated, "issues": [
        {"rule": "logo_check", "status": "fail", "message": message}
    ]}


def run_logo_check(image_path: str, rules: dict) -> dict:
    """Detect the approved logo in a creative using ORB feature matching.

    ORB + a RANSAC homography tolerates common resizing, placement and modest
    perspective changes. It does not prove the logo is an approved variant:
    human review remains necessary for recolours, clear space and context.
    """
    logo_rules = rules.get("logo", {})
    reference_value = logo_rules.get("reference_path", "assets/brand_logos/primary_logo.png")
    reference = Path(reference_value)
    if not reference.is_absolute():
        reference = Path(__file__).resolve().parents[1] / reference
    if not reference.is_file():
        return _failure(
            f"Approved reference logo is missing: {reference}. "
            "Install the official logo at assets/brand_logos/primary_logo.png."
        )
    try:
        creative = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        template = cv2.imread(str(reference), cv2.IMREAD_COLOR)
        if creative is None:
            return _failure("Uploaded creative is not a readable image.")
        if template is None:
            return _failure("Approved reference logo exists but is not a readable image.")

        ih, iw = creative.shape[:2]
        th, tw = template.shape[:2]
        if min(ih, iw, th, tw) < 16:
            return _failure("Creative or reference logo is too small for reliable matching.")

        detector = cv2.ORB_create(nfeatures=3000, scaleFactor=1.2, nlevels=8)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        creative_gray = cv2.cvtColor(creative, cv2.COLOR_BGR2GRAY)
        kp_ref, des_ref = detector.detectAndCompute(template_gray, None)
        kp_img, des_img = detector.detectAndCompute(creative_gray, None)
        if des_ref is None or des_img is None or len(kp_ref) < 8 or len(kp_img) < 8:
            return _failure("Not enough visual features for reliable logo matching.")

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        pairs = matcher.knnMatch(des_ref, des_img, k=2)
        good = [m for pair in pairs if len(pair) == 2
                for m, n in [pair] if m.distance < 0.75 * n.distance]
        if len(good) < 8:
            return _failure("Approved logo was not confidently detected in the creative.", automated=True)

        src = np.float32([kp_ref[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst = np.float32([kp_img[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        homography, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        inliers = int(mask.ravel().sum()) if mask is not None else 0
        if homography is None or inliers < 8:
            return _failure("Approved logo was not confidently detected in the creative.", automated=True)

        corners = np.float32([[0, 0], [tw, 0], [tw, th], [0, th]]).reshape(-1, 1, 2)
        projected = cv2.perspectiveTransform(corners, homography).reshape(-1, 2)
        x0, y0 = np.floor(projected.min(axis=0)).astype(int)
        x1, y1 = np.ceil(projected.max(axis=0)).astype(int)
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(iw, x1), min(ih, y1)
        detected_width = max(0, x1 - x0)
        bbox = [int(x0), int(y0), int(x1), int(y1)]
        match_ratio = inliers / max(1, len(good))
        min_width = int(logo_rules.get("min_width_px", 80))
        clear_space = int(logo_rules.get("clear_space_px", 40))
        issues = []
        if detected_width < min_width:
            issues.append({"rule": "logo_min_width", "status": "fail", "location": bbox,
                           "message": f"Detected logo width ({detected_width}px) is below {min_width}px."})
        if x0 < clear_space or y0 < clear_space or iw - x1 < clear_space or ih - y1 < clear_space:
            issues.append({"rule": "logo_clear_space", "status": "fail", "location": bbox,
                           "message": f"Logo may not have the required {clear_space}px clear space."})
        return {
            "passed": not issues, "automated": True, "match_score": round(match_ratio, 3),
            "inlier_matches": inliers, "good_matches": len(good), "bbox": bbox,
            "method": "ORB feature matching + RANSAC homography", "issues": issues,
            "note": "A match indicates visual similarity to the reference; human review is still required for approved variant, recolour, legibility and context."
        }
    except ImportError:
        return _failure("OpenCV is unavailable; use the human logo checklist.")
    except Exception as exc:
        return _failure(f"Logo inspection failed safely: {type(exc).__name__}: {exc}")
