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


data = pd.read_csv('Phishing_Email.csv')

x = data['Email Text']
y = data['Email Type']

vectorizer  = TfidfVectorizer(max_features=5000)

x2 = x.fillna('')

X_Tfidf = vectorizer.fit_transform(x2)
X_train, X_test, y_train, y_test = train_test_split(X_Tfidf, y, test_size=0.2, random_state=42)

#Train logistical regression classifier
model = LogisticRegression()
model.fit(X_train, y_train)

#Evaluate trained model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))


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
print(f'Subject: {message.get('Subject')}')
print(f'BCC; {message.get('BCC')}')
print(f'Data; {message.get('Date')}')

# Check for text/plain content type and print it
part = message.get_payload()[0]  # Assuming the text/plain part is the first one
if part.get_content_type() == "text/plain":
    email_content = part.get_payload(decode=True).decode()  # Decode and store the content

links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)


print("Content:")
print(email_content) 

new_email = [email_content]
new_email_tfidf = vectorizer.transform(new_email)
prediction = model.predict(new_email_tfidf)
print("Prediction:", prediction)

imap.close()