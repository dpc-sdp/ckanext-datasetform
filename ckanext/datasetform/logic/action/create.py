import logging
import re
import socket

import ckan.lib.mailer as mailer
from ckan.plugins import toolkit
from ckan.plugins.toolkit import check_access, ValidationError

log = logging.getLogger(__name__)


errors_text = {
    "name": "Missing value for Name.",
    "email": "Missing value for Email.",
    "subject": "Missing value for Subject",
    "message": "Missing value for Message.",
    "terms": "Please accept the privacy statement.",
    "recipient_email": "Missing Recipient email",
    "id": "Missing Dataset ID",
    "pkg_name": "Missing Dataset Name",
}


def send_contant_form(context, data_dict):
    success = False
    check_access("package_show", context, data_dict)

    errors = {}

    for error_text_key in errors_text:
        if error_text_key not in data_dict or data_dict[error_text_key] == "":
            errors[error_text_key] = errors_text[error_text_key]
        elif error_text_key == "email":
            if (
                re.match(
                    "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                    data_dict["email"],
                )
                is None
            ):
                errors[error_text_key] = "Incorrect email address."

    if (len(errors)) != 0:
        raise ValidationError(errors)

    recipient_email = data_dict.pop("recipient_email")
    pkg_id = data_dict.pop("id")
    pkg_name = data_dict.pop("pkg_name")

    extra_vars = {
        "name": data_dict["name"],
        "email": data_dict["email"],
        "pkg_url": data_dict["pkg_url"],
        "pkg_id": pkg_id,
        "message": data_dict["message"],
    }

    mail_dict = {
        "recipient_email": recipient_email,
        "recipient_name": recipient_email,
        "subject": data_dict["subject"],
        "body": toolkit.render("emails/contact_form.txt", extra_vars),
        "body_html": toolkit.render("emails/contact_form.html", extra_vars),
    }

    try:
        mailer.mail_recipient(**mail_dict)
    except (mailer.MailerException, socket.error):
        log.error("Cannot send contact email for dataset %s.", pkg_name, exc_info=1)
    else:
        success = True
    return {"success": success}
