def enviar_mail(mail):
    from django.core.mail import EmailMultiAlternatives, BadHeaderError
    from django.utils.html import strip_tags

    subject = mail['subject']
    message = mail['message']
    message_html = message
    message_text = strip_tags(message)
    from_email = mail['from_email']
    reply_to = mail['reply_to']
    to = mail['to'] #to = 'hello', 'from@example.com', 'to@example.com'

    if subject and message and from_email and to:
        try:
            msg = EmailMultiAlternatives(subject, message_text, from_email, [to], headers = {'Reply-To': reply_to,})
            msg.attach_alternative(message_html, "text/html")
            msg.send()
        except BadHeaderError:
            return False
        return True
    else:
        return False