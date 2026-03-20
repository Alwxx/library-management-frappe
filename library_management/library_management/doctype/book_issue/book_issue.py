import frappe
from frappe.model.document import Document

class BookIssue(Document):

    def validate(self):
        # Fetch latest book value from DB
        available = frappe.db.get_value("Book", self.book, "available_copies")

        # Check availability
        if available is None:
            frappe.throw("Book not found")

        if available <= 0:
            frappe.throw("Book not available")

        # Prevent duplicate issue
        existing = frappe.db.exists("Book Issue", {
            "book": self.book,
            "member": self.member,
            "docstatus": 1
        })

        if existing:
            frappe.throw("This member already has this book")

    def on_submit(self):
        # Reduce stock
        book = frappe.get_doc("Book", self.book)
        book.available_copies -= 1
        book.save()