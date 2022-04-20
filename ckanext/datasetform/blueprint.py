import ckan.lib.mailer as mailer
import logging
import re
import socket

from ckan import model
from ckan.common import c, _, config
from ckan.lib.base import abort
from ckan.lib.navl.dictization_functions import unflatten
from ckan.logic import clean_dict, parse_params, tuplize_dict
from ckan.plugins.toolkit import check_access, get_action, h, render, request
from flask import Blueprint

log = logging.getLogger(__name__)

datavic_datasetform = Blueprint('datavic_datasetform', __name__)


def send(dataset_id):
    # Auth check to make sure the user can see this package.

    context = {'model': model, 'user': c.user}

    data_dict = {'id': dataset_id, 'include_tracking': True}

    check_access('package_show', context, data_dict)

    try:
        pkg_dict = get_action('package_show')(context, {'id': dataset_id, 'include_tracking': True})
        pkg = context['package']
    except Exception as e:
        log.error(str(e))
        abort(403)

    # Get recipient email address.
    recipient_email_key = config.get('ckan.package.contact_recipient', 'maintainer_email')

    recipient_email = pkg_dict.get(recipient_email_key)

    if not recipient_email:
         recipient_email = config.get('email_to')

    if request.method == 'POST':
        data_dict = clean_dict(unflatten(tuplize_dict(parse_params(request.form))))
        data_dict['url'] = '/dataset/%s' % pkg.name
        success = False

        if not recipient_email:
            log.error("Recipient address for dataset %s is empty.", pkg.name)
        else:
            # Form validation.
            errors = {}

            if data_dict['name'] == '':
                errors['name'] = [u'Missing value for Your Name.']

            if data_dict['email'] == '':
                errors['email'] = [u'Missing value for Your Email.']
            elif re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                          data_dict['email']) is None:
                errors['email'] = [u'Incorrect email address.']

            if data_dict['subject'] == '':
                errors['subject'] = [u'Missing value for Subject']

            if data_dict['message'] == '':
                errors['message'] = [u'Missing value for your Message.']

            if 'terms' not in data_dict:
                errors['terms'] = [u'Please accept the privacy statement.']

            if (len(errors)) != 0:
                h.flash_error(u'Please correct all errors in the contact form.')
                return render('package/read.html', extra_vars={
                    u'data': data_dict,
                    u'errors': errors,
                    u'pkg_dict': pkg_dict,
                })

            # Attempt to send mail.
            body = 'Name: %s\nEmail: %s' % (data_dict['name'], data_dict['email'])
            body += '\n\nDataset: %s' % data_dict['url']
            body += '\nDataset ID: %s' % pkg.id
            body += '\n\n%s' % data_dict['message']

            mail_dict = {
                'recipient_email': recipient_email,
                'recipient_name': recipient_email,
                'subject': data_dict['subject'],
                'body': body
            }

            try:
                mailer.mail_recipient(**mail_dict)
            except (mailer.MailerException, socket.error):
                log.error(u'Cannot send contact email for dataset %s.', pkg.name, exc_info=1)
            else:
                success = True

            if success:
                h.flash_success(_(u'Your message has been sent.'))
            else:
                h.flash_error(_(u'Sorry, there was an error sending the email. Please try again later.'))


    return h.redirect_to('dataset.read', id=pkg.name)


datavic_datasetform.add_url_rule(u'/dataset/<dataset_id>/contact',
                                 methods=[u'POST'], view_func=send)