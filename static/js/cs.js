function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


(function($){

    $(function() {

        console.log(document.cookie);

        let itemCategory = $('#id_item_category');

        itemCategory.on('change', function() {

            let $this = $(this);
            let itemCategoryId = $this.val();

            $.ajax({
                url: "/inventory/items/",
                cache: 'false',
                dataType: 'json',
                type: 'POST',
                data: {
                    'category_id': itemCategoryId
                },
                beforeSend: function( xhr ) {
                    xhr.setRequestHeader('X-CSRFToken', '')
                },
            }).then(function( data ) {
                if ( console && console.log ) {
                    console.log( data );
                }
            },function( data ) {
                if ( console && console.log ) {
                    console.log( data );
                }
            });
        });

    });
})(jQuery)

