import logging

from ckan.lib.base import h, BaseController, render, abort, request
from ckan import model
from ckan.common import c, _, config
import ckan.logic as logic
from ckan.logic import check_access, get_action, clean_dict, tuplize_dict, ValidationError, parse_params
from ckan.lib.navl.dictization_functions import unflatten
import socket
import ckan.lib.mailer as mailer
import re

log = logging.getLogger(__name__)
flatten_to_string_key = logic.flatten_to_string_key

class ContactController(BaseController):
    def send(self, dataset_id):
        """
        Send contact form submission.
        :param dataset_id:
        :return:
        """

        # Auth check to make sure the user can see this package.

        context = {'model': model, 'user': c.user}

        data_dict = {'id': dataset_id, 'include_tracking': True}

        check_access('package_show', context, data_dict)

        try:
            c.pkg_dict = get_action('package_show')(context, {'id': dataset_id, 'include_tracking': True})
            c.pkg = context['package']
        except:
            abort(403)

        # Get recipient email address.
        recipient_email_key = config.get('ckan.package.contact_recipient', 'maintainer_email')
        recipient_email = c.pkg_dict.get(recipient_email_key)
        if not recipient_email:
             recipient_email = config.get('email_to')

        if request.method == 'POST':
            data_dict = clean_dict(unflatten(tuplize_dict(parse_params(request.POST))))
            data_dict['url'] = '/dataset/%s' % c.pkg.name
            success = False

            if not recipient_email:
                log.error("Recipient address for dataset %s is empty.", c.pkg.name)
            else:
                # Form validation.
                errors = {}

                if data_dict['name'] == '':
                    errors['name'] = [u'Missing value for Your Name.']

                if data_dict['email'] == '':
                    errors['email'] = [u'Missing value for Your Email.']
                elif re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data_dict['email']) == None:
                    errors['email'] = [u'Incorrect email address.']

                if data_dict['subject'] == '':
                    errors['subject'] = [u'Missing value for Subject']

                if data_dict['message'] == '':
                    errors['message'] = [u'Missing value for your Message.']

                if (len(errors)) != 0:
                    h.flash_error(u'Please correct all errors in the contact form.')
                    vars = {'data': data_dict, 'errors': errors}
                    return render('package/read.html', extra_vars=vars)

                # Attempt to send mail.
                body = 'Name: %s\nEmail: %s' % (data_dict['name'], data_dict['email'])
                body += '\n\nDataset: %s' % (data_dict['url'])
                body += '\nDataset ID: %s' % (c.pkg.id)
                body += '\n\n%s' % data_dict['message']

                mail_dict = {
                    'recipient_email': recipient_email,
                    'recipient_name': recipient_email,
                    'subject': data_dict['subject'],
                    'body': body,
                    'headers': {'reply-to': data_dict['email']}
                }

                try:
                    mailer.mail_recipient(**mail_dict)
                except (mailer.MailerException, socket.error):
                    log.error(u'Cannot send contact email for dataset %s.', c.pkg.name, exc_info=1)
                else:
                    success = True

            if success:
                h.flash_success(_(u'Your message has been sent.'))
            else:
                h.flash_error(_(u'Sorry, there was an error sending the email. Please try again later.'))

        h.redirect_to(str('/dataset/%s' % (c.pkg.name)))
