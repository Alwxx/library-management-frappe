import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class BookReturn(Document):

    def on_submit(self):
        # increase book count
        book = frappe.get_doc("Book", self.book)
        book.available_copies += 1
        book.save()

        # get issued record
        issue_name = frappe.db.get_value(
            "Book Issue",
            {"book": self.book, "member": self.member, "docstatus": 1},
            "name"
        )

        if issue_name:
            issue = frappe.get_doc("Book Issue", issue_name)

            # convert both to date
            return_date = getdate(self.return_date)
            due_date = getdate(issue.return_date)

            # update status
            issue.status = "Returned"
            issue.save()

            # fine calculation
            if return_date > due_date:
                days = (return_date - due_date).days
                self.fine = days * 10