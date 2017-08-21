
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader, select_autoescape

def send_template_email(tmpl_id, tmpl_to, tmpl_subject, tmpl_from='noreply@keepseeds.com', **kwargs):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = tmpl_subject
    msg['From'] = tmpl_from
    msg['To'] = tmpl_to

    mail_merge = get_template(tmpl_id, **kwargs)

    plain_part = MIMEText(mail_merge['plain'], 'plain')
    html_part = MIMEText(mail_merge['html'], 'html')

    msg.attach(plain_part)
    msg.attach(html_part)

    string_message = msg.as_string()

    # Begin send message.
    server = smtplib.SMTP('localhost')
    server.sendmail(tmpl_from, tmpl_to, string_message)
    server.quit()

    return string_message

def get_template(tmpl_id, **kwargs):
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
    send_template_email('forgot_password', 'test@user.com', 'Keepseeds - Reset Password Request', first_name='Andy', last_name='Mepham')
