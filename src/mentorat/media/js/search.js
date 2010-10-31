function field_of_interest_changed(view, field_index) {
    var search = $("#search").val()
    if (view == "mentorship_admin")
    {
        url = "/mentorship_admin/search/?field=" + field_index
    }
    else
    {
        url = "/profiles/?field=" + field_index
    }
    url += "&search=" + search
    document.location = url

    return false;
}

/* sets the field to the selected field of interest */
function search_button_pressed(view, field) {
    var field_index = document.getElementById("field_select").selectedIndex
    field.value = field_index

    return false;
}
