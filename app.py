from flask import Flask, request, jsonify
import re
import dns.resolver
import smtplib

app = Flask(__name__)

# Basic regex email validation
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Check if email domain has valid MX records
def check_mx_records(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except:
        return False

# Verify email by connecting to SMTP server
def verify_email_smtp(email):
    domain = email.split('@')[-1]
    try:
        server = smtplib.SMTP(f"mail.{domain}")
        server.quit()
        return True
    except:
        return False

@app.route('/validate-email', methods=['GET'])
def validate_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Step 1: Check email format
    is_valid = is_valid_email(email)
    if not is_valid:
        return jsonify({"email": email, "valid": False, "reason": "Invalid format"})

    # Step 2: Check MX records
    domain = email.split('@')[-1]
    has_mx = check_mx_records(domain)
    if not has_mx:
        return jsonify({"email": email, "valid": False, "reason": "No mail servers found"})

    # Step 3: Verify SMTP (optional, some servers may block it)
    is_deliverable = verify_email_smtp(email)

    return jsonify({
        "email": email,
        "valid": is_valid and has_mx and is_deliverable,
        "reason": "Valid email" if is_valid and has_mx and is_deliverable else "Email may not be deliverable"
    })

if __name__ == '__main__':
    app.run(debug=True)
