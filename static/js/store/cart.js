/**
 * Created by Dmitriy on 14.04.2016.
 */

$(document).ready(function(){
    $('.add-to-cart-button').each(function(i, obj) {
    //test
    });
});

function addToCart(modificationId) {
    Cookies.set('cart_products', modificationId);
}