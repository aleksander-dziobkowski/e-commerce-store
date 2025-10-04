document.getElementById("checkout-button").addEventListener("click", () => {
    fetch("/store/payu-create-order/", {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        if (data.redirectUri) {
            window.location.href = data.redirectUri;
        } else {
            alert("Something went wrong...");
            console.error(data);
        }
    });
});