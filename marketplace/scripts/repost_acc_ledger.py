from frappe.query_builder import DocType
import frappe

SalesInvoice = DocType("Sales Invoice")
GLEntry = DocType("GL Entry")

# Code to find Sales Invoice whose GL Entries are missing and status is not paid.
def get_si_without_gl():
	query = (
		frappe.qb.from_(SalesInvoice)
		.left_join(GLEntry)
		.on(
			(GLEntry.voucher_type == "Sales Invoice")
			& (GLEntry.voucher_no == SalesInvoice.name)
		)
		.select(
			SalesInvoice.name,
			SalesInvoice.customer,
			SalesInvoice.posting_date,
			SalesInvoice.grand_total,
			SalesInvoice.outstanding_amount,
			SalesInvoice.status,
		)
		.where(
			(SalesInvoice.docstatus == 1)     # submitted
			& (~SalesInvoice.status.isin(["Paid"]))
			& (GLEntry.name.isnull())         # ❌ no GL entries
		)
		.orderby(SalesInvoice.posting_date)
	)

	return query.run(as_dict=True)

def batch_generator(iterable, batch_size=500):
	batch = []
	for item in iterable:
		batch.append(item)
		if len(batch) == batch_size:
			yield batch
			batch = []
	if batch:
		yield batch
		
BATCH_SIZE = 500
COMPANY = "Alphard Golf"

def batch_repost():
	batch_no = 1
	sales_invoices = get_si_without_gl()
	for batch in batch_generator(sales_invoices, BATCH_SIZE):

		print(f"\n--- Processing Batch {batch_no} | size={len(batch)} ---")

		try:
			voucher_items = []

			for inv in batch:
				try:
					voucher_items.append({
						"voucher_type": "Sales Invoice",
						"voucher_no": inv["name"]
					})
				except Exception as e:
					frappe.log_error(
						title="Voucher Prepare Failed",
						message=f"{inv.get('name')}\n{frappe.get_traceback()}"
					)
					continue

			if not voucher_items:
				print("⚠ No valid vouchers in this batch. Skipping.")
				continue

			repost_doc = frappe.get_doc({
				"doctype": "Repost Accounting Ledger",
				"company": COMPANY,
				"vouchers": voucher_items
			})

			repost_doc.save()

			frappe.db.commit()  # ✅ commit batch safely

			print(f"✔ Batch {batch_no} created: {repost_doc.name}")

		except Exception:
			frappe.db.rollback()  # ❌ only this batch fails

			frappe.log_error(
				title=f"Batch {batch_no} Failed",
				message=frappe.get_traceback()
			)

			print(f"❌ Batch {batch_no} failed. Logged error and continuing.")

		batch_no += 1
  
def enqueue_reposting_acc_ledger():
    job_name = "enqueue_reposting_of_acc_ledger"
    try:
        frappe.enqueue(
			"marketplace.scripts.repost_acc_ledger.batch_repost",
			queue="long",
			timeout=1200,
			job_name=job_name
		)
    except Exception as e:
        print(f"Reposting of Accounting Ledger Failed....\n{str(e)}")
		
