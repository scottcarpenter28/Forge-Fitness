$(document).ready(function () {
    $(".close-message-btn").click(function (event) {
        const current_element = event.currentTarget;
        const nearest_li = current_element.closest("li");
        nearest_li.remove();
    });
})