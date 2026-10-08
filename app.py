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

PATH_IES_LOGO = BASE_DIR / "ies_logo.png"
PATH_ESM_MARK = BASE_DIR / "esm_mark.png"
PATH_EFF_MARK = BASE_DIR / "eff_mark.png"
PATH_EMBLEM = BASE_DIR / "Emblem_of_Ethiopia.svg.png"
PATH_FONT = BASE_DIR / "GillSansMTCondensed.ttf"


def load_image(path: Path):
  if path.exists():
    return Image.open(path)
  return None


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
      '<div class="main-header">Institute of Ethiopian Standards (IES)</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="sub-header">National Standard Mark Pre-License Generator'
      " | Certification Scheme & Standard Mark Administration</div>",
      unsafe_allow_html=True,
  )

with col_logo2:
  if img_ies_logo:
    st.image(img_ies_logo, width=90)

st.markdown("---")

# ==========================================
# 4. COMPREHENSIVE INPUT FORM & PARAMETERS
# ==========================================
st.markdown("### Fill out the official details below to generate and download the secure pre-license document.")

with st.form("pre_license_form"):
  st.markdown("#### 1. Client & Product Information")
  col_f1, col_f2 = st.columns(2)
  
  with col_f1:
    client_name = st.text_input("Client Name", placeholder="e.g., Apex Manufacturing PLC")
    product_type = st.text_input("Product Type", placeholder="e.g., Edible Vegetable Oil")
    brand_name = st.text_input("Brand Name", placeholder="e.g., Golden Sunshine")
    
  with col_f2:
    address_location = st.text_input("Address / Location", placeholder="e.g., Addis Ababa, Ethiopia")
    standard_ref = st.text_input("Standard Reference Number", placeholder="e.g., ES 1234:2024")
    tin_number = st.text_input("TIN Number", placeholder="e.g., 0012345678")

  st.markdown("#### 2. Conformity Assessment & Licensing Details")
  col_f3, col_f4 = st.columns(2)
  
  with col_f3:
    cab_name = st.text_input("CAB Name", placeholder="e.g., Ethiopian Conformity Assessment Enterprise")
    validity_period = st.selectbox("Pre-License Validity Duration", ["3 Months", "6 Months", "1 Year"])
    
  with col_f4:
    issue_date = st.text_input("Issue Date", value=datetime.now().strftime('%Y-%m-%d'))
    license_scope = st.text_area("Scope of License / Certified Lines", placeholder="Specify authorized product lines and variants...")

  submitted = st.form_submit_button("Generate Pre-License Document")

# ==========================================
# 5. PREVIEW & GENERATION OUTPUT
# ==========================================
if submitted:
  if not client_name or not standard_ref:
    st.error("Please provide at least the mandatory Client Name and Standard Reference Number fields.")
  else:
    st.success(f"Pre-License data successfully processed for **{client_name}** under Scheme Ownership.")

    st.markdown(
        """
        <div class="card">
            <h3>Official Pre-License Authorization Summary</h3>
            <p>The form data below has been compiled for conformance verification under the National Standards Body guidelines.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
      st.markdown("### **Enterprise Profile**")
      st.write(f"**Client Name:** {client_name}")
      st.write(f"**TIN Number:** {tin_number if tin_number else 'N/A'}")
      st.write(f"**Address / Location:** {address_location if address_location else 'N/A'}")
      st.write(f"**CAB Name:** {cab_name if cab_name else 'N/A'}")

    with col2:
      st.markdown("### **Product & Standard Parameters**")
      st.write(f"**Product Type:** {product_type if product_type else 'N/A'}")
      st.write(f"**Brand Name:** {brand_name if brand_name else 'N/A'}")
      st.write(f"**Standard Reference:** {standard_ref}")
      st.write(f"**Validity Duration:** {validity_period}")

    if license_scope:
      st.markdown("**Scope of License:**")
      st.info(license_scope)

    st.markdown("---")

    # Display Conformance Marks
    st.markdown("### **Authorized Standard Marks & Insignia**")
    mark_col1, mark_col2, mark_col3 = st.columns(3)

    with mark_col1:
      if img_esm_mark:
        st.image(img_esm_mark, caption="Ethiopian Standard Mark (ESM)", width=150)
      else:
        st.info("ESM Mark asset pending.")

    with mark_col2:
      if img_eff_mark:
        st.image(img_eff_mark, caption="EFF Conformance Mark", width=150)
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

    document_summary = (
        f"INSTITUTE OF ETHIOPIAN STANDARDS (IES)\n"
        f"NATIONAL STANDARD MARK PRE-LICENSE CERTIFICATE\n"
        f"==================================================\n"
        f"Client Name: {client_name}\n"
        f"Address / Location: {address_location}\n"
        f"TIN Number: {tin_number}\n"
        f"Product Type: {product_type}\n"
        f"Brand Name: {brand_name}\n"
        f"Standard Reference: {standard_ref}\n"
        f"CAB Name: {cab_name}\n"
        f"Issue Date: {issue_date}\n"
        f"Validity Period: {validity_period}\n"
        f"License Scope: {license_scope}\n"
    )

    st.download_button(
        label="Download Official Pre-License Summary (.txt)",
        data=document_summary,
        file_name=f"Pre_License_{client_name.replace(' ', '_')}.txt",
        mime="text/plain",
    )

else:
  st.info("💡 Fill out the form above with your complete client and product specifications, then click **Generate Pre-License Document**.")

  with st.expander("System Diagnostic: Asset Verification Status"):
    st.write(f"- **IES Logo (`ies_logo.png`):** {'✅ Loaded' if img_ies_logo else '❌ Missing'}")
    st.write(f"- **ESM Mark (`esm_mark.png`):** {'✅ Loaded' if img_esm_mark else '❌ Missing'}")
    st.write(f"- **EFF Mark (`eff_mark.png`):** {'✅ Loaded' if img_eff_mark else '❌ Missing'}")
    st.write(f"- **National Emblem (`Emblem_of_Ethiopia.svg.png`):** {'✅ Loaded' if img_emblem else '❌ Missing'}")
    st.write(f"- **Custom Font (`GillSansMTCondensed.ttf`):** {'✅ Present' if PATH_FONT.exists() else '❌ Missing'}")
