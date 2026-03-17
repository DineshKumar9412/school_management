import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")


def _send(to: str, subject: str, html: str):
    """Low-level send via SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"EduCore Platform <{SMTP_FROM}>"
    msg["To"]      = to
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_FROM, to, msg.as_string())


# ── Email to the enrolled SCHOOL ────────────────────────────────────────────
def send_school_confirmation(school_name: str, principal_name: str,
                              email: str, board: str, city: str):
    subject = f"🎓 Welcome to EduCore — {school_name} Enrollment Confirmed!"
    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background:#f7f8fc; margin:0; padding:0; }}
    .wrapper {{ max-width:600px; margin:40px auto; background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 4px 24px rgba(0,0,0,0.08); }}
    .header {{ background:linear-gradient(135deg,#0a9b8c,#3d4bce); padding:40px 36px; text-align:center; }}
    .header h1 {{ color:#fff; font-size:28px; margin:0 0 8px; letter-spacing:-0.5px; }}
    .header p  {{ color:rgba(255,255,255,0.85); font-size:15px; margin:0; }}
    .logo {{ font-size:36px; margin-bottom:12px; }}
    .body {{ padding:36px; }}
    .greeting {{ font-size:18px; font-weight:700; color:#111827; margin-bottom:8px; }}
    .msg {{ font-size:15px; color:#374151; line-height:1.7; margin-bottom:24px; }}
    .info-card {{ background:#f0fafa; border:1.5px solid #b2e8e3; border-radius:12px; padding:20px 24px; margin-bottom:24px; }}
    .info-row {{ display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #e5e7eb; font-size:14px; }}
    .info-row:last-child {{ border-bottom:none; }}
    .info-label {{ color:#6b7280; font-weight:600; }}
    .info-value {{ color:#111827; font-weight:700; text-align:right; }}
    .steps {{ margin-bottom:28px; }}
    .steps h3 {{ font-size:16px; font-weight:700; color:#111827; margin-bottom:14px; }}
    .step {{ display:flex; align-items:flex-start; gap:12px; margin-bottom:12px; }}
    .step-num {{ min-width:28px; height:28px; border-radius:50%; background:#0a9b8c; color:#fff; font-size:12px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:2px; }}
    .step-text {{ font-size:14px; color:#374151; line-height:1.5; }}
    .step-text strong {{ color:#111827; }}
    .cta {{ text-align:center; margin-bottom:28px; }}
    .cta-btn {{ display:inline-block; background:linear-gradient(135deg,#0a9b8c,#3d4bce); color:#fff; text-decoration:none; padding:14px 36px; border-radius:10px; font-size:15px; font-weight:700; letter-spacing:0.02em; }}
    .footer {{ background:#f7f8fc; padding:20px 36px; text-align:center; border-top:1px solid #e5e7eb; }}
    .footer p {{ font-size:13px; color:#9ca3af; margin:0; }}
    .footer strong {{ color:#0a9b8c; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <div class="logo">🎓</div>
      <h1>Enrollment Confirmed!</h1>
      <p>Welcome to the EduCore School Management Platform</p>
    </div>
    <div class="body">
      <p class="greeting">Dear {principal_name},</p>
      <p class="msg">
        Congratulations! <strong>{school_name}</strong> has been successfully enrolled on
        <strong>EduCore</strong>. Our team is thrilled to have you on board and will reach out
        within <strong>24 hours</strong> to begin your onboarding journey.
      </p>

      <div class="info-card">
        <div class="info-row"><span class="info-label">School Name</span><span class="info-value">{school_name}</span></div>
        <div class="info-row"><span class="info-label">Principal</span><span class="info-value">{principal_name}</span></div>
        <div class="info-row"><span class="info-label">Email</span><span class="info-value">{email}</span></div>
        <div class="info-row"><span class="info-label">Board</span><span class="info-value">{board}</span></div>
        <div class="info-row"><span class="info-label">City</span><span class="info-value">{city or 'Not provided'}</span></div>
      </div>

      <div class="steps">
        <h3>📋 What happens next?</h3>
        <div class="step"><div class="step-num">1</div><div class="step-text"><strong>Onboarding Call</strong> — Our team will call you within 24 hours to set up your account.</div></div>
        <div class="step"><div class="step-num">2</div><div class="step-text"><strong>Data Setup</strong> — We'll help you import students, staff, and class data.</div></div>
        <div class="step"><div class="step-num">3</div><div class="step-text"><strong>Training</strong> — Free training session for your admin staff included.</div></div>
        <div class="step"><div class="step-num">4</div><div class="step-text"><strong>Go Live!</strong> — Start using EduCore with full support from day one.</div></div>
      </div>

      <div class="cta">
        <a href="http://127.0.0.1:8000" class="cta-btn">Visit EduCore Platform →</a>
      </div>

      <p class="msg" style="font-size:14px; color:#6b7280;">
        If you have any questions, simply reply to this email. We're always happy to help! 😊
      </p>
    </div>
    <div class="footer">
      <p>© 2024 <strong>EduCore</strong> — School Management Platform. Built with ❤️ for educators across India.</p>
    </div>
  </div>
</body>
</html>
"""
    _send(email, subject, html)


