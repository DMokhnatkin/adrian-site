var cartCookieName = 'products_in_cart';
var cartReloadUrl = '/store/cart/cartPreview';
var cartCheckoutUrl = '/store/cart/checkout';

$(document).ready(function(){
    // Add logic for toolbox buttons
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

    // Change in cart count when cart is changed
    $(document).on('cartChanged', function () {
        $('.count-val').each(function () {
            $(this).html(getCountInCart($(this).attr('id').substr(4)));
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
    Cookies.set(cartCookieName, prods, { expires: 30 });
    $(document).trigger('cartChanged');
}

function removeFromCart(productId) {
    var prods = getProdsInCart();
    prods = (prods) ? prods : {};
    delete prods[productId];
    Cookies.set(cartCookieName, prods, { expires: 30 });
    $(document).trigger('cartChanged');
}

// Clear cart
function clear() {
    Cookies.remove(cartCookieName, null);
    $(document).trigger('cartChanged');
}

// Decrease product in cart count
function decInCart(prodId, ct){
    var curCt = getCountInCart(prodId);
    if (curCt) {
        if (curCt - ct <= 0)
            removeFromCart(prodId);
        else
            setCountInCart(prodId, curCt - ct);
    }
}

// Increase product in cart count
function incInCart(prodId, ct){
    var curCt = getCountInCart(prodId);
    if (curCt) {
        setCountInCart(prodId, curCt + ct);
    }
    else {
        setCountInCart(prodId, ct);
    }
}