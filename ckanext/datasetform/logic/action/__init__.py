from . import create


def datasetform_actions():
    actions = dict(send_contact_form=create.send_contact_form)
    return actions
