import nltk
import ssl
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
import pickle
import imaplib
import email
import text2emotion as te
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')

imap_server = "imap.gmail.com"
email_address = "marwansorour08212003@gmail.com"
password = "qnqq woyn tsat znoq"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)

punkt_path = '/Users/marwansorour/Desktop/AI-EmailMonitoringSystem/english.pickle'

# Load the Punkt tokenizer using the specified path
with open(punkt_path, 'rb') as file:
    punkt_tokenizer = PunktSentenceTokenizer(pickle.load(file))

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



stop_words = set(stopwords.words('english'))



#tokenize email content and convert to lower case so that it is case insensitive 
tokens = sent_tokenize(email_content.lower())

print(tokens)

#Check if there are non-alphanumeric characters 
filtered_tokens = [word for word in tokens if word.isalnum()]
print(filtered_tokens)


key_word_matching = ["urgent", "loss of opportunity", "action required", "do not want to miss", "immediately", "consequences"]
threat_score = sum(token in key_word_matching for token in filtered_tokens)


print('Threat Score: ', threat_score)

threshold = 1  # Adjust threshold as needed

threat_score = 0


   

# Classification
if threat_score >= threshold:
    print("This email contains threats or urgencies.")
else:
    print("This email does not contain threats or urgencies.")


# stopWords.close()
imap.close()