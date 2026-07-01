## Marketplace

Stores information of various marketplace

### Requirements

- Ubuntu v22.04
- ERPNext v15

### Installation Guide

1. `bench get-app https://github.com/zainab-unifyxperts/erp-marketplace.git` - Downloads this app from the repository
2. `bench install-app marketplace` - Installs Marketplace on current site
3. If after installation you get `Module Not Found Error` on your site, do the following:
   - [Reset dependencies for all installed apps](https://discuss.frappe.io/t/modulenotfounderror/86527/6)
   - If step 1 doesn't work try `bench setup requirements --python` or `bench setup env`
4. Perform a `bench migrate` after the above installation to reflect changes to custom doctypes (if present)
5. **Optional**: You can also do `bench restart`

## Configuration

- Go to Marketplace Doctype -> Create a new Marketplace (for e.g. Shopify, Amazon)
- Following are the custom Doctypes for this App.

    | Doctype Name         | Fields                            | Description                                                       |
    | --------------------- | ----------------------------------- | --------------------------------------------------------------------- |
    | Marketplace           | Name (data)                        | Name of the Marketplace                                            |
    | Marketplace Order Id  | Marketplace Order Id (Data)        | The Order Id received from Marketplace (from shopify in our case) |
    | Marketplace Order Id  | Marketplace (link -> Marketplace)  | Linked to the Marketplace that we have created                     |

## Related Apps

- [erp-shopify-integration](https://github.com/zainab-unifyxperts/erp-shopify-integration) — depends on this app; install this app first if you're setting up Shopify sync.

## Release Note

- This app hosts marketplace order id and marketplace doctypes needed for order syncing between Shopify and ERPNext
- It also contains customization to Sales Order, Delivery Note, Customer, Item, Packed Item, Sales Order Item, Sales Taxes and Charges
- **Note**: run `bench migrate` every time you install a new app on your site

### License

mit