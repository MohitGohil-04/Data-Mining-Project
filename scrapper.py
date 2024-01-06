from tkinter import filedialog
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))
from wordcloud import WordCloud
import shutil
import os

reviewList = []


def getSoup(url):
    r = requests.get(
        "http://localhost:8050/render.html", params={"url": url, "wait": 2}
    )
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


# print(soup.title.text)


def getReviews(soup):
    reviews = soup.find_all("div", {"data-hook": "review"})
    try:
        for item in reviews:
            review = {
                "title": item.find("a", {"data-hook": "review-title"}).text.strip(),
                "ratings": float(
                    item.find("i", {"data-hook": "review-star-rating"})
                    .text.replace("out of 5 stars", "")
                    .strip()
                ),
                "body": item.find("span", {"data-hook": "review-body"}).text.strip(),
            }
            reviewList.append(review)
    except:
        pass


for x in range(1, 200):
    soup = getSoup(
        f"https://www.amazon.in/boAt-Airdopes-190-Breathing-Signature/product-reviews/B0BBTYBLJV/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}"
    )
    getReviews(soup)
    print(len(reviewList))
    if not soup.find("li", {"class": "a-disabled a-last"}):
        pass
    else:
        break

filename = str(input("Enter the filename: "))
df = pd.DataFrame(reviewList)
df.to_csv(filename + ".csv", index=False)

df = pd.read_csv(filename + ".csv")
text_df = df.drop(["title", "ratings"], axis=1)


