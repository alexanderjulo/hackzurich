import requests

base_url = 'http://api.autoidlabs.ch/'


def crawl():
    print "getting customer ids."
    customer_ids = requests.get(base_url + 'customerids').json()
    print "got customer ids."
    products = {}
    transactions = []
    migros_product_counter = 0
    for customer_id in customer_ids:
        print "checking customer_id %s" % customer_id
        customer_transactions = requests.get(
            base_url + 'pos/%s' % customer_id
        ).json()
        transactions.append(customer_transactions)
        for transaction in customer_transactions:
            ean = transaction['migrosEan']
            product = requests.get(base_url + 'products/%s' % ean).json()
            products[ean] = (True if product.get else False)
            if product.get('name'):
                migros_product_counter = migros_product_counter + 1
                print "EAN %s is a migros product: %s" % (ean, product['name'])
    print ("Checked %i customers, %i transactions and %i products of " +
           "which %i are migros products.") % (
        len(customer_ids), len(transactions), len(products),
        migros_product_counter)


if __name__ == '__main__':
    crawl()
