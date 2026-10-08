from datetime import datetime
from io import BytesIO
from pathlib import Path
from PIL import Image
import streamlit as st

# ReportLab imports for exact PDF layout generation
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
PATH_EMBLEM = BASE_DIR / "Emblem_of_Ethiopia.svg.png"

# ==========================================
# 3. SIDEBAR FORM INPUTS (EXACT TEMPLATE FIELDS)
# ==========================================
st.markdown("### Institute of Ethiopian Standards (IES)")
st.markdown("Enter the exact certificate parameters below to generate the official pre-licence PDF.")

with st.form("pre_license_form"):
    st.markdown("#### Certificate Data Fields")
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        client_name = st.text_input("Client Name", value="ALEM")
        product_type = st.text_input("Product Type", value="OIL")
        brand_name = st.text_input("Brand", value="IFNAN")
        address_location = st.text_input("Address", value="AA")
        standard_ref = st.text_input("Standard Reference Number", value="ES 1212")
        cab_name = st.text_input("CAB Name", value="ECAE")
        
    with col_s2:
        cab_number = st.text_input("CAB Number", value="9009")
        date_applied = st.text_input("Date Applied", value="06-10-2026")
        pre_licence_no = st.text_input("Pre-Licence Number", value="ESML-AOI-CA9009")
        issue_date = st.text_input("Issue Date", value="07-10-2026")
        valid_until = st.text_input("Valid Until", value="07-10-2026")
        remark = st.text_input("Remark", value="CHECKED AND VERIFIED")

    submitted = st.form_submit_button("Generate Exact PDF Certificate")

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
    
    # Custom styles matching the exact document layout
    title_style = ParagraphStyle(
        'CertTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1, # Center
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
        logo_img = RLImage(str(PATH_IES_LOGO), width=130, height=50)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
        story.append(Spacer(1, 8))

    # 2. Header Titles
    story.append(Paragraph("INSTITUTE OF ETHIOPIAN STANDARDS (IES)", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("NATIONAL STANDARD MARK", subtitle_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("PRE LABELING - LICENSE", subtitle_style))
    story.append(Spacer(1, 15))

    # 3. Metadata Table (Left: Exact Fields, Right: ESM Mark)
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
    
    if PATH_ESM_MARK.exists():
        esm_img = RLImage(str(PATH_ESM_MARK), width=105, height=105)
        esm_img.hAlign = 'CENTER'
        mark_table = Table([[esm_img], [Paragraph("<font size=7 color='#CC0000'><b>ብሔራዊ የስታንዳርድ ምልክት</b><br/>National Standards Mark</font>", ParagraphStyle('Center', alignment=1))]], colWidths=[130])
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

    # Background Watermark Callback
    def add_watermark(canvas_obj, doc_obj):
        canvas_obj.saveState()
        if PATH_EMBLEM.exists():
            canvas_obj.drawImage(str(PATH_EMBLEM), 130, 160, width=340, height=340, mask='auto', preserveAspectRatio=True)
        canvas_obj.restoreState()

    doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
    buffer.seek(0)
    return buffer

# ==========================================
# 5. EXECUTION & DOWNLOAD
# ==========================================
if submitted:
    st.success("Official Certificate PDF generated successfully matching exact template specs!")
    
    form_data = {
        "client_name": client_name,
        "product_type": product_type,
        "brand_name": brand_name,
        "address_location": address_location,
        "standard_ref": standard_ref,
        "cab_name": cab_name,
        "cab_number": cab_number,
        "date_applied": date_applied,
        "pre_licence_no": pre_licence_no,
        "issue_date": issue_date,
        "valid_until": valid_until,
        "remark": remark
    }
    
    pdf_buffer = generate_pdf(form_data)
    
    st.download_button(
        label="📥 Download Official Pre-Licence PDF",
        data=pdf_buffer,
        file_name=f"Pre_Licence_{client_name}.pdf",
        mime="application/pdf"
    )
else:
    st.info("👈 Verify the exact template parameters in the sidebar and click **Generate Exact PDF Certificate**.")
