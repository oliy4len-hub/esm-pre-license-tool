from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from PIL import Image
import streamlit as st

# ReportLab imports for precise PDF layout generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
        .stButton>button {
            background-color: #2d6a4f;
            color: white;
            font-weight: 600;
            border-radius: 4px;
            padding: 0.6rem 1.2rem;
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

# Initialize session state for persistent downloads
if "pdf_buffer" not in st.session_state:
    st.session_state.pdf_buffer = None
if "client_filename" not in st.session_state:
    st.session_state.client_filename = "Pre_Licence.pdf"

# ==========================================
# 3. STRUCTURED EXECUTIVE FORM INPUTS (WITH CALENDAR TOOLS)
# ==========================================
st.markdown('<div class="main-header">Institute of Ethiopian Standards (IES)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Certification Scheme & Standard Mark Administration | Pre-License Generation Portal</div>', unsafe_allow_html=True)

with st.form("pre_license_form"):
    
    # SECTION 1
    st.markdown("### 1. Client & Product Information")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        client_name = st.text_input("Client Name", value="ALEM", placeholder="e.g., Apex Manufacturing PLC")
        product_type = st.text_input("Product Type", value="OIL", placeholder="e.g., Edible Vegetable Oil")
        brand_name = st.text_input("Brand", value="IFNAN", placeholder="e.g., Golden Sunshine")
        
    with col_f2:
        address_location = st.text_input("Address / Location", value="AA", placeholder="e.g., Addis Ababa, Ethiopia")
        standard_ref = st.text_input("Standard Reference Number", value="ES 1212", placeholder="e.g., ES 1234:2024")

    st.markdown("---")

    # SECTION 2
    st.markdown("### 2. Conformity Assessment & Licensing Details")
    col_f3, col_f4 = st.columns(2)
    
    with col_f3:
        cab_name = st.text_input("CAB Name", value="ECAE", placeholder="e.g., Ethiopian Conformity Assessment Enterprise")
        cab_number = st.text_input("CAB Number", value="9009", placeholder="e.g., 9009")
        
        # Calendar tool for Date Applied
        date_applied_val = st.date_input("Date Applied", value=datetime.now().date())
        
        pre_licence_no = st.text_input("Pre-Licence Number", value="ESML-AOI-CA9009", placeholder="e.g., ESML-TD-CA9009")
        
    with col_f4:
        # Calendar tool for Issue Date
        issue_date_val = st.date_input("Issue Date", value=datetime.now().date())
        
        # Automatic 6-month validity calculation (Issue Date + 180 days)
        valid_until_val = issue_date_val + timedelta(days=180)
        st.date_input("Valid Until (Auto: Issue Date + 6 Months)", value=valid_until_val, disabled=True)
        
        mark_selection = st.selectbox(
            "Standard Mark Selection", 
            ["Ethiopian Standard Mark (ESM)", "EFF Conformance Mark"]
        )
        remark = st.text_input("Remark", value="CHECKED AND VERIFIED", placeholder="Any specific remarks...")

    st.markdown("---")
    submitted = st.form_submit_button("Generate Official Pre-Licence PDF Certificate")

# ==========================================
# 4. PDF GENERATION ENGINE
# ==========================================
def generate_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=30,
        bottomMargin=30
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CertTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#000000')
    )
    
    subtitle_style = ParagraphStyle(
        'CertSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#000000')
    )

    field_style = ParagraphStyle(
        'FieldStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#000000')
    )

    disclaimer_style = ParagraphStyle(
        'DisclaimerStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#FF0000')
    )

    note_style = ParagraphStyle(
        'NoteStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#000000')
    )

    # 1. Header Logo
    if PATH_IES_LOGO.exists():
        logo_img = RLImage(str(PATH_IES_LOGO), width=140, height=55)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
        story.append(Spacer(1, 10))

    # 2. Header Titles
    story.append(Paragraph("INSTITUTE OF ETHIOPIAN STANDARDS (IES)", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("NATIONAL STANDARD MARK PRE LABELING LICENSE", subtitle_style))
    story.append(Spacer(1, 15))

    # 3. Metadata Table (Left: Fields, Right: Selected Mark)
    fields_text = f"""
    <b>Client Name:</b> {data['client_name']}<br/>
    <b>Product Type:</b> {data['product_type']}<br/>
    <b>Brand:</b> {data['brand_name']}<br/>
    <b>Address:</b> {data['address_location']}<br/>
    <b>Standard Reference Number:</b> {data['standard_ref']}<br/>
    <b>CAB Name:</b> {data['cab_name']}<br/>
    <b>CAB Number:</b> {data['cab_number']}<br/>
    <b>Date Applied:</b> {data['date_applied']}<br/>
    <b>Pre-Licence Number:</b> {data['pre_licence_no']}<br/>
    <b>Issue Date:</b> {data['issue_date']}<br/>
    <b>Valid Until:</b> {data['valid_until']}<br/>
    <b>Remark:</b> {data['remark']}
    """
    
    p_fields = Paragraph(fields_text, field_style)
    
    target_mark_path = PATH_ESM_MARK if "ESM" in data['mark_selection'] else PATH_EFF_MARK
    mark_label_text = "ብሔራዊ የስታንዳርድ ምልክት<br/>National Standards Mark" if "ESM" in data['mark_selection'] else "የኢነርጂ ቅልጥፍና ምልክት<br/>Energy Efficiency Mark"

    if target_mark_path.exists():
        mark_img = RLImage(str(target_mark_path), width=110, height=110)
        mark_img.hAlign = 'CENTER'
        mark_table = Table([[mark_img], [Paragraph(f"<font size=7 color='#CC0000'><b>{mark_label_text}</b></font>", ParagraphStyle('Center', alignment=1))]], colWidths=[130])
        table_data = [[p_fields, mark_table]]
    else:
        table_data = [[p_fields, ""]]

    content_table = Table(table_data, colWidths=[350, 170])
    content_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
    ]))
    
    story.append(content_table)
    story.append(Spacer(1, 15))

    # 4. Disclaimer
    disclaimer_text = "Disclaimer: The client code can be reassigned to other clients if the holder fails to present the product certificate within the validity period."
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    story.append(Spacer(1, 20))

    # 5. Signatures and Stamps
    sig_data = [
        [
            Paragraph("<b>Authorized Signature:</b>", field_style),
            Paragraph("<b>Official Stamp:</b>", field_style)
        ],
        [
            Spacer(1, 25),
            Spacer(1, 25)
        ],
        [
            Paragraph("____________________________", field_style),
            Paragraph("____________________________", field_style)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[250, 250])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 15))

    # 6. Footer Note
    story.append(Paragraph("Note: This pre-licence is not valid unless it bears the official stamp of the Institute.", note_style))

    # 7. Background Watermark Callback
    def add_watermark(canvas_obj, doc_obj):
        canvas_obj.saveState()
        if PATH_EMBLEM.exists():
            canvas_obj.drawImage(str(PATH_EMBLEM), 130, 160, width=340, height=340, mask='auto', preserveAspectRatio=True)
        canvas_obj.restoreState()

    doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
    buffer.seek(0)
    return buffer

