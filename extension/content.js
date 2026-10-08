chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {

    if (request.action === "getProductData") {

        const product = extractProduct();

        sendResponse(product);
    }

    return true;
});


function extractProduct() {

    let product = {
        name: "",
        brand: "",
        price: "",
        image: "",
        seller: "",
        color: "",
        specifications: ""
    };


    product.name = findProductName();

    product.price = findPrice();

    product.brand = findBrand();

    product.image = findProductImage();

    product.seller = findSeller();

    product.color = findColor();

    product.specifications = findSpecifications();


    return product;
}


function findProductName() {

    let selectors = [
        "#productTitle",
        "h1",
        "[class*='product-title']",
        "[class*='ProductTitle']",
        "[class*='title']"
    ];

    for (let selector of selectors) {

        let element = document.querySelector(selector);

        if (element && element.innerText.trim()) {
            return element.innerText.trim();
        }
    }

    return "";
}


function findPrice() {

    let selectors = [
        ".a-price-whole",
        ".a-offscreen",
        "[class*='price']",
        "[class*='Price']"
    ];

    for (let selector of selectors) {

        let element = document.querySelector(selector);

        if (element && element.innerText.trim()) {
            return element.innerText.trim();
        }
    }

    return "";
}


function findBrand() {

    let selectors = [
        "#bylineInfo",
        "[class*='brand']",
        "[class*='Brand']"
    ];

    for (let selector of selectors) {

        let element = document.querySelector(selector);

        if (element && element.innerText.trim()) {
            return element.innerText.trim();
        }
    }

    return "";
}


function findProductImage() {

    let selectors = [
        "#landingImage",
        "#imgBlkFront",
        "[class*='product'] img",
        "[class*='Product'] img"
    ];

    for (let selector of selectors) {

        let element = document.querySelector(selector);

        if (element && element.src) {
            return element.src;
        }
    }

    return "";
}


function findSeller() {

    let selectors = [
        "#sellerProfileTriggerId",
        "#merchant-info",
        "[class*='seller']",
        "[class*='Seller']"
    ];

    for (let selector of selectors) {

        let element = document.querySelector(selector);

        if (element && element.innerText.trim()) {
            return element.innerText.trim();
        }
    }

    return "";
}


function findColor() {

    let text = document.body.innerText;

    let match = text.match(
        /Color\s*:?\s*([A-Za-z]+)/i
    );

    if (match) {
        return match[1];
    }

    return "";
}


function findSpecifications() {

    let selectors = [
        "#feature-bullets",
        "#productDetails",
        "[class*='specification']",
        "[class*='Specification']"
    ];

    for (let selector of selectors) {

        let element = document.querySelector(selector);

        if (element && element.innerText.trim()) {
            return element.innerText.trim();
        }
    }

    return "";
}