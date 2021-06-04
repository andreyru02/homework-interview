import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, login, password, smtp, imap):
        self.login = login
        self.password = password
        self.smtp = smtp
        self.imap = imap

    def send_email(self, to_email, subject, letter):
        # Create message
        message = MIMEMultipart()
        message['From'] = self.login
        message['To'] = ', '.join(to_email)
        message['Subject'] = subject
        message.attach(MIMEText(letter))

        send_message = smtplib.SMTP(self.smtp, 587)

        # Identify ourselves to smtp gmail client
        send_message.ehlo()

        # Secure our email with tls encryption
        send_message.starttls()

        # re-identify ourselves as an encrypted connection
        send_message.ehlo()

        # Send message
        send_message.login(self.login, self.password)
        send_message.sendmail(self.login, to_email, message.as_string())
        send_message.quit()

    def get_mail(self, header=None):
        get_email = imaplib.IMAP4_SSL(self.imap)
        get_email.login(self.login, self.password)
        get_email.list()
        get_email.select("INBOX")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = get_email.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = get_email.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        get_email.logout()
        return email_message


if __name__ == '__main__':
    mail = Email('login@gmail.com', 'password', 'imap.gmail.com', 'smtp.gmail.com')
    mail.send_email(mail.login, 'Subject', 'Letter')
    get_mail = mail.get_mail(header='Header')
    print(get_mail)
