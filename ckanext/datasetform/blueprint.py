import logging

from ckan import model
from ckan.common import c, _, config
from ckan.lib.base import abort
from ckan.lib.navl.dictization_functions import unflatten
from ckan.logic import clean_dict, parse_params, tuplize_dict, ValidationError
from ckan.plugins.toolkit import check_access, get_action, h, render, request
from flask import Blueprint

log = logging.getLogger(__name__)

datavic_datasetform = Blueprint("datavic_datasetform", __name__)


def send(dataset_id):
    # Auth check to make sure the user can see this package.

    context = {"model": model, "user": c.user}

    data_dict = {"id": dataset_id, "include_tracking": True}

    check_access("package_show", context, data_dict)

    try:
        pkg_dict = get_action("package_show")(
            context, {"id": dataset_id, "include_tracking": True}
        )
        pkg = context["package"]
    except Exception as e:
        log.error(str(e))
        abort(403)

    # Get recipient email address.
    recipient_email_key = config.get(
        "ckan.package.contact_recipient", "maintainer_email"
    )

    recipient_email = pkg_dict.get(recipient_email_key)

    if not recipient_email:
        recipient_email = config.get(
            "ckan.package.default_recipient_email"
        ) or config.get("email_to")

    if request.method == "POST":
        data_dict = clean_dict(unflatten(tuplize_dict(parse_params(request.form))))
        data_dict["pkg_url"] = "/dataset/%s" % pkg.name

        if not recipient_email:
            log.error("Recipient address for dataset %s is empty.", pkg.name)
        else:
            # Form validation.
            try:
                data_dict["id"] = pkg.id
                data_dict["pkg_name"] = pkg.name
                data_dict["recipient_email"] = recipient_email

                send_contact = get_action("send_contant_form")(context, data_dict)
            except ValidationError as e:
                errors = e.error_dict
                h.flash_error("Please correct all errors in the contact form.")
                return render(
                    "package/read.html",
                    extra_vars={
                        "data": data_dict,
                        "errors": errors,
                        "pkg_dict": pkg_dict,
                    },
                )

            if send_contact["success"]:
                h.flash_success(_("Your message has been sent."))
            else:
                h.flash_error(
                    _(
                        "Sorry, there was an error sending the email. Please try again later."
                    )
                )

    return h.redirect_to("dataset.read", id=pkg.name)


datavic_datasetform.add_url_rule(
    "/dataset/<dataset_id>/contact", methods=["POST"], view_func=send
)
