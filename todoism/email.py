from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from todoism.extensions import mail


def _send_mail_async(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(to, subject, template, **kwargs):
    message = Message(current_app.config['TODOISM_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=_send_mail_async, args=[app, message])
    thr.start()
    return thr


def send_confirm_mail(user, token, to=None):
    send_mail(subject='Email Confirm', to=to or user.email, template='emails/confirm', user=user, token=token)
