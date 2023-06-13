import re
import smtplib
import pdfplumber
from googletrans import Translator

criteria = {
    'Education': 3,
    'Experience': 5,
    'Skills': 2,
    'ACADEMIC': 3
}

def extract_emails(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails

def calculate_mark(text):
    total_mark = 0
    for criterion, weight in criteria.items():
        if criterion in text:
            criterion_score = 1 
            total_mark += criterion_score * weight
    return total_mark

def process_cv(file_path):
    with pdfplumber.open(file_path) as pdf:
        cv_data = ""
        for page in pdf.pages:
            cv_data += page.extract_text()

        translator = Translator()
        translate = translator.translate(cv_data, dest="english")
        print(translate.text)
        mark = calculate_mark(translate.text)
        emails = extract_emails(translate.text)
        return mark, emails

def process_cv_list(file_paths):
    cv_marks = []
    cv_emails = []
    for file_path in file_paths:
        cv_mark, emails = process_cv(file_path)
        cv_marks.append(cv_mark)
        cv_emails.append(emails)
    return cv_marks, cv_emails

def send_email(result, email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ayachi.oumaima19@gmail.com'
    sender_password = 'bqcsvkligvhgqvbe'

    if result == 'accept':
        subject = 'Congratulations! Your CV has been accepted.'
        body = 'Dear applicant,\n\nCongratulations! We are pleased to inform you that your CV has been accepted.'
    else:
        subject = 'Regret: Your CV has not been accepted.'
        body = 'Dear applicant,\n\nWe regret to inform you that your CV has not been accepted at this time.'

    message = f'Subject: {subject}\n\n{body}'
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message)
        print(f"Email sent to {email} successfully.")
    except Exception as e:
        print(f"Error sending email to {email}. Error message: {str(e)}")


# Example usage
file_paths = ['Cv-recruitment/cv2.pdf']
cv_marks, cv_emails = process_cv_list(file_paths)
for i, (cv_mark, emails) in enumerate(zip(cv_marks, cv_emails)):
    print(f"CV {i+1} Mark: {cv_mark}")
    print(f"CV {i+1} Emails: {emails}")
    
    if cv_mark == 10:
        send_email('accept', emails[0])
    else:
        send_email('reject', emails[0])
    