# ── Email to ADMIN (you) ────────────────────────────────────────────────────
def send_admin_notification(school_name: str, principal_name: str,
                             email: str, phone: str, board: str,
                             city: str, state: str, total_students: int,
                             enrollment_id: int):
    subject = f"🏫 New Enrollment: {school_name} — EduCore"
    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <style>
    body {{ font-family:'Segoe UI',Arial,sans-serif; background:#f7f8fc; margin:0; padding:0; }}
    .wrapper {{ max-width:600px; margin:40px auto; background:#fff; border-radius:16px; overflow:hidden; box-shadow:0 4px 24px rgba(0,0,0,0.08); }}
    .header {{ background:linear-gradient(135deg,#f55d2c,#ffc224); padding:32px 36px; }}
    .header h1 {{ color:#fff; font-size:22px; margin:0 0 4px; }}
    .header p  {{ color:rgba(255,255,255,0.9); font-size:14px; margin:0; }}
    .body {{ padding:32px 36px; }}
    .badge {{ display:inline-block; background:#e8faf0; color:#14803a; border:1.5px solid #a7f3c3; border-radius:100px; padding:4px 14px; font-size:12px; font-weight:700; margin-bottom:20px; }}
    .info-card {{ background:#fffbf0; border:1.5px solid #ffd9b5; border-radius:12px; padding:20px 24px; margin-bottom:20px; }}
    .info-row {{ display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #f3e8d8; font-size:14px; }}
    .info-row:last-child {{ border-bottom:none; }}
    .info-label {{ color:#6b7280; font-weight:600; }}
    .info-value {{ color:#111827; font-weight:700; text-align:right; }}
    .footer {{ background:#f7f8fc; padding:16px 36px; text-align:center; border-top:1px solid #e5e7eb; font-size:13px; color:#9ca3af; }}
    .footer strong {{ color:#f55d2c; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h1>🏫 New School Enrollment!</h1>
      <p>A new school just enrolled on EduCore — action required within 24hrs.</p>
    </div>
    <div class="body">
      <div class="badge">✅ Enrollment #{enrollment_id} Received</div>
      <div class="info-card">
        <div class="info-row"><span class="info-label">School Name</span><span class="info-value">{school_name}</span></div>
        <div class="info-row"><span class="info-label">Principal</span><span class="info-value">{principal_name}</span></div>
        <div class="info-row"><span class="info-label">Email</span><span class="info-value">{email}</span></div>
        <div class="info-row"><span class="info-label">Phone</span><span class="info-value">{phone}</span></div>
        <div class="info-row"><span class="info-label">Board</span><span class="info-value">{board}</span></div>
        <div class="info-row"><span class="info-label">Location</span><span class="info-value">{city or ''}{', ' + state if state else ''}</span></div>
        <div class="info-row"><span class="info-label">Total Students</span><span class="info-value">{total_students}</span></div>
      </div>
      <p style="font-size:14px;color:#374151;">Please reach out to this school within 24 hours to begin onboarding.</p>
    </div>
    <div class="footer">© 2024 <strong>EduCore</strong> Admin Notifications</div>
  </div>
</body>
</html>
"""
    if ADMIN_EMAIL:
        _send(ADMIN_EMAIL, subject, html)
