import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import imaplib
import email

nltk_data_path = "/Users/marwansorour/Desktop/AI-EmailMonitoringSystem"
nltk.data.path.append(nltk_data_path)

nltk.download('stopwords', download_dir=nltk_data_path)

imap_server = "imap.gmail.com"
email_address = "marwansorour08212003@gmail.com"
password = "qnqq woyn tsat znoq"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)


imap.select("Inbox")

_, msgnumbers = imap.search(None, "ALL")

Latest_Message_Number = msgnumbers[0].split()[-1]
_, data = imap.fetch(Latest_Message_Number, "(RFC822)")
message = email.message_from_bytes(data[0][1])

print(f'message number; {Latest_Message_Number}')
print(f'From; {message.get('From')}')
print(f'To; {message.get('To')}')
print(f'BCC; {message.get('BCC')}')
print(f'Data; {message.get('Date')}')

# Check for text/plain content type and print it
part = message.get_payload()[0]  # Assuming the text/plain part is the first one
if part.get_content_type() == "text/plain":
    email_content = part.get_payload(decode=True).decode()  # Decode and store the content

print("Content:")
print(email_content) 

nltk.download('punkt')
#nltk.download("stopwords")
stop_words = set(stopwords.words('english'))

#tokenize email content and convert to lower case so that it is case insensitive 
tokens = word_tokenize(email_content.lower())

#Check if there are non-alphanumeric characters 
filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

key_word_matching = ["urgent", "loss of opportunity", "action required", "do not want to miss", "immediately", "consequences"]
threat_score = sum(token in key_word_matching for token in filtered_tokens)

threshold = 2  # Adjust threshold as needed

# Classification
if threat_score >= threshold:
    print("This email contains threats or urgencies.")
else:
    print("This email does not contain threats or urgencies.")


imap.close()