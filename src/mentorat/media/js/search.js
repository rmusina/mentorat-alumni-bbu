function field_of_interest_changed(field_index) {
    var search = $("#search").val()
    url = "/mentorship_admin/search/?field=" + field_index
    document.location = url

    return false;
}
