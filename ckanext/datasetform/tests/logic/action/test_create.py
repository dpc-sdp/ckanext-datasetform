import pytest

import ckan.tests.factories as factories
from ckan.logic import ValidationError

import ckanext.datasetform.logic.action.create as create


@pytest.mark.usefixtures("clean_db", "mail_server")
class TestContactSend:
    data_dict = {
        "name": "test",
        "email": "info@test.ckan.net",
        "recipient_email": "test@test2.com",
        "subject": "Test email",
        "message": "Test email message",
        "terms": True,
    }

    def pkg_add_keys(self, data_dict, dataset):
        data_dict["id"] = dataset["id"]
        data_dict["pkg_name"] = dataset["name"]
        data_dict["pkg_url"] = "/dataset/%s" % dataset["name"]
        return data_dict

    def test_check_email_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()
        data_dict["email"] = "testincorrectemail"

        data_dict = self.pkg_add_keys(data_dict, dataset)

        with pytest.raises(ValidationError, match="Incorrect email address."):
            create.send_contant_form(context, data_dict)

    def test_check_terms_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)
        data_dict.pop("terms")

        with pytest.raises(ValidationError, match=create.errors_text["terms"]):
            create.send_contant_form(context, data_dict)

    def test_check_subject_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)
        data_dict.pop("subject")

        with pytest.raises(ValidationError, match=create.errors_text["subject"]):
            create.send_contant_form(context, data_dict)

    def test_check_message_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)
        data_dict.pop("message")

        with pytest.raises(ValidationError, match=create.errors_text["message"]):
            create.send_contant_form(context, data_dict)

    def test_check_name_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)
        data_dict.pop("name")

        with pytest.raises(ValidationError, match=create.errors_text["name"]):
            create.send_contant_form(context, data_dict)

    def test_check_recipient_email_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)
        data_dict.pop("recipient_email")

        with pytest.raises(
            ValidationError, match=create.errors_text["recipient_email"]
        ):
            create.send_contant_form(context, data_dict)

    def test_check_id_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)
        data_dict.pop("id")

        with pytest.raises(
            ValidationError, match="Missing id, can not get Package object"
        ):
            create.send_contant_form(context, data_dict)

    def test_check_pkg_name_validation(self):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)
        data_dict.pop("pkg_name")

        with pytest.raises(ValidationError, match=create.errors_text["pkg_name"]):
            create.send_contant_form(context, data_dict)

    def test_check_email_send_validation(self, mail_server):
        dataset = factories.Dataset()
        user = factories.User()
        context = {"user": user["name"]}

        data_dict = self.data_dict.copy()

        data_dict = self.pkg_add_keys(data_dict, dataset)

        send = create.send_contant_form(context, data_dict)

        msgs = mail_server.get_smtp_messages()

        # Compare with sended recipient email
        assert self.data_dict["recipient_email"] == msgs[0][2][0]

        assert send["success"] == True
