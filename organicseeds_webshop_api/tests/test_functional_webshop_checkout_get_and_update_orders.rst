Checkout Items, get Orders and add Invoices and Shipments
=========================================================

Setup
-----
::

    >>> magento_url = "http://hobby.developlocal.sativa.jokasis.de/"
    >>> from splinter import Browser
    >>> browser = Browser(wait_time=5)

    >>> import yaml
    >>> import pytest
    >>> from webtest import TestApp, AppError
    >>> from organicseeds_webshop_api import main
    >>> from organicseeds_webshop_api.testing import get_file, testconfig, reset_database_with_testdata
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
    >>> browser.is_text_present("Zur Kasse gehen")
    True

Checkout  as guest with required data::

    >>> browser.find_by_css(".btn-checkout").first.click()
    >>> browser.is_text_present("Checkout Method")
    True
    >>> browser.check("checkout_method")
    >>> browser.find_by_id("onepage-guest-register-button").first.click()

Set billing addresss:

    >>> browser.fill("billing[firstname]", "billing_firstname")
    >>> browser.fill("billing[lastname]", "billing_lastname")
    >>> browser.fill("billing[email]", "joka@developlocal.sativa.jokasis.de")
    >>> browser.fill("billing[street][]", "billing_street1")
    >>> browser.fill("billing[city]", "billing_city")
    >>> browser.fill("billing[postcode]", "billing_postcode")
    >>> browser.fill("billing[telephone]", "billing_telephone")
    >>> browser.select('billing[country_id]', 'CH')
    >>> browser.select('billing[region_id]', '104')
    >>> browser.find_by_css("#billing-buttons-container .button").first.click()

Choose shipping::

   >>> browser.find_by_css("#shipping-method-buttons-container .button").first.click()

Choose payment::

   >>> browser.check("payment[method]")
   >>> browser.find_by_css("#payment-buttons-container .button").first.click()

Review order::

   >>> browser.find_by_css("#review-buttons-container .button").first.click()
   >>> "Vielen Dank" in browser.html
   True


Get Orders:
-----------

Every checkout creates an new order. We can list all oder information::

    >>> app.get('/orders')
    <200 OK application/json body=...
