# VERIQRA AI — Round 3 complete implementation

Brand Content Compliance Assistant for Team BrainWave.

## Included research requirements
- Modular logo, colour, PDF-font and report checks.
- Groq → OpenRouter → offline local fallback for contextual claim review.
- T01–T07 offline benchmark cache.
- SQLite brand profiles, reports, issues, visual reviews and review history.
- Context-aware prohibited/preferred terms, evidence gaps, disclaimer checks, human approval/rejection.
- JSON and corrected-text exports.

## Run locally (Windows)
1. Install Python 3.10 or newer.
2. Extract the ZIP.
3. Open Command Prompt in the extracted folder.
4. Run:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env
   python test_benchmark.py
   python -m unittest discover -s tests -v
   streamlit run app.py
   ```
5. Optional: add API keys to `.env`. Never upload `.env` to GitHub.

## Render
- Runtime: Python 3
- Build: `pip install -r requirements.txt`
- Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Add `GROQ_API_KEY` and/or `OPENROUTER_API_KEY` in Render → Environment.
- Deploy from the repository root.

## Visual identity reference assets
The supplied official VERIQRA AI logo is installed at `assets/brand_logos/primary_logo.png`.
Logo detection uses OpenCV ORB feature matching and a RANSAC homography, allowing the reference artwork to be found when resized and placed within a larger creative. Missing, unreadable or insufficient-feature references return a structured failure for manual review. A visual match does not certify correct logo variant, recolour, clear space or context; a human reviewer must confirm those points.

Brand colour and font rules are assembled from the currently selected SQLite brand profile. The default profile values in this starter project are #0A3D62 and #F5F6FA; Poppins and Inter; Delta E maximum 5; minimum logo width 80 px; clear space 40 px. Adjust the profile values to the approved brand guide. PDF embedded font metadata is inspected; exact font family cannot be inferred reliably from raster PNG/JPG files.

## Important implementation boundaries
- A disclaimer's presence does not prove that the advertisement is compliant.
- AI and deterministic rules are screening aids, not legal advice or legal approval.
- Unsupported means evidence was not supplied; it does not mean the claim is false.
- PDF embedded font metadata is checked. Exact font family cannot be inferred reliably from raster PNG/JPG files.
- SQLite is stored in `veriqra.db`. On Render free web services, the local filesystem is ephemeral and may be reset on redeploy/restart. Use an external managed database or a persistent disk for production retention.
- No automated test can guarantee every marketing scenario is compliant. Run the included tests and add jurisdiction-specific cases before a real campaign.

## Round 3 verification notes
- The AI audit checkbox controls whether the external/local AI claim audit is invoked; when disabled, deterministic brand-rule checks still run and the report records that AI was disabled.
- Visual palette and font rules are assembled from the currently selected saved brand profile.
- A reviewer explicitly selects the report that receives a visual review, avoiding accidental attachment to an unrelated latest report.
- Verification run during packaging: `python -m unittest discover -s tests -v` (5 tests passed) and `python test_benchmark.py` (7/7 cases passed).
- These checks validate the included offline tests only; they do not prove external API availability, logo matching with a real approved reference image, or production hosting persistence.
