
import streamlit as st
import json
import re
from datetime import datetime

# VERIQRA AI
# Brand Content Compliance Assistant
# Developed by Team BrainWave


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="VERIQRA AI",
    page_icon="🛡️",
    layout="wide"
)




# ---------------- PREMIUM NAVY & EMERALD UI ----------------

st.markdown("""
<style>
/* Overall background */
.stApp {
    background: linear-gradient(135deg, #101d35 0%, #142640 50%, #102b38 100%);
    color: #f1f5f9;
}

/* Main layout */
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14243b, #102b35);
    border-right: 1px solid #31516a;
}

/* Headings */
h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 750 !important;
    letter-spacing: -0.4px;
}

/* Main title accent */
h1 {
    text-shadow: 0 0 22px rgba(52, 211, 153, 0.18);
}

/* General text */
p, label, .stMarkdown {
    color: #d5e2ee;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: #1d3450 !important;
    color: #ffffff !important;
    border: 1px solid #42617a !important;
    border-radius: 12px !important;
}

/* Input focus */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border: 1px solid #34d399 !important;
    box-shadow: 0 0 0 2px rgba(52, 211, 153, 0.15) !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    background: linear-gradient(110deg, #059669, #10b981, #34d399);
    color: #ffffff !important;
    border: 1px solid #4ade80;
    border-radius: 12px;
    font-weight: 700;
    padding: 0.65rem 1.1rem;
    box-shadow: 0 5px 18px rgba(16, 185, 129, 0.18);
    transition: all 0.2s ease;
}

/* Button hover */
.stButton button:hover,
.stDownloadButton button:hover {
    background: linear-gradient(110deg, #047857, #059669);
    border: 1px solid #86efac;
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(16, 185, 129, 0.3);
}

/* Cards and bordered containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(31, 55, 80, 0.8);
    border: 1px solid #3b6075;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid #42617a;
}

/* Dividers */
hr {
    border-color: #36546b !important;
}

/* File uploader */
div[data-testid="stFileUploader"] {
    background: rgba(29, 52, 80, 0.8);
    border: 1px dashed #4b8b80;
    border-radius: 14px;
    padding: 14px;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1d3853, #1b3d43);
    border: 1px solid #39776b;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.12);
}

/* Metric values */
div[data-testid="stMetricValue"] {
    color: #6ee7b7 !important;
    font-weight: 750;
}

/* Links */
a {
    color: #6ee7b7 !important;
}

/* Smooth transitions */
.stTextInput, .stTextArea, .stSelectbox {
    transition: all 0.2s ease;
}
</style>
""", unsafe_allow_html=True)




# ---------------- BRAND GUIDELINES ----------------

st.sidebar.title("Brand Guidelines")

brand_name = st.sidebar.text_input(
    "Organisation Name",
    "BrainWave"
)

prohibited_text = st.sidebar.text_area(
    "Prohibited Words (one per line)",
    "guaranteed\n100% free\nbest in the world"
)

preferred_text = st.sidebar.text_area(
    "Preferred Terminology (old=new)",
    "cheap=affordable\nbuy now=explore now\nguys=everyone"
)

disclaimer = st.sidebar.text_input(
    "Required Disclaimer",
    "Terms and conditions apply."
)

approved_facts_text = st.sidebar.text_area(
    "Approved Facts (one per line)",
    "Founded in 2024\nAvailable online"
)

brand_colours = st.sidebar.text_input(
    "Approved Brand Colours",
    "Blue, White"
)

brand_font = st.sidebar.text_input(
    "Approved Brand Font",
    "Arial"
)

# Convert guideline text into lists and dictionaries

prohibited_words = [
    word.strip()
    for word in re.split(r"[,\n]+", prohibited_text)
    if word.strip()
]

preferred_words = {}

for line in preferred_text.splitlines():
    if "=" in line:
        old_word, new_word = line.split("=", 1)
        preferred_words[old_word.strip()] = new_word.strip()

approved_facts = []

for fact in approved_facts_text.splitlines():
    if fact.strip():
        approved_facts.append(fact.strip())


# ---------------- CONTENT CHECKING FUNCTION ----------------

