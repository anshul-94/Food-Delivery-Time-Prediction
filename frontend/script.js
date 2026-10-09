
const form = document.getElementById("prediction-form");
const button = document.getElementById("predict-button");
const buttonText = document.getElementById("button-text");
const result = document.getElementById("result");
const prediction = document.getElementById("prediction");
const errorMessage = document.getElementById("error-message");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    result.hidden = true;
    errorMessage.hidden = true;

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    // Convert numeric form fields from strings to numbers.
    const numericFields = [
        "Delivery_person_Age",
        "Delivery_person_Ratings",
        "Vehicle_condition",
        "multiple_deliveries",
        "Delivery_Distance",
        "Order_Hour",
        "Order_Minute",
        "Month",
        "Is_Weekend",
    ];

    for (const field of numericFields) {
        payload[field] = Number(payload[field]);
    }

    button.disabled = true;
    buttonText.textContent = "Predicting...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = data.detail;
            const message = Array.isArray(detail)
                ? detail.map((item) => item.msg).join("; ")
                : typeof detail === "string"
                    ? detail
                    : "The prediction request failed.";

            throw new Error(message);
        }

        prediction.textContent =
            data.predicted_delivery_time_minutes.toFixed(2);

        result.hidden = false;
        result.scrollIntoView({
            behavior: "smooth",
            block: "nearest",
        });
    } catch (error) {
        errorMessage.textContent =
            error.message || "Unable to reach the prediction API.";

        errorMessage.hidden = false;
    } finally {
        button.disabled = false;
        buttonText.textContent = "Predict delivery time";
    }
});
