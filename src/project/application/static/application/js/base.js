const ALERT_TYPES = {
    "SUCCESS": "success",
    "WARNING": "warning",
    "ERROR": "error",
}

function add_alert(alert_type, message){
    const new_alert = `
    <li class="${alert_type} alert-message">
        <span>${message}</span>
        <i id="" class="fa-solid fa-x close-message-btn" onclick="remove_alert(this)"></i>
    </li>
    `;
    $("#alert-messages ul").append(new_alert);
}

function remove_alert(element) {
    const nearest_li = element.closest("li");
    nearest_li.remove();
}



$(document).ready(function () {
    $(".close-message-btn").click((event) => remove_alert(event.currentTarget));
})