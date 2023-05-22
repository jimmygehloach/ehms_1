$.ajax({
    url: URL,
    cache: 'false',
    dataType: 'json',
    type: 'POST',
    data: dataObj,
    beforeSend: function (xhr) {
        target.html('<option value="">Loading ...</option>');
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}')
    },
}).done(function (data) {
   // change the target options with the
    // fetched data from the server
    let htmlCode;
    htmlCode += '<option value="" selected>Choose your option</option>';
    console.log(data);
    $.each(data, function (index, value) {
        htmlCode += '<option value="' +  value.id  + '">' + value.full_name + '</option>';
    });
    target.html(htmlCode);
}).fail(function (e) {
    // on fail show helping message
    let htmlCode;
    if ( e === 404 ) {
        htmlCode = '<option value="" hidden>Ward not found.</option>';
    } else if (e === 405) {
        htmlCode = '<option value="" hidden>Method not allowed.</option>';
    } else {
        htmlCode = '<option value="" hidden>Something went wrong. Try again.</option>';
    }
    target.html(htmlCode);
});
