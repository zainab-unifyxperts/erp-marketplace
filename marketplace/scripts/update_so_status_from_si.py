from frappe.query_builder import DocType
import frappe

SalesInvoice = DocType("Sales Invoice")
SalesInvoiceItem = DocType("Sales Invoice Item")
SalesOrder = DocType("Sales Order")
DeliveryNote = DocType("Delivery Note")


def stream_target_sales_invoices():

    query = (
        frappe.qb.from_(SalesInvoiceItem)
        .join(SalesInvoice).on(SalesInvoice.name == SalesInvoiceItem.parent)
        .join(SalesOrder).on(SalesOrder.name == SalesInvoiceItem.sales_order)
        .join(DeliveryNote).on(DeliveryNote.name == SalesInvoiceItem.delivery_note)
        .select(SalesInvoice.name)
        .where(
            (SalesInvoice.docstatus == 1)
            & (SalesOrder.status != "Completed")
            & (DeliveryNote.custom_fulfilled_on_shopify == 1)
        )
        .distinct()
    )

    sql, params = query.walk()

    for row in frappe.db.sql(sql, params, as_dict=True):
        yield row["name"]
        

def batch_generator(generator, size=500):

    batch = []

    for item in generator:
        batch.append(item)

        if len(batch) >= size:
            yield batch
            batch = []

    if batch:
        yield batch
        
def process_sales_invoice_batch(batch):

    failed = []
    updated = 0

    for si_name in batch:

        try:
            si = frappe.get_doc("Sales Invoice", si_name)

            si.update_prevdoc_status()
            si.set_status(update=True)
            si.db_set("status", si.status)

            updated += 1
            print("✅", si_name)

        except Exception as e:
            failed.append({
                "invoice": si_name,
                "error": str(e)
            })
            print("❌ Failed:", si_name, e)

    frappe.db.commit()

    return updated, failed

def run_mass_status_update():

    total_checked = 0
    total_updated = 0
    all_failed = []

    for batch in batch_generator(stream_target_sales_invoices(), 500):

        print(f"\n--- Processing batch size={len(batch)} ---")

        updated, failed = process_sales_invoice_batch(batch)

        total_checked += len(batch)
        total_updated += updated
        all_failed.extend(failed)

        print(
            f"Progress → checked={total_checked} "
            f"updated={total_updated} "
            f"failed={len(all_failed)}"
        )

    print("\n=== DONE ===")
    print("Checked:", total_checked)
    print("Updated:", total_updated)
    print("Failed:", len(all_failed))

    return all_failed

def enqueue_mass_update():
    job_name = "update_so_status_from_si"
    try:
        frappe.enqueue(
            "marketplace.scripts.update_so_status_from_si.run_mass_status_update",
            queue="long",
            timeout=1200,
            job_name=job_name
        )
    except Exception as e:
        print(f"Updating status failed...\n{str(e)}")
    