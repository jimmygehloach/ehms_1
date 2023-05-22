(function() {
    let checkBoxes = $('input[type=checkbox]');
    let changeCheckboxClasses = (obj) => {
        if (obj.prop('checked') === true) {
            obj.parent('label').removeClass('checkbox-unchecked');
            obj.parent('label').addClass('checkbox-checked');
            obj.parent('label').find('p').text('Selected. Click to unselect.');
        } else if (obj.prop('checked') === false) {
            obj.parent('label').removeClass('checkbox-checked');
            obj.parent('label').addClass('checkbox-unchecked');
            obj.parent('label').find('p').text('Unselected. Click to select.');
        }
    }

    checkBoxes.each(function() {
        let _this = $(this);
        _this.hide();
        _this.parent('label').parent('div').addClass('checkbox-wrapper');
            changeCheckboxClasses(_this);
        });

        checkBoxes.on('click', function(e) {
            e.stopPropagation();
            let _this = $(this);
            changeCheckboxClasses(_this);
        });

})()
