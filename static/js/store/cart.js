/**
 * Created by Dmitriy on 14.04.2016.
 */

$(document).ready(function(){
    $('.add-to-cart-button').each(function(i, obj) {
    //test
    });
	$('.add-to-cart-button').bind('change', validateDate);
});

function addToCart(modificationId) {
    Cookies.set('cart_products', modificationId);
}