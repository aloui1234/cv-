import PyPDF2
import  re
import smtplib


# Define the criteria and scoring system
criteria = {
    'Education': 3,
    'Experience': 5,
    'Skills': 2,
    'PARCOURS ACADÉMIQUE': 3,
    'EXPÉRIENCE PROFESSIONNELLE': 5,
    'COMPÉTENCES': 2,
    'CONNAISSANCES': 1
}
def extract_emails(text):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return emails

# Function to calculate the overall mark
def calculate_mark(text):
    total_mark = 0
    for criterion, weight in criteria.items():
        # Perform the necessary calculations based on the criterion
        # You can extract data from the CV data and apply your logic here
        if criterion in str(text):
            criterion_score = 1  # Replace with actual calculation
            total_mark += criterion_score * weight
    return total_mark

# Function to process a single CV
def process_cv(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        # Extract relevant data from the PDF using PyPDF2 or other PDF library
        cv_data = extract_data_from_pdf(pdf_reader)
        mark = calculate_mark(cv_data)
        emails = extract_emails(cv_data)
        return mark , emails

def extract_data_from_pdf(pdf_reader):
    # Implement your code to extract data from the PDF here
    # You can access individual pages and extract text, perform pattern matching, etc.
    # Return the extracted data as needed
    # Example: Extracting text from the first page
    first_page = pdf_reader.pages[0]
    text = first_page.extract_text()
    return text

# Function to process a list of CVs and return the marks for all of them
def process_cv_list(file_paths):
    cv_marks = []
    cv_emails=[]
    for file_path in file_paths:
        cv_mark,emails = process_cv(file_path)
        cv_marks.append(cv_mark)
        cv_emails.append(emails)

    return cv_marks,cv_emails

# Function to send acceptance or rejection emails
def send_email(result, email):
    smtp_server = ''
    smtp_port = 587
    sender_email = ''
    sender_password = ''

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
file_paths = ['Cv-recruitment/hamza.pdf']
cv_marks,cv_emails = process_cv_list(file_paths)
for i, (cv_mark,emails) in enumerate(zip(cv_marks,cv_emails)):
    print(f"CV {i+1} Mark: {cv_mark}")
    print(f"CV {i+1} Emails: {emails}")
    if cv_mark > 10:
        send_email('accept', emails[0])
    else:
        send_email('reject', emails[0])
    