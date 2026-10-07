import os
import io
from datetime import datetime
import streamlit as st

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# Page Configuration
st.set_page_config(
    page_title="IES Pre-License Generation Portal",
    page_icon="📄",
    layout="centered"
)

st.title("Institute of Ethiopian Standards (IES)")
st.subheader("National Standard Mark Pre-License Generator")
st.markdown("Fill out the official details below to generate and download the secure pre-license PDF.")

with st.form("pre_license_form"):
    st.markdown("### 1. Client & Product Information")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name", placeholder="e.g., Apex Manufacturing PLC")
        product_type = st.text_input("Product Type", placeholder="e.g., Edible Vegetable Oil")
        brand = st.text_input("Brand Name", placeholder="e.g., Golden Sunshine")
    with col2:
        address = st.text_input("Address / Location", placeholder="Addis Ababa, Ethiopia")
        standard_reference_number = st.text_input("Standard Reference Number", placeholder="e.g., ES 1234:2024")

    st.markdown("### 2. Conformity Assessment & Licensing Details")
    col3, col4 = st.columns(2)
    with col3:
        cab_name = st.text_input("CAB Name", placeholder="e.g., Ethiopian Conformity Assessment Enterprise")
        cab_number = st.text_input("CAB Number", placeholder="e.g., CAB-012")
        date_applied = st.date_input("Date Applied", value=datetime.today())
        pre_licence_number = st.text_input("Pre-Licence Number", placeholder="e.g., IES/PL/2026/089")
    with col4:
        issue_date = st.date_input("Issue Date", value=datetime.today())
        valid_until = st.date_input("Valid Until", value=datetime.today())
        remark = st.text_area("Remark", placeholder="Any specific technical notes...")

    st.markdown("### 3. Standard Marks Selection")
    col_mark1, col_mark2 = st.columns(2)
    with col_mark1:
        include_esm_mark = st.checkbox("Include ESM Standard Mark")
    with col_mark2:
        include_eff_mark = st.checkbox("Include EFF Fortified Food Mark")

    submitted = st.form_submit_button("📄 Generate Official Pre-License PDF")

