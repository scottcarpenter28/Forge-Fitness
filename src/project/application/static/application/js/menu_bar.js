$(document).ready(function(){
    // The div representing the menu bar.
    const menu_bar = $('#menu-bar');
    // The button to open the div with.
    const toggle_open_btn = $("#toggle-menu-open")
    // The button to close the div with.
    const toggle_close_btn = $("#toggle-menu-close")

    $(toggle_open_btn).click(function(){
        menu_bar.animate({"left":"0"}, "slow");
        toggle_open_btn.hide();
        toggle_close_btn.fadeIn();
    });

    $('#toggle-menu-close').click(function(){
        menu_bar.animate({"left":"-500px"}, "slow");
        toggle_open_btn.fadeIn();
        toggle_close_btn.hide();
    });

});