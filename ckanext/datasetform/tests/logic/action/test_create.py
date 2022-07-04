import pytest

import ckan.tests.factories as factories
from ckan.logic import ValidationError
from ckan.tests.helpers import call_action

import ckanext.datasetform.logic.action.create as create


@pytest.fixture
def data_dict():
    dataset = factories.Dataset()
    return {
        "name": "test",
        "email": "info@test.ckan.net",
        "recipient_email": "test@test2.com",
        "subject": "Test email",
        "message": "Test email message",
        "terms": True,
        "id": dataset["id"],
        "pkg_name": dataset["name"],
        "pkg_url": "/dataset/%s" % dataset["name"],
    }


@pytest.mark.ckan_config("ckan.plugins", "datasetform")
@pytest.mark.usefixtures("clean_db", "mail_server")
class TestContactSend:
    def test_check_email_validation(self, data_dict):
        data_dict["email"] = "testincorrectemail"

        with pytest.raises(ValidationError, match="Incorrect email address."):
            call_action("send_contant_form", **data_dict)


    @pytest.mark.parametrize("field", ["terms", "subject", "message", "name", "recipient_email", "id", "pkg_name"])
    def test_check_fields_validation(self, field, data_dict):
        data_dict.pop(field)

        with pytest.raises(ValidationError, match=create.errors_text[field]):
            call_action("send_contant_form", **data_dict)


    def test_check_email_send_validation(self, mail_server, data_dict):
        send = call_action("send_contant_form", **data_dict)
        msgs = mail_server.get_smtp_messages()

        # Compare with sended recipient email
        assert data_dict["recipient_email"] == msgs[0][2][0]

        assert send["success"] == True