def check_content(content):

    issues = []
    corrected_content = content

    # 1. Check prohibited words

    for word in prohibited_words:

        pattern = re.compile(
            rf"\b{re.escape(word)}\b",
            re.IGNORECASE
        )

        matches = pattern.findall(content)

        if matches:

            issues.append({
                "category": "Prohibited Terminology",
                "detected": ", ".join(matches),
                "rule": "This expression is prohibited by the brand guidelines.",
                "correction": "Replace with approved wording or remove it.",
                "severity": "High"
            })

            corrected_content = pattern.sub(
                "[REVIEW REQUIRED]",
                corrected_content
            )

    
    # 2. Check preferred terminology

    for old_word in preferred_words:

        new_word = preferred_words[old_word]

        pattern = re.compile(rf"\b{re.escape(old_word)}\b", re.IGNORECASE)

        matches = pattern.findall(content)

        if matches:

            issues.append({
                "category": "Preferred Terminology",
                "detected": ", ".join(matches),
                "rule": "The brand requires preferred terminology.",
                "correction": "Replace " + old_word + " with " + new_word,
                "severity": "Medium"
            })

            corrected_content = pattern.sub(
                new_word,
                corrected_content
            )

    # 3. Check required disclaimer

    if disclaimer.strip():

        if disclaimer.lower() not in content.lower():

            issues.append({
                "category": "Missing Disclaimer",
                "detected": "Required disclaimer is missing.",
                "rule": "Every publication must contain the approved disclaimer.",
                "correction": "Add: " + disclaimer,
                "severity": "High"
            })

            corrected_content = (
                corrected_content.rstrip()
                + "\n\n"
                + disclaimer
            )

    # 4. Check claims against approved facts

    sentences = re.split(r"[.!?\n]+", content)

    claim_words = [
        "founded",
        "certified",
        "award",
        "guarantee",
        "available",
        "serves",
        "million",
        "percent",
        "discount",
        "years",
        "results"
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        has_number = any(
            character.isdigit() for character in sentence
        )

        has_claim_word = False

        for word in claim_words:
            if word.lower() in sentence.lower():
                has_claim_word = True

        if has_number or has_claim_word:

            fact_verified = False

            for fact in approved_facts:
                if fact.lower() in sentence.lower():
                    fact_verified = True

            if not fact_verified:

                issues.append({
                    "category": "Fact Verification",
                    "detected": sentence,
                    "rule": "Claims must match the organisation's approved facts.",
                    "correction": "Verify this claim or replace it with an approved fact.",
                    "severity": "High"
                })

    return issues, corrected_content


# ---------------- APPLICATION HEADER ----------------

st.title("🛡️ VERIQRA AI")

st.subheader("Brand Content Compliance Assistant")

st.write(
    "Check your content against approved brand guidelines "
    "before publishing."
)

st.caption(
    "Team BrainWave | Saveetha Engineering College"
)

st.divider()


# ---------------- STEP 1: CONTENT SUBMISSION ----------------

st.header("1. Submit Your Content")

content_type = st.selectbox(
    "Select Content Type",
    [
        "Social Media Post",
        "Advertisement",
        "Email",
        "Document"
    ]
)

content = st.text_area(
    "Enter your content here",
    height=180,
    placeholder="Paste your content before publishing..."
)

uploaded_file = st.file_uploader(
    "Or upload a text file",
    type=["txt", "md"]
)

if uploaded_file is not None:
    content = uploaded_file.read().decode(
        "utf-8",
        errors="replace"
    )

# Optional creative image for visual review

st.subheader("Upload Creative for Visual Review")

creative = st.file_uploader(
    "Upload your advertisement or social media image",
    type=["png", "jpg", "jpeg"]
)

if creative is not None:
    st.image(
        creative,
        caption="Uploaded Brand Creative",
        use_container_width=True
    )


# ---------------- STEP 2: CONTENT ANALYSIS ----------------

st.header("2. Check Brand Compliance")

if st.button(
    "Check Content",
    type="primary",
    use_container_width=True
):

    if not content.strip():

        st.warning("Please enter or upload content first.")

    else:

        issues, corrected_content = check_content(content)

        st.session_state["issues"] = issues
        st.session_state["corrected"] = corrected_content
        st.session_state["original"] = content
        st.session_state["content_type"] = content_type
        st.session_state["checked"] = True
        st.session_state["decision"] = None

        st.session_state["revised_content"] = corrected_content


# ---------------- STEP 3: SHOW ISSUES ----------------

if st.session_state.get("checked", False):

    issues = st.session_state["issues"]

    st.divider()

    st.header("3. Compliance Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Issues",
        len(issues)
    )

    high_issues = 0

    for issue in issues:
        if issue["severity"] == "High":
            high_issues += 1

    col2.metric(
        "High Severity Issues",
        high_issues
    )

    if len(issues) == 0:
        result_status = "No Issues Found"
    else:
        result_status = "Needs Review"

    col3.metric(
        "Compliance Status",
        result_status
    )
    medium_issues = sum(
        1 for issue in issues
        if issue["severity"] == "Medium"
    )

    compliance_score = max(
        0,
        100 - (high_issues * 15) - (medium_issues * 8)
    )

    st.subheader("📊 Brand Compliance Score")
    st.metric("Indicative Compliance Score", f"{compliance_score}%")
    st.progress(compliance_score / 100)

    if len(issues) == 0:

        st.success("No rule violations were detected.")

    else:

        for number, issue in enumerate(issues, start=1):

            with st.expander(
                "Issue " + str(number) + ": " + issue["category"]
            ):

                st.write("**Detected Content:**")
                st.write(issue["detected"])

                st.write("**Rule Broken:**")
                st.write(issue["rule"])

                st.write("**Suggested Correction:**")
                st.write(issue["correction"])

                st.write("**Severity:**", issue["severity"])


    # ---------------- STEP 4: CORRECTIONS ----------------

    st.divider()

    st.header("4. Review Suggested Corrections")

    revised_content = st.text_area(
        "Edit the corrected content before approval",
        height=180,
        key="revised_content"
    )


    # ---------------- STEP 5: VISUAL IDENTITY ----------------

    st.divider()

    st.header("5. Visual Identity Review")

    st.write(
        "A human reviewer must compare the uploaded creative "
        "with the organisation's approved visual guidelines."
    )

    st.write("**Approved Colours:**", brand_colours)

    st.write("**Approved Font:**", brand_font)

    logo_check = st.checkbox(
        "Logo is correct and properly placed."
    )

    colour_check = st.checkbox(
        "Brand colours match the approved colours."
    )

    font_check = st.checkbox(
        "Font matches the approved brand font."
    )

    layout_check = st.checkbox(
        "Creative layout follows brand guidelines."
    )

    visual_complete = (
        logo_check
        and colour_check
        and font_check
        and layout_check
    )


    # ---------------- STEP 6: HUMAN APPROVAL ----------------

    st.divider()

    st.header("6. Final Human Approval")

    reviewed = st.checkbox(
        "I have reviewed all detected issues and the final content."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Approve Content",
            use_container_width=True
        ):

            if not reviewed:

                st.warning(
                    "Please confirm that you reviewed the issues."
                )

            elif not visual_complete:

                st.warning(
                    "Complete all visual identity checks first."
                )

            else:

                st.session_state["decision"] = "Approved"

                st.session_state["final_content"] = revised_content

                st.success(
                    "Content approved by the human reviewer."
                )

    with col2:

        if st.button(
            "Reject Content",
            use_container_width=True
        ):

            st.session_state["decision"] = "Rejected"

            st.session_state["final_content"] = revised_content

            st.error(
                "Content rejected by the human reviewer."
            )


    # ---------------- STEP 7: DOWNLOAD REPORT ----------------

    if st.session_state.get("decision") is not None:

        decision = st.session_state["decision"]

        st.divider()

        st.header("7. Final Compliance Report")

        st.write("**Organisation:**", brand_name)

        st.write(
            "**Content Type:**",
            st.session_state["content_type"]
        )

        st.write("**Final Decision:**", decision)

        report = {
            "Project": "VERIQRA AI",
            "Organisation": brand_name,
            "Content Type": st.session_state["content_type"],
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Original Content": st.session_state["original"],
            "Corrected Content": st.session_state["final_content"],
            "Issues": issues,
            "Visual Review": {
                "Logo": logo_check,
                "Colours": colour_check,
                "Font": font_check,
                "Layout": layout_check
            },
            "Final Decision": decision
        }

        report_data = json.dumps(
            report,
            indent=4
        )

        st.download_button(
            "Download Compliance Report",
            data=report_data,
            file_name="VERIQRA_AI_Report.json",
            mime="application/json",
            use_container_width=True
        )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "VERIQRA AI | Team BrainWave | "
    "Brand Content Compliance Assistan"
)
