import re

def extract_email(text):
    """Extracts email addresses from the given text.

    Args:
        text (str): The input text containing email addresses.
    
    P.S. email pattern: local-part@domain
    e.g. 114514.newbee@example.com

    Returns:
        list: A list of extracted email addresses.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def extract_phone_numbers(text):
    """Extracts phone numbers from the given text.

    Args:
        text (str): The input text containing phone numbers.
    
    P.S. phone number pattern: normally 11 digits in China
    first digit is 1, second digit is 3-9
    e.g. 13800138000

    Returns:
        list: A list of extracted phone numbers.
    """
    phone_pattern = r'\b1[3-9]\d{9}\b'
    return re.findall(phone_pattern, text)

if __name__ == "__main__":
    input_text = input("Enter text to extract emails and phone numbers: ")

    emails = extract_email(input_text)
    phone_numbers = extract_phone_numbers(input_text)

    print("Extracted Emails:")
    for email in emails:
        print(f" - {email}")

    print("Extracted Phone Numbers:")
    for phone in phone_numbers:
        print(f" - {phone}")
