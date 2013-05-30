Checkout Items, get Orders and add Invoices and Shipments
=========================================================

Setup
-----
::

    >>> magento_url = "http://hobby.developlocal.sativa.jokasis.de/"
    >>> from splinter import Browser
    >>> browser = Browser('chrome', wait_time=16)

    >>> import yaml
    >>> import pytest
    >>> import time
    >>> from webtest import TestApp, AppError
    >>> from organicseeds_webshop_api import main
    >>> from organicseeds_webshop_api.testing import get_file, testconfig, reset_database_with_testdata, store_database_with_testdata
    >>> app = TestApp(main(testconfig()))


We start with a fresh database and testdata items/groups/categories::

    >>> reset_database_with_testdata()


Checkout Items
--------------

Add item to shopping card::

    >>> item_url = "http://hobby.developlocal.sativa.jokasis.de/titlede-itemka32-de.html"
    >>> browser.visit(item_url)
    >>> qty = browser.find_by_name('qty').first
    >>> browser.find_by_css('.btn-cart').first.click()
    >>> browser.is_element_present_by_css(".btn-proceed-checkout")
    True

Checkout  as guest with required data::

    >>> browser.find_by_css(".btn-checkout").first.click()
    >>> browser.is_element_present_by_name("checkout_method")
    True
    >>> browser.check("checkout_method")
    >>> browser.find_by_id("onepage-guest-register-button").first.click()

Set billing addresss:

    >>> browser.is_element_present_by_id("checkout-step-billing")
    True
    >>> browser.fill("billing[firstname]", "Joscha")
    >>> browser.fill("billing[lastname]", "krutzki")
    >>> browser.fill("billing[email]", "joka@developlocal.sativa.jokasis.de")
    >>> browser.fill("billing[street][]", "Engelstrasse 3")
    >>> browser.fill("billing[city]", "Zurich")
    >>> browser.fill("billing[postcode]", "8003")
    >>> browser.fill("billing[telephone]", "00410498273")
    >>> browser.select('billing[country_id]', 'CH')
    >>> browser.select('billing[region_id]', '104')
    >>> browser.find_by_css("#billing-buttons-container .button").first.click()

Choose shipping::

    >>> browser.is_element_present_by_css("#checkout-step-shipping_method button")
    True
    >>> time.sleep(4)
    >>> browser.find_by_css("#shipping-method-buttons-container button").first.click()

Choose payone online payment::

   ..>>> browser.is_element_present_by_id("checkout-step-payment")
   ..True
   ..>>> time.sleep(4)
   ..>>> browser.find_by_css("#p_method_payone_creditcard").first.check()
   ..>>> browser.is_element_present_by_id("payone_creditcard_cc_type_select")
   ..True
   ..>>> browser.select('payone_creditcard_cc_type_select', '3_V')
   ..>>> browser.fill("payment[cc_number]", "4111111111111111")
   ..>>> browser.select("payment[cc_exp_month]", "11")
   ..>>> browser.select("payment[cc_exp_year]", "2015")
   ..>>> browser.find_by_css("#payment-buttons-container .button").first.click()

Choose offline payment::

   >>> browser.is_element_present_by_id("checkout-step-payment")
   True
   >>> time.sleep(4)
   >>> browser.find_by_id("p_method_invoice").first.check()
   >>> browser.find_by_css("#payment-buttons-container .button").first.click()

Review order::

   >>> browser.is_element_present_by_id("checkout-step-review")
   True
   >>> time.sleep(4)
   >>> browser.check("agreement[1]")
   >>> browser.check("agreement[2]")
   >>> browser.find_by_css("#review-buttons-container .button").first.click()
   >>> time.sleep(4)
   >>> "Vielen Dank" in browser.html
   True

Store database, to make testing with payone work we may not reuse order_increment_ids::

   >>> store_database_with_testdata()


Get Orders:
-----------

Every checkout creates an new order with status "pending".
We can list all new orders:

    >>> resp = app.get('/orders', {"status": "pending"})
    >>> orders = resp.json_body["orders"]
    >>> orders
    [{u'shop...

and get the latest::

    >>> order = orders.pop()
    >>> order_id = order["order_increment_id"]
    >>> order_id
    200...

No order item is invoiced and  paid yet::

    >>> item = order["items"][0]
    >>> order['total_paid']
    0
    >>> order['total_invoiced']
    0

Now we can invoice and capture the online payment

    >>> invoices_post_data = {"invoices": [{"order_increment_id": order_id,
    ...                       "order_item_qtys": [{"order_item_id": item["order_item_id"],
    ...                                            "qty": item["qty_ordered"]}]
    ...                       }]}
    >>> resp = app.put_json('/invoices', invoices_post_data)
    >>> resp.json_body
    {u'invoice_results': [{u'order_increment_id...

The order is now in state "processing"::

    >>> resp = app.get('/orders', {"status": "processing"})
    >>> orders = resp.json_body["orders"]
    >>> order = orders.pop()
    >>> order["order_increment_id"] == order_id
    True

Order items are invoiced::

    >>> order['total_invoiced']
    7.56

If all is payed and shipped we set the order status to "complete":


    >>> app.put_json('/orders', {"orders": [{"order_increment_id": order_id, "status": "complete"}]})
    <200 OK app...

    >>> resp = app.get('/orders', {"status": "complete"})
    >>> orders = resp.json_body["orders"]
    >>> order_updated = orders.pop()
    >>> order_updated["order_increment_id"] == order_id
    True