if submitted:
    if not client_name or not pre_licence_number:
        st.error("Please fill in at least the **Client Name** and **Pre-Licence Number** fields.")
    else:
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
            story = []
            styles = getSampleStyleSheet()

            # Styles using built-in Times New Roman
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                fontName='Times-Bold',
                fontSize=16,
                leading=20,
                alignment=TA_CENTER
            )

            value_style = ParagraphStyle(
                'ValueStyle',
                parent=styles['Normal'],
                fontName='Times-Roman',
                fontSize=12,
                leading=16,
                alignment=TA_LEFT
            )

            disclaimer_style = ParagraphStyle(
                'DisclaimerStyle',
                parent=styles['Normal'],
                fontName='Times-Italic',
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                textColor=colors.red
            )

            signature_style = ParagraphStyle(
                'SignatureStyle',
                parent=styles['Normal'],
                fontName='Times-Bold',
                fontSize=12,
                leading=16,
                alignment=TA_LEFT
            )

            # 1. Header Logo & Titles
            logo_path = os.path.join("assets", "ies_logo.png")
            if os.path.exists(logo_path):
                ies_logo = Image(logo_path, width=150, height=75)
                logo_table = Table([[ies_logo]], colWidths=[504])
                logo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('PADDING', (0, 0), (-1, -1), 0),
                ]))
                story.append(logo_table)
                story.append(Spacer(1, 8))

            story.append(Paragraph("INSTITUTE OF ETHIOPIAN STANDARDS (IES)", header_style))
            story.append(Spacer(1, 6))

            # Dynamic Header Title with PRE LABELING - LICENSE split onto a new line based on selection
            if include_esm_mark and not include_eff_mark:
                story.append(Paragraph("NATIONAL STANDARD MARK", header_style))
                story.append(Spacer(1, 4))
                story.append(Paragraph("PRE LABELING - LICENSE", header_style))
            elif include_eff_mark and not include_esm_mark:
                story.append(Paragraph("NATIONAL FORTIFIED FOOD MARK", header_style))
                story.append(Spacer(1, 4))
                story.append(Paragraph("PRE LABELING - LICENSE", header_style))
            elif include_esm_mark and include_eff_mark:
                story.append(Paragraph("NATIONAL STANDARD & FORTIFIED FOOD MARK", header_style))
                story.append(Spacer(1, 4))
                story.append(Paragraph("PRE LABELING - LICENSE", header_style))
            else:
                story.append(Paragraph("NATIONAL STANDARD MARK", header_style))
                story.append(Spacer(1, 4))
                story.append(Paragraph("PRE LABELING - LICENSE", header_style))

            story.append(Spacer(1, 15))

            # 2. Main Data Fields & Selected Standard Mark Side-by-Side
            fields_flowables = []
            
            issue_date_str = issue_date.strftime('%d-%m-%Y') if issue_date else "N/A"
            valid_until_str = valid_until.strftime('%d-%m-%Y') if valid_until else "N/A"
            date_applied_str = date_applied.strftime('%d-%m-%Y') if date_applied else "N/A"

            fields_data = [
                ("Client Name:", client_name),
                ("Product Type:", product_type or "N/A"),
                ("Brand:", brand or "N/A"),
                ("Address:", address or "N/A"),
                ("Standard Reference Number:", standard_reference_number or "N/A"),
                ("CAB Name:", cab_name or "N/A"),
                ("CAB Number:", cab_number or "N/A"),
                ("Date Applied:", date_applied_str),
                ("Pre-Licence Number:", pre_licence_number),
                ("Issue Date:", issue_date_str),
                ("Valid Until:", valid_until_str),
                ("Remark:", remark or "N/A"),
            ]

            for label, val in fields_data:
                line_text = f"<b>{label}</b> {val}"
                fields_flowables.append(Paragraph(line_text, value_style))
                fields_flowables.append(Spacer(1, 3))

            mark_flowables = []
            mark_added = False

            if include_esm_mark:
                esm_path = os.path.join("assets", "esm_mark.png")
                if os.path.exists(esm_path):
                    esm_img = Image(esm_path, width=110, height=110)
                    esm_img.hAlign = 'CENTER'
                    mark_flowables.append(esm_img)
                    mark_flowables.append(Spacer(1, 10))
                    mark_added = True

            if include_eff_mark:
                eff_path = os.path.join("assets", "eff_mark.png")
                if os.path.exists(eff_path):
                    eff_img = Image(eff_path, width=110, height=110)
                    eff_img.hAlign = 'CENTER'
                    mark_flowables.append(eff_img)
                    mark_flowables.append(Spacer(1, 10))
                    mark_added = True

            if not mark_added:
                no_mark_style = ParagraphStyle(
                    'NoMarkStyle',
                    parent=styles['Normal'],
                    fontName='Times-Italic',
                    fontSize=10,
                    leading=14,
                    alignment=TA_CENTER,
                    textColor=colors.gray
                )
                mark_flowables.append(Paragraph("[No Standard Mark Selected]", no_mark_style))

            content_table = Table([[fields_flowables, mark_flowables]], colWidths=[310, 194])
            content_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('PADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (1, 0), (1, 0), 8),
                ('RIGHTPADDING', (1, 0), (1, 0), 8),
            ]))
            story.append(content_table)
            story.append(Spacer(1, 15))

            # 3. Disclaimer Section (Red Font Color)
            disclaimer_text = (
                "<b>Disclaimer:</b> The client code can be reassigned to other clients "
                "if the holder fails to present the product certificate within the validity period."
            )
            story.append(Paragraph(disclaimer_text, disclaimer_style))
            story.append(Spacer(1, 20))

            # 4. Final Signature and Stamp Block (Centered)
            sig_data = [
                [
                    Paragraph("<b>Authorized Signature:</b><br/><br/><br/>___________________________", signature_style),
                    Paragraph("<b>Official Stamp:</b><br/><br/><br/>___________________________", signature_style)
                ]
            ]
            sig_table = Table(sig_data, colWidths=[230, 230])
            sig_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 20),
                ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ]))
            story.append(sig_table)

            # Canvas callback for Watermark and Bottom Footer Note
            def draw_page_decorations(canvas_obj, document):
                canvas_obj.saveState()
                
                # 1. Washed-out background FDRE Emblem watermark
                watermark_path = os.path.join("assets", "Emblem_of_Ethiopia.svg.png")
                if os.path.exists(watermark_path):
                    canvas_obj.setFillAlpha(0.08)
                    canvas_obj.setStrokeAlpha(0.08)
                    img_size = 350
                    x_pos = (612 - img_size) / 2
                    y_pos = (792 - img_size) / 2
                    canvas_obj.drawImage(watermark_path, x_pos, y_pos, width=img_size, height=img_size, mask='auto')
                
                # 2. Official Stamp Notice as a fixed bottom footer (using Times-Bold)
                canvas_obj.setFont('Times-Bold', 9)
                canvas_obj.setFillColor(colors.black)
                canvas_obj.drawCentredString(612 / 2.0, 30, "Note: This pre-licence is not valid unless it bears the official stamp of the Institute.")
                
                canvas_obj.restoreState()

            doc.build(story, onFirstPage=draw_page_decorations, onLaterPages=draw_page_decorations)
            buffer.seek(0)

            st.success("Pre-License PDF generated successfully!")
            st.download_button(
                label="📥 Download Generated PDF",
                data=buffer,
                file_name=f"Pre_License_{pre_licence_number}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error generating PDF document: {str(e)}")