fetch("/config/")
            .then((result) => {
                return result.json();
            })
            .then((data) => {
                // Initialize Stripe.js
                const stripe = Stripe(data.publicKey);

                // new
                // Event handler
                let submitBtn = document.querySelector("#submitBtn");
                if (submitBtn !== null) {
                    submitBtn.addEventListener("click", () => {
                        // Get Checkout Session ID
                        fetch("/create-checkout-session/")
                            .then((result) => {
                                return result.json();
                            })
                            .then((data) => {
                                console.log(data);
                                // Redirect to Stripe Checkout
                                return stripe.redirectToCheckout({
                                    sessionId: data.sessionId
                                })
                            })
                            .then((res) => {
                                console.log(res);
                            });
                    });
                }
                let submitBtn2 = document.querySelector("#submitBtn1");
                if (submitBtn2 !== null) {
                    submitBtn2.addEventListener("click", () => {
                        // Get Checkout Session ID
                        fetch("/create-checkout-session1/")
                            .then((result) => {
                                return result.json();
                            })
                            .then((data) => {
                                console.log(data);
                                // Redirect to Stripe Checkout
                                return stripe.redirectToCheckout({
                                    sessionId: data.sessionId
                                })
                            })
                            .then((res) => {
                                console.log(res);
                            });
                    });
                }
            });