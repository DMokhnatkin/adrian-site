var cartCookieName = 'products_in_cart';
var cartReloadUrl = '/store/cart/cartPreview';
var cartCheckoutUrl = '/store/cart/checkout';

$(document).ready(function(){
    // Add logic for add-to-cart buttons
    $('a.add-to-cart').click(function () {
        var prodId = this.id.substr(3);
        setCountInCart(prodId, getCountInCart(prodId) + 1);
        return false;
    });
    
    // Add logic for preview toolbox buttons
    $(document).on('cartPreviewLoaded', function () {
        $('a.clear-cart').click(function () {
            if (confirm('Очистить корзину?'))
            {
                clear();
            }
        });
    });

    // Reload cart preview when cart is changed
    $(document).on('cartChanged', function () {
        $.ajax({
            url: cartReloadUrl,
            type: 'GET',
            data:
            {
                'products' : JSON.stringify(getProdsInCart())},
            dataType: 'html',
            success: function (data) {
                $('#cart-preview-block').html(data);
                $(document).trigger('cartPreviewLoaded');
            }
        });
    });
    $(document).trigger('cartChanged');
});

function getProdsInCart() {
    var cookie = Cookies.get(cartCookieName);
    if (!cookie)
        return {};
    else
        return jQuery.parseJSON(cookie);
}

// Get count of specified product in cart
function getCountInCart(productId) {
    var prods = getProdsInCart();
    return (!prods[productId]) ? 0 : prods[productId];
}

// Set count of specified product in cart
function setCountInCart(productId, count) {
    var prods = getProdsInCart();
    prods = (prods) ? prods : {};
    prods[productId] = count;
    Cookies.set(cartCookieName, prods, { expires: 7 });
    $(document).trigger('cartChanged');
}

// Clear cart
function clear() {
    Cookies.remove(cartCookieName, null);
    $(document).trigger('cartChanged');
}