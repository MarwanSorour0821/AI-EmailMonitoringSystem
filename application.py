# from exchangelib import Account, Credentials

# user_email = 'marwansorour08212003@gmail.com'
# user_password = 'ykntzojkumfpfvtf'

# credential = Credentials(user_email,user_password)
# # account = Account(primary_smtp_address=user_email, credentials=credential, autodiscover=True)

# account = Account(
#     primary_smtp_address=user_email,
#     credentials=credential,
#     autodiscover=False,
#     config={
#         'server': 'https://outlook.office365.com/EWS/Exchange.asmx'  # Example URL, replace with your server URL
#     }
# )

# inbox = account.inbox
# messages = inbox.all().order_by('-datetime_received')

# for email in messages:
#     print("Subject:", email.subject)
#     print("Content:", email.body)
#     print("------------")

import imaplib
import email

imap_server = "imap.gmail.com"
email_address = "marwansorour08212003@gmail.com"
password = "qnqq woyn tsat znoq"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)


imap.select("Inbox")

_, msgnumbers = imap.search(None, "ALL")

for msgnumber in msgnumbers[0].split():
    _, data = imap.fetch(msgnumber, "RFC822")
    message = email.message_from_bytes(data[0][1])

    print(f'message number; {msgnumber}')
    print(f'From; {message.get('From')}')
    print(f'To; {message.get('To')}')
    print(f'BCC; {message.get('BCC')}')
    print(f'Data; {message.get('Date')}')

    print("Content: ")
    for part in message.walk():
        if part.get_content_type() == "text/plain":
            print(part.as_string())

imap.close()