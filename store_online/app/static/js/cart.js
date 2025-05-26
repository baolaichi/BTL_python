document.addEventListener('DOMContentLoaded', function() {
    // Update cart quantity with AJAX
    document.querySelectorAll('.update-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const action = this.dataset.action;

            fetch(`/cart/api/update/${itemId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ action: action })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.removed) {
                        document.querySelector(`.cart-item-${itemId}`).remove();
                    } else {
                        document.querySelector(`.quantity-${itemId}`).textContent = data.quantity;
                        document.querySelector(`.item-total-${itemId}`).textContent =
                            `$${data.item_total.toFixed(2)}`;
                    }

                    document.querySelector('.cart-total').textContent = `$${data.cart_total.toFixed(2)}`;
                    document.querySelector('.cart-count').textContent = data.cart_count;

                    // Show success message
                    const alert = document.createElement('div');
                    alert.className = 'alert alert-success alert-dismissible fade show';
                    alert.innerHTML = `
                        Cart updated successfully!
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    `;
                    const container = document.querySelector('.container');
                    container.prepend(alert);

                    // Auto dismiss after 3 seconds
                    setTimeout(() => {
                        alert.classList.remove('show');
                        alert.classList.add('fade');
                    }, 3000);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});