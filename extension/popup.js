document.getElementById("analyze").addEventListener(
    "click",
    analyzeProduct
);


async function analyzeProduct() {

    const button =
        document.getElementById("analyze");

    const status =
        document.getElementById("status");


    button.disabled = true;

    status.innerText =
        "Reading product information...";


    chrome.tabs.query(
        {
            active: true,
            currentWindow: true
        },
        function (tabs) {

            if (!tabs || !tabs[0]) {

                status.innerText =
                    "No active tab found.";

                button.disabled = false;

                return;
            }


            chrome.tabs.sendMessage(
                tabs[0].id,

                {
                    action: "getProductData"
                },

                async function (product) {

                    if (chrome.runtime.lastError) {

                        status.innerText =
                            "Cannot read this page.";

                        button.disabled = false;

                        return;
                    }


                    if (!product) {

                        status.innerText =
                            "Product not detected.";

                        button.disabled = false;

                        return;
                    }


                    displayProduct(product);


                    status.innerText =
                        "AI is analyzing the product...";


                    try {

                        const response =
                            await fetch(
                                "http://127.0.0.1:5050/analyze",
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body:
                                        JSON.stringify(product)
                                }
                            );


                        if (!response.ok) {

                            throw new Error(
                                "Backend returned error"
                            );
                        }


                        const result =
                            await response.json();


                        displayRisk(result);


                        status.innerText =
                            "AI analysis completed.";

                    }

                    catch (error) {

                        console.error(error);

                        status.innerText =
                            "Backend connection failed.";

                    }

                    finally {

                        button.disabled = false;

                    }

                }
            );

        }
    );
}


function displayProduct(product) {

    const productName =
        document.getElementById("productName");

    productName.innerText =
        product.name ||
        "Product not detected";


    const productDetails =
        document.getElementById("productDetails");

    const details =
        document.getElementById("details");


    details.innerHTML = "";


    addDetail(
        details,
        "Brand",
        product.brand
    );


    addDetail(
        details,
        "Price",
        product.price
    );


    addDetail(
        details,
        "Seller",
        product.seller
    );


    addDetail(
        details,
        "Color",
        product.color
    );


    productDetails.classList.remove(
        "hidden"
    );
}


function addDetail(
    container,
    name,
    value
) {

    const div =
        document.createElement("div");


    div.className =
        "feature";


    div.innerHTML =
        `<span>${name}</span>
         <span>${value || "Unavailable"}</span>`;


    container.appendChild(div);
}


function displayRisk(result) {

    const riskResult =
        document.getElementById("riskResult");


    riskResult.classList.remove(
        "hidden"
    );


    document.getElementById(
        "score"
    ).innerText =
        `${result.risk_score} / 100`;


    document.getElementById(
        "level"
    ).innerText =
        `${result.risk_level} RISK`;


    displayFeatures(
        result.features
    );


    displayAIAnalysis(
        result
    );


    displayOCR(
        result.ocr_analysis
    );


    displayWarnings(
        result.warnings
    );
}


function displayFeatures(features) {

    const container =
        document.getElementById(
            "features"
        );


    container.innerHTML = "";


    if (!features) {

        return;
    }


    addFeature(
        container,
        "Image",
        features.image
    );


    addFeature(
        container,
        "Brand / Logo",
        features.brand_logo
    );


    addFeature(
        container,
        "Price",
        features.price
    );


    addFeature(
        container,
        "Seller",
        features.seller
    );


    addFeature(
        container,
        "Specifications",
        features.specifications
    );


    addFeature(
        container,
        "Color",
        features.color
    );


    addFeature(
        container,
        "Size",
        features.size
    );
}


function addFeature(
    container,
    name,
    value
) {

    const div =
        document.createElement("div");


    div.className =
        "feature";


    div.innerHTML =
        `<span>${name}</span>
         <span>${value} / 100</span>`;


    container.appendChild(div);
}


function displayAIAnalysis(result) {

    const container =
        document.getElementById(
            "aiAnalysis"
        );


    container.innerHTML = "";


    const similarity =
        result.similarity_analysis;


    const imageAnalysis =
        result.image_analysis;


    const box =
        document.createElement("div");


    box.className =
        "ai-box";


    if (similarity) {

        box.innerHTML += `

            <div class="ai-item">

                <strong>CLIP Similarity:</strong>

                ${similarity.similarity}%

            </div>

            <div class="ai-item">

                <strong>CLIP Image Risk:</strong>

                ${similarity.risk} / 100

            </div>

        `;
    }


    if (
        imageAnalysis &&
        imageAnalysis.objects
    ) {

        box.innerHTML += `
            <div class="ai-item">

                <strong>YOLO Objects:</strong>

            </div>
        `;


        if (
            imageAnalysis.objects.length === 0
        ) {

            box.innerHTML +=
                `<div>No recognizable object detected</div>`;

        }

        else {

            imageAnalysis.objects.forEach(
                function (object) {

                    box.innerHTML += `

                        <div>

                            ${object.object}

                            -

                            ${object.confidence}%

                        </div>

                    `;

                }
            );

        }

    }


    container.appendChild(box);
}


function displayOCR(ocr) {

    const container =
        document.getElementById(
            "ocrAnalysis"
        );


    container.innerHTML = "";


    if (!ocr) {

        return;
    }


    const box =
        document.createElement("div");


    box.className =
        "ai-box";


    if (!ocr.success) {

        box.innerHTML =
            `<div class="error">
                OCR analysis failed
             </div>`;

        container.appendChild(box);

        return;
    }


    if (
        !ocr.text ||
        ocr.text.length === 0
    ) {

        box.innerHTML =
            `<div>
                No readable text detected
             </div>`;

    }

    else {

        box.innerHTML =
            `<strong>Detected Text:</strong>`;


        ocr.text.forEach(
            function (item) {

                box.innerHTML += `

                    <div class="ai-item">

                        ${item.text}

                        -

                        ${item.confidence}%

                    </div>

                `;

            }
        );

    }


    container.appendChild(box);
}


function displayWarnings(warnings) {

    const container =
        document.getElementById(
            "warnings"
        );


    container.innerHTML = "";


    if (
        !warnings ||
        warnings.length === 0
    ) {

        container.innerHTML =
            `<div class="success">
                No major warnings detected.
             </div>`;

        return;
    }


    warnings.forEach(
        function (warning) {

            const div =
                document.createElement("div");


            div.className =
                "warning";


            div.innerText =
                "⚠ " + warning;


            container.appendChild(div);

        }
    );
}