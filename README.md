## Marketplace

Stores information of various marketplace 

### Requirements 
* Ubuntu v22.04
* ERPNext v15
  
### Installation Guide
  1) Login in to the github account that has access to the current repository
  2) In Github go to Settings -> SSH and GPG keys -> new SSH Key -> add the ssh key of the machine you're installing this frappe app on.
  **Note**: You only need to map the ssh key to your GitHub account once 
* ```bench get-app git@github.com:raymond-fung/erp-marketplace.git``` - Downloads an app from a git repository 
* `bench install-app marketplace` - Installs Marketplace on current site
* If after installation you get `Module Not Found Error` on your site, do the following
    1. [Reset dependencies for all install apps](https://discuss.frappe.io/t/modulenotfounderror/86527/6)
    2. If step 1 doesn't work try `bench setup requiremnts --python` or `bench setup env`
* Peform a `bench migrate` after the above installation to reflect changes to custom doctypes(if present)
* **Optional**:You can also do `bench restart`   
## Configuration 
* Go to Marketplace Doctype -> Create a new Marketplace (for e.g. Shopify, Amazon) 
* Following are the custom Doctypes for this App.
  | Doctype Name | Fields |Description|
  |--------------|--------|-----------|
  | Marketplace | Name (data)| Name of the Marketplace|
  | Marketplace Order Id | Marketplace Order Id (Data) | The Order Id recieved from Marketplace(from shopify in our case) | 
  | Marketplace Order Id | Marketplace (link -> Marketplace) | Linked to the Marketplace that we have created |
## Release Note
* This app hosts marketplace order id and marketplace doctypes needed for order syncing between Shopify and ERPNext
* It also contains customization to Sales Order, Delivery Note, Customer, Item, Packed Item, Sales Order Item, Sales Taxes and Charges
* **Note** run `bench migrate` everytime you install a new app now your site  
  
#### License

mit
