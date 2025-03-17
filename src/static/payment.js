// Initialize Stripe with your public key
const stripe = Stripe(pk_test_51QCHnvExyakfDI8GZ3wGl3QqBkWHeSQ0MsBHBWMCPrSje7xDAgP80J1vXkReiunG9npvEQLS10JiUUXMm2vc3kK500dQKuYi0O);

// Create an instance of Elements
const elements = stripe.elements();

// Create an instance of the card Element
const card = elements.create('card');

// Add an instance of the card Element into the `card-element` <div>
card.mount('#card-element');

// Get references to the form and submit button
const form = document.getElementById('payment-form');
const submitButton = document.getElementById('submit');

// Handle form submission
form.addEventListener('submit', function(event) {
    event.preventDefault();
    submitButton.disabled = true;

    // Fetch the client secret from your backend
    fetch('/api/payments/create-payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Include authentication token if necessary
            'Authorization': 'Bearer ' + b316850672976d2af2f5c0a568f3d987724c1a22003333625a9335c6c771848c  // Replace with actual token
        },
        body: JSON.stringify({ order_id: orderId })
    })
    .then(response => response.json())
    .then(data => {
        const clientSecret = data.client_secret;

        // Confirm the payment with the client secret
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card
            }
        }).then(function(result) {
            if (result.error) {
                // Show error to your customer
                console.error(result.error.message);
                submitButton.disabled = false;
            } else {
                // The payment succeeded!
                if (result.paymentIntent.status === 'succeeded') {
                    console.log('Payment succeeded!');
                    // Redirect the user to a success page or show success message
                    window.location.href = '/payment-success';
                }
            }
        });
    })
    .catch((error) => {
        console.error('Error:', error);
        submitButton.disabled = false;
    });
});