# print(text_df.columns)
def data_processing(text):
    text = str(text).lower()
    text = re.sub(r"https\S+|www\S+https\S+", "", text, re.MULTILINE)
    text = re.sub(r"\@w+|\#", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text_tokens = word_tokenize(text)
    filtered_text = [w for w in text_tokens if not w in stop_words]
    return " ".join(filtered_text)


text_df.text = text_df["body"].apply(data_processing)
# print(text_df.head(10))


def polarity(text):
    return TextBlob(str(text)).sentiment.polarity


text_df["polarity"] = text_df["body"].apply(polarity)


def sentiment(label):
    if label < 0:
        return "Negative"
    elif label == 0:
        return "Neutral"
    else:
        return "Positive"


text_df["sentiment"] = text_df["polarity"].apply(sentiment)
bar_chart = plt.figure(figsize=(5, 5))
sns.countplot(x="sentiment", data=text_df)
plt.show()
bar_chart.savefig(filename + ".png")

pie_chart = plt.figure(figsize=(5, 5))
palette_color = sns.color_palette("bright")
tags = text_df["sentiment"].value_counts()
tags.plot(
    kind="pie",
    autopct="%1.1f%%",
    shadow=True,
    colors=palette_color,
    startangle=90,
    label="",
)
plt.title("Distribution of sentiments")
plt.show()
pie_chart.savefig(filename + " pie chart.png")

# word cloud code
pos_comments = text_df[text_df.sentiment == "Positive"]
pos_comments = pos_comments.sort_values(["polarity"], ascending=False)
# print(pos_comments.head())
text = " ".join([word for word in pos_comments["body"]])
positive_wordcloud = plt.figure(figsize=(20, 15), facecolor="None")
wordcloud = WordCloud(max_words=500, width=500, height=500).generate(text)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most frequent words in positive comments")
plt.show()
positive_wordcloud.savefig(filename + " positive word cloud.png")

pos_comments = text_df[text_df.sentiment == "Negative"]
pos_comments = pos_comments.sort_values(["polarity"], ascending=False)
# print(pos_comments.head())
text = " ".join([word for word in pos_comments["body"]])
negative_wordcloud = plt.figure(figsize=(20, 15), facecolor="None")
wordcloud = WordCloud(max_words=500, width=500, height=500).generate(text)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most frequent words in negative comments are")
plt.show()
negative_wordcloud.savefig(filename + " negative word cloud.png")

os.mkdir(filename)

# source file location
source_csv_dir = f"D:\Amazon Scrapper\\{filename+'.csv'}"
source_barchart_dir = f"D:\Amazon Scrapper\\{filename+'.png'}"
source_piechart_dir = f"D:\Amazon Scrapper\\{filename+' pie chart.png'}"
source_positivecloud_dir = f"D:\Amazon Scrapper\\{filename+' positive word cloud.png'}"
source_negativecloud_dir = f"D:\Amazon Scrapper\\{filename+' negative word cloud.png'}"

# destination file location
destination_csv_dir = f"D:\Amazon Scrapper\\{filename}"
destination_barchart_dir = f"D:\Amazon Scrapper\\{filename}"
destination_piechart_dir = f"D:\Amazon Scrapper\\{filename}"
destination_positivecloud_dir = f"D:\Amazon Scrapper\\{filename}"
destination_negativecloud_dir = f"D:\Amazon Scrapper\\{filename}"

shutil.move(source_csv_dir, destination_csv_dir)
shutil.move(source_barchart_dir, destination_barchart_dir)
shutil.move(source_piechart_dir, destination_piechart_dir)
shutil.move(source_positivecloud_dir, destination_positivecloud_dir)
shutil.move(source_negativecloud_dir, destination_negativecloud_dir)


# mail

from tkinter import *
import smtplib
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

attachements = []

master = Tk()
master.geometry("500x400")
master.title("Email")

# functions


def sendEmail():
    msg = EmailMessage()

    fromaddr = temp_username.get()
    toaddr = temp_receiver.get()
    password = temp_password.get()
    to = temp_receiver.get()
    subject = temp_subject.get()
    body = temp_body.get()
    # instance of MIMEMultipart

    # storing the senders email address
    msg["From"] = fromaddr

    # storing the receivers email address
    msg["To"] = toaddr

    # storing the subject
    msg["Subject"] = "Subject of the Mail"

    # string to store the body of the mail
    body = "Body_of_the_mail"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, "plain"))

    # attachment = attachements[0]

    p = MIMEBase("application", "octet-stream")

    filename = attachements[0]
    filetype = filename.split(".")
    filetype = filetype[1]
    if filetype == "jpg" or filetype == "JPG" or filetype == "png" or filetype == "PNG":
        import imghdr

        with open(filename, "rb") as f:
            file_data = f.read()
            image_type = imghdr.what(filename)
            msg.add_attachment(
                file_data, maintype="image", subtype=image_type, filename=f.name
            )
    else:
        with open(filename, "rb") as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=f.name,
            )

    s = smtplib.SMTP("smtp.outlook.com", 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


def selectFile():
    filename = filedialog.askopenfilename(
        initialdir="d:/", title="Please select a file"
    )
    attachements.append(filename)
    notif.config(fg="green", text="Attached " + str(len(attachements)) + " files")


def reset():
    usernameEntry.delete(0, "end")
    passwordEntry.delete(0, "end")
    receiverEntry.delete(0, "end")
    subjectEntry.delete(0, "end")
    bodyEntry.delete(0, "end")


def destroy():
    master.destroy()


Label(
    master,
    text="Please use the form below to send an email",
    bg="black",
    fg="white",
    font=("Calibri", 11),
).grid(row=1, padx=5, pady=10)

Label(master, text="Email", fg="black", font=("Calibri", 11)).grid(
    row=2, sticky=W, padx=70, pady=8
)
Label(master, text="Password", fg="black", font=("Calibri", 11)).grid(
    row=3, sticky=W, padx=70, pady=8
)
Label(master, text="To", fg="black", font=("Calibri", 11)).grid(
    row=4, sticky=W, padx=70, pady=8
)
Label(master, text="Subject", fg="black", font=("Calibri", 11)).grid(
    row=5, sticky=W, padx=70, pady=8
)
Label(master, text="Body", fg="black", font=("Calibri", 11)).grid(
    row=6, sticky=W, padx=70, pady=8
)
notif = Label(master, text="", font=("Calibri", 11), fg="red")
notif.grid(row=10, sticky=S)


temp_username = StringVar()
temp_password = StringVar()
temp_receiver = StringVar()
temp_subject = StringVar()
temp_body = StringVar()


usernameEntry = Entry(master, textvariable=temp_username)
usernameEntry.grid(row=2, column=0, ipadx=35)
passwordEntry = Entry(master, show="*", textvariable=temp_password)
passwordEntry.grid(row=3, column=0, ipadx=35)
receiverEntry = Entry(master, textvariable=temp_receiver)
receiverEntry.grid(row=4, column=0, ipadx=35)
subjectEntry = Entry(master, textvariable=temp_subject)
subjectEntry.grid(row=5, column=0, ipadx=35)
bodyEntry = Entry(master, textvariable=temp_body)
bodyEntry.grid(row=6, column=0, ipadx=35, pady=10)


Button(
    master,
    text="Send",
    width=11,
    fg="black",
    font=("georgia", 8, "bold"),
    command=sendEmail,
).grid(row=7, sticky=W, pady=10, padx=70)
Button(
    master,
    text="Reset",
    width=11,
    fg="black",
    font=("georgia", 8, "bold"),
    command=reset,
).grid(row=7, sticky=W, padx=220, pady=10)
Button(
    master,
    text="Attachments",
    width=11,
    fg="black",
    font=("georgia", 8, "bold"),
    command=selectFile,
).grid(row=8, sticky=W, padx=70, pady=10)
Button(
    master,
    text="Exit",
    width=11,
    fg="black",
    font=("georgia", 8, "bold"),
    command=destroy,
).grid(row=8, sticky=W, padx=220, pady=10)

master.mainloop()
