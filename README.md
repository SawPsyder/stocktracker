# stocktracker
Small python stock tracker experiment.
Uses selenium to get stock data from configured webshop urls.

## Installation
1. Install python on your system, Im using 12.8.
2. Install at least Chrome v133 on your system. If not the latest version, the stealth driver might not work and a fallback to the normal driver is used.
3. Start `install.bat` once to let it install all dependencies in a virtual environment.
4. Start `run.bat` once to generate the `config.json` file.
5. Edit the config file es specified below.
6. Start `run.bat` to run the program.

## Configuration
The sample configuration file `config.json` is - surprise - formatted in JSON.
Just edit the values and add new checks and rules as needed.

I hope the structure is self-explanatory. If not, here is a short explanation:

```json
[
    {
        "class": "Check", // The class of the object. Currently only "Check" is supported. Thats needed to decode the json, dont change it.
        "name": "MSI GeForce RTX 5090 Ventus 3X OC", // The name of the product you want to track.
        "rules": [ // These rules are OR-based. If one of them is true, the product marked as is in stock.
            {
                "class": "RuleWebsite", // The class of the object. Currently only "RuleWebsite" is supported. Thats needed to decode the json, dont change it.
                "name": "Alternate DE", // The name of the website you want to track.
                "url": "https://www.alternate.de/MSI/GeForce-RTX-5090-32G-VENTUS-3X-OC-Grafikkarte/html/product/100109567", // The url of the product.
                "search_text": "In den Warenkorb", // The text to be found in the HTML of the website.
                "search_element": ".cart-btn-text" // This is optional. If specified, the search_text will be searched in this element. This is a basic CSS selector.
            },
            {
                "class": "RuleWebsite", // Some website will not work, this is an example - at least not without a captcha protection.
                "name": "Caseking DE",  // Caseking has some kind of protection against bots.
                "url": "https://www.caseking.de/msi-geforce-rtx-5090-32g-ventus-3x-oc-32768-mb-gddr7/GCMC-403.html", 
                "search_text": "Auf Lager",
                "search_element": "#js-product-availability-container",
                "perform_cloudflare_check": true // This is optional. If set to true, it will be tried to solve a cloudflare checkbox protection.
            },
            {
                "class": "RuleWebsite",
                "name": "Amazon DE", // Amazon is working - but too many requests will get you in a captcha protection, that can not be solved automatically.
                "url": "https://www.amazon.de/dp/B0DT6S77JK",
                "search_text": "Auf Lager",
                "search_element": "#availability",
                "timeout": 2 // You can use timeouts (default is 1s) to wait longer for a website to load. This can also be used to slow down the request speed to run less in bot protections.
            }
        ]
    }
]
```

### Bot protection notice
This is basically some kind of web scraping. 
Some websites have bot protection, which will block you from accessing the website.

To check if a website is working or running in a bot protection you can follow the steps it takes in Chrome.
Or:
1. Let the program run once with your configuration.
2. Open the `archive` folder
3. Open the `.html` file that begins with the name of your rule.
4. See if the content that needs to be check is included in this file.