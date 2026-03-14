from reportlab.pdfgen import canvas
from datetime import datetime

def generate_report(results):

    report_path = "reports/forensic_report.pdf"

    c = canvas.Canvas(report_path)

    c.setFont("Helvetica-Bold",16)
    c.drawString(150,800,"Digital Media Authenticity Analysis Report")

    c.setFont("Helvetica",12)
    c.drawString(50,770,"Generated on: " + str(datetime.now()))

    y = 740

    for item in results:

        c.drawString(50,y,"File Name: " + item["filename"])
        y -= 20

        for k,v in item["result"].items():
            c.drawString(70,y,f"{k}: {v}")
            y -= 20

        y -= 20

    c.drawString(50,y,"Forensic Techniques Used:")
    y -= 20

    c.drawString(70,y,"• Error Level Analysis (ELA)")
    y -= 20

    c.drawString(70,y,"• Compression Artifact Detection")
    y -= 20

    c.drawString(70,y,"• Deepfake Probability Estimation")

    c.save()

    return report_path