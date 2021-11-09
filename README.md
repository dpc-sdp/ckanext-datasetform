# CKAN Dataset Contact Form

This CKAN extension adds a simple form to each dataset that sends an email to the author/maintainer of the current dataset.

#### Enable Email settings
```
email_to = datavic@salsadigital.com.au
#error_email_from = ckan-errors@example.com
smtp.server = <SMTP_SERVER>
smtp.starttls = True
smtp.user = <SMTP_USERNAME>
smtp.password = <SMTP_PASSWORD>
#smtp.mail_from =
```

#### Install the extension 
Refer to [Extending guide](http://docs.ckan.org/en/latest/extensions/tutorial.html#installing-the-extension).
```
. /app/ckan/default/bin/activate
cd /app/ckan/default/src/ckanext-datasetform
python setup.py develop
```

#### Enable the plugin
Add `datasetform` to the list of plugins
```
ckan.plugins = stats text_view image_view recline_view datasetform
```

#### Settings
```
## Dataset Contact form settings
# Recipient email for each package. Use the field name from dataset, eg. maintainer_email or author_email.
ckan.package.contact_recipient = maintainer_email
```
If `ckan.package.contact_recipient` is not set, the form will fall back to using the CKAN setting `email_to`.