# ==========================================
# 5. EXECUTION & SESSION STATE PERSISTENCE
# ==========================================
if submitted:
    form_data = {
        "client_name": client_name,
        "product_type": product_type,
        "brand_name": brand_name,
        "address_location": address_location,
        "standard_ref": standard_ref,
        "cab_name": cab_name,
        "cab_number": cab_number,
        "date_applied": date_applied_val.strftime('%d-%m-%Y'),
        "pre_licence_no": pre_licence_no,
        "issue_date": issue_date_val.strftime('%d-%m-%Y'),
        "valid_until": valid_until_val.strftime('%d-%m-%Y'),
        "mark_selection": mark_selection,
        "remark": remark
    }
    
    # Store buffer in session state so it doesn't get cleared on rerun
    st.session_state.pdf_buffer = generate_pdf(form_data)
    st.session_state.client_filename = f"Pre_Licence_{client_name}.pdf"
    st.success("Official Certificate PDF generated successfully!")

# Always render the download button outside the form if the PDF exists in session state
if st.session_state.pdf_buffer is not None:
    st.markdown("---")
    st.markdown("### 📥 Download Certificate")
    st.download_button(
        label="📥 Download Official Pre-Licence PDF Certificate",
        data=st.session_state.pdf_buffer,
        file_name=st.session_state.client_filename,
        mime="application/pdf"
    )
else:
    st.info("💡 Fill out the structured sections above and click **Generate Official Pre-Licence PDF Certificate**.")
