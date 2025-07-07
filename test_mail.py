import smtplib
import os

# --- Fill in your details here ---
# ❗️ Use your new, regenerated authorization code
SENDER_EMAIL = "2747872854@qq.com"
SENDER_PASSWORD = "zgwhsmlsvectdede"
RECEIVER_EMAIL = "2747872854@qq.com" # Sending to yourself for a test
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
# -----------------------------------

print(f"🐍 Starting smtplib test...")
print(f"Connecting to {SMTP_SERVER} on port {SMTP_PORT}...")

try:
    # Connect to the server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=60)
    print("✅ Connection successful.")

    # Enable detailed debug output
    server.set_debuglevel(1)

    print("\nIssuing EHLO command...")
    server.ehlo()

    print("\nStarting TLS encryption...")
    server.starttls()
    print("✅ STARTTLS successful.")

    print("\nRe-issuing EHLO command after TLS...")
    server.ehlo()

    print(f"\nLogging in as {SENDER_EMAIL}...")
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("✅ Login successful.")

    # Create the email message
    subject = "SMTPLIB Test"
    body = "This is a test email sent directly from smtplib in Python."
    message = f"Subject: {subject}\n\n{body}"

    print(f"\nSending email to {RECEIVER_EMAIL}...")
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
    print("✅ Email sent successfully!")

except Exception as e:
    print(f"\n❌ An error occurred:")
    print(e)

finally:
    try:
        server.quit()
        print("\nConnection closed.")
    except NameError:
        pass