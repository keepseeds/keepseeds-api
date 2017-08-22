"""
Module containing function definitions for mail utility.
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader, select_autoescape

def get_default_email_subject(tmpl_id):
    """
    Provided with a Template ID, look up a relevant subject.
    """
    template = 'Keepseeds | {}'

    if tmpl_id == 'reset_password':
        return template.format('Reset Password Request')

    if tmpl_id == 'verify_email':
        return template.format('Verify Email')

    return template.format('Automated Email')

def send_template_email(tmpl_id, tmpl_to, tmpl_subject=None,
                        tmpl_from='noreply@keepseeds.com',
                        **kwargs):
    """
    Send an email using an email template.
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = tmpl_subject or get_default_email_subject(tmpl_id)
    msg['From'] = tmpl_from
    msg['To'] = tmpl_to

    mail_merge = get_template(tmpl_id, **kwargs)

    plain_part = MIMEText(mail_merge['plain'], 'plain')
    html_part = MIMEText(mail_merge['html'], 'html')

    msg.attach(plain_part)
    msg.attach(html_part)

    string_message = msg.as_string()

    # Begin send message.
    server = get_smtp_server()
    server.sendmail(tmpl_from, tmpl_to, string_message)
    server.quit()

    return string_message

def get_smtp_server():
    """
    Get current SMTP server.
    """
    smtp_host = os.environ.get('SMTP_HOST', 'localhost')
    smtp_port = os.environ.get('SMTP_PORT', 25)
    smtp_login = os.environ.get('SMTP_USERNAME', None)
    smtp_password = os.environ.get('SMTP_PASSWORD', None)

    server = smtplib.SMTP(host=smtp_host, port=smtp_port)

    if smtp_host != 'localhost':
        server.login(smtp_login, smtp_password)

    return server

def get_template(tmpl_id, **kwargs):
    """
    Get an email template, html and plain parts.
    """
    env = Environment(loader=PackageLoader('mail'),
                      autoescape=select_autoescape(['html', 'xml', 'txt']))
    html_template = env.get_template('{}.html'.format(tmpl_id))
    plain_template = env.get_template('{}.txt'.format(tmpl_id))

    mail_merge = {
        'html': html_template.render(**kwargs),
        'plain': plain_template.render(**kwargs)
    }
    return mail_merge

if (__name__ == '__main__'):
    send_template_email('forgot_password',
                        'test@user.com',
                        'Keepseeds - Reset Password Request',
                        first_name='Andy',
                        last_name='Mepham')
