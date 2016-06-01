/**
 * Created by Dmitriy on 06.05.2016.
 */

$(document).ready(function () {
    $('.address-field').autocomplete({
        source: []
    });
    $('.address-field').on('input', function () {
       ymaps.suggest($(this).val()).then(function (items) {
           var addresses = [];
           $.each(items, function (key, val) {
               addresses.push(val.displayName);
           });
           $(".address-field").autocomplete("option", "source", addresses);
       });
    });
});