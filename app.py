from datetime import datetime
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="IES Pre-License Generator | National Standards Body",
    page_icon="🇪🇹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Executive Presentation
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.2rem;
            color: #1b4332;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #40916c;
            font-weight: 500;
            margin-bottom: 2rem;
        }
        .card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 5px solid #2d6a4f;
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background-color: #2d6a4f;
            color: white;
            font-weight: 600;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1b4332;
            color: white;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. ROBUST PATH RESOLUTION (PATHLIB)
# ==========================================
BASE_DIR = Path(__file__).parent

# Asset Paths
PATH_IES_LOGO = BASE_DIR / "ies_logo.png"
PATH_ESM_MARK = BASE_DIR / "esm_mark.png"
PATH_EFF_MARK = BASE_DIR / "eff_mark.png"
PATH_EMBLEM = BASE_DIR / "Emblem_of_Ethiopia.svg.png"
PATH_FONT = BASE_DIR / "GillSansMTCondensed.ttf"


def load_image(path: Path):
  """Safely load an image asset if it exists."""
  if path.exists():
    return Image.open(path)
  return None


# Load Assets
img_ies_logo = load_image(PATH_IES_LOGO)
img_esm_mark = load_image(PATH_ESM_MARK)
img_eff_mark = load_image(PATH_EFF_MARK)
img_emblem = load_image(PATH_EMBLEM)

# ==========================================
# 3. HEADER & INSTITUTIONAL BRANDING
# ==========================================
col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])

with col_logo1:
  if img_emblem:
    st.image(img_emblem, width=90)

with col_title:
  st.markdown(
      '<div class="main-header">Institute of Ethiopian Standards</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="sub-header">Certification Scheme & Standard Mark'
      " Administration | Pre-License Generation Portal</div>",
      unsafe_allow_html=True,
  )

with col_logo2:
  if img_ies_logo:
    st.image(img_ies_logo, width=90)

st.markdown("---")

# ==========================================
# 4. SIDEBAR - CLIENT & CERTIFICATION CONFIGURATION
# ==========================================
st.sidebar.header("📋 Client & Certificate Parameters")

with st.sidebar.form("pre_license_form"):
  client_name = st.text_input(
      "Client / Enterprise Name", placeholder="e.g., Apex Manufacturing PLC"
  )
  tin_number = st.text_input("TIN Number", placeholder="e.g., 0012345678")
  sector = st.selectbox(
      "Industrial Sector",
      [
          "Food and Agriculture",
          "Chemical and Construction",
          "Electrical and Electronic",
          "Textile and Leather",
          "Engineering and Metallurgy",
      ],
  )
  standard_ref = st.text_input(
      "Applicable Ethiopian Standard (ES)",
      placeholder="e.g., ES ISO 9001:2015 / ES 1234:2024",
  )
  validity_period = st.selectbox(
      "Pre-License Validity Duration", ["3 Months", "6 Months", "1 Year"]
  )
  issuing_region = st.selectbox(
      "Operational Region / Town",
      ["Addis Ababa", "Adama", "Hawassa", "Bahir Dar", "Dire Dawa", "Mekelle"],
  )

  submitted = st.form_submit_button("Generate Pre-License Document")

# ==========================================
# 5. MAIN CONTENT & CERTIFICATE PREVIEW
# ==========================================
if submitted:
  if not client_name or not standard_ref:
    st.error(
        "Please provide the mandatory Client Name and Standard Reference"
        " fields."
    )
  else:
    st.success(
        f"Pre-License authorization successfully generated for **{client_name}**"
        f" under Scheme Ownership."
    )

    # Certificate Card Container
    st.markdown(
        """
        <div class="card">
            <h3>Official Pre-License Authorization Preview</h3>
            <p>This document verifies that the designated client has fulfilled preliminary conformity assessment requirements and is authorized to utilize the Ethiopian Standard Mark under administrative supervision.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Display Metadata Breakdown
    col1, col2 = st.columns(2)

    with col1:
      st.markdown("### **Client Details**")
      st.write(f"**Enterprise:** {client_name}")
      st.write(f"**TIN:** {tin_number if tin_number else 'N/A'}")
      st.write(f"**Sector:** {sector}")
      st.write(f"**Location:** {issuing_region}, Ethiopia")

    with col2:
      st.markdown("### **Scheme Administration**")
      st.write(f"**Standard Reference:** {standard_ref}")
      st.write(f"**Validity:** {validity_period}")
      st.write(
          f"**Issuance Date:** {datetime.now().strftime('%Y-%m-%d')}"
      )
      st.write("**Status:** Active Pre-License Conformance")

    st.markdown("---")

    # Display Conformity Marks side-by-side
    st.markdown("### **Authorized Standard Marks & Insignia**")
    mark_col1, mark_col2, mark_col3 = st.columns(3)

    with mark_col1:
      if img_esm_mark:
        st.image(
            img_esm_mark,
            caption="Ethiopian Standard Mark (ESM)",
            width=150,
        )
      else:
        st.info("ESM Mark asset pending.")

    with mark_col2:
      if img_eff_mark:
        st.image(
            img_eff_mark, data="EFF Conformance", caption="EFF Mark", width=150
        )
      else:
        st.info("EFF Mark asset pending.")

    with mark_col3:
      if img_ies_logo:
        st.image(img_ies_logo, caption="NSB Scheme Ownership", width=150)
      else:
        st.info("IES Logo asset pending.")

    # Export Section
    st.markdown("---")
    st.subheader("📥 Export & Official Distribution")

    # Buffer generation mock for download
    document_summary = (
        f"INSTITUTE OF ETHIOPIAN STANDARDS\nPRE-LICENSE CERTIFICATE\n\nClient:"
        f" {client_name}\nTIN: {tin_number}\nSector: {sector}\nStandard:"
        f" {standard_ref}\nValidity: {validity_period}\nRegion:"
        f" {issuing_region}\nDate: {datetime.now().strftime('%Y-%m-%d')}"
    )

    st.download_button(
        label="Download Official Pre-License Certificate (.txt / PDF)",
        data=document_summary,
        file_name=f"Pre_License_{client_name.replace(' ', '_')}.txt",
        mime="text/plain",
    )

else:
  # Landing state before form submission
  st.info(
      "👈 Configure the client parameters in the sidebar and click **Generate"
      " Pre-License Document** to initiate the verification and generation"
      " workflow."
  )

  # Preview of available assets status
  with st.expander("System Diagnostic: Asset Verification Status"):
    st.write(
        f"- **IES Logo (`ies_logo.png`):**"
        f" {'✅ Loaded' if img_ies_logo else '❌ Missing'}"
    )
    st.write(
        f"- **ESM Mark (`esm_mark.png`):**"
        f" {'✅ Loaded' if img_esm_mark else '❌ Missing'}"
    )
    st.write(
        f"- **EFF Mark (`eff_mark.png`):**"
        f" {'✅ Loaded' if img_eff_mark else '❌ Missing'}"
    )
    st.write(
        f"- **National Emblem (`Emblem_of_Ethiopia.svg.png`):**"
        f" {'✅ Loaded' if img_emblem else '❌ Missing'}"
    )
    st.write(
        f"- **Custom Font (`GillSansMTCondensed.ttf`):**"
        f" {'✅ Present' if PATH_FONT.exists() else '❌ Missing'}"
    )