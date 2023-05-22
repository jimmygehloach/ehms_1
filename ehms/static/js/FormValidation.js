
class FormValidation {
    /*
    * Form Validation class
    *
    * This class is made with intention of validating form.
    * If you have to validate the html form at front end
    * then you can use this class. The steps you required
    * to utilise this class are mentioned in this description.
    *
    * Steps involved within html <form> <!--form--> </form> : -
    * ------------------------------------------------------
    *   1. Create data-validation (By default) attribute
    *      on each field of the form which you suppose to validate.
    *   2. If you want to display message then provide
    *      data-message (By default) attribute on form fields.
    *   3. If you do not want to display messages then by default
    *      messages will be displayed, if the message feature
    *      is turned on. By default, it is turned off.
    *   4. In data-validation attribute each validation should
    *      be  seperated with a symbol. By default, it is
    *      pipe "|" symbol and validation parameters are
    *      started  with colon ":" symbol whereas seperated with
    *      comma "," symbol. These symbols can be easily replaced
    *      when you instantiate this class.
    *
    * Note: -
    * -----------------------------------------------------------------------
    *   1. The validation methods and their messages are need to be
    *      synchronized. Make sure they are typed in the similar order.
    *   2. If you want to skip any message against validation method
    *      then simple keep it empty.
    *      e.g: - data-validation="required|username|max:20|min:5"
    *      data-message="This is required field.|Username is invalid|||".
    *      In this example you do not want to provide the last two validation
    *      method's messages. So, the default message will fire.
    *
    * Steps involved within <script> //tags </script> : -
    * ------------------------------------------------
    *   1. Instantiate the class.
    *   2. Provide the form id.
    *   3. Change the defaults, if you're not satisfied.
    *   4. That's it. Thank you.
    *
    * @params (object: formId is mandatory ... rest are optional)
    * @returns Nothing| but do some changes (validation response) in the
    *          DOM of the form whose id is provided.
    * @author JBG
    * */

    #formId = '';
    #generalEvents = ['keyup', 'keydown', 'click']
    #eventName = 'keyup'; // redundant
    #eventSelectName = 'change'; // redundant
    #selectEvents = ['click', 'change'];
    #validationAttributeName = 'data-validation';
    #flagName = 'data-flag';
    #fireEventHandler = true
    #errorColor = 'rgba(255,0,0,0.15)';
    #successColor = 'rgba(0,255,0,0.15)';
    #onPageLoad = false;
    #validationSeparator = '|';
    #validationArgumentSeparator = ':';
    #validationMessageSeparator = '|';
    #validatorWithinSeparator = ',';
    #regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    #usernameRegex = /^[a-zA-Z0-9_]+$/;
    #decimalRegex = /^-?[\d]+\.[\d]+$/;
    #showMessages = true
    #showDefaultMessages = true
    #showColorFormFields = true
    #listStyle = 'ordered' // 'ordered' || 'unordered'
    #fieldSelectors = 'input, select, textarea'
    #uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
    #fileSizes = ['GB','MB','KB'];
    #validFileExtensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'xlx', 'xlsx'];
    #imageExtensions = ['jpg', 'jpeg', 'png', 'gif'];

    #defaultMessage = {
        username: 'Username is invalid.',
        email: 'Email is invalid.',
        address: "Invalid entry of address. Characters allowed are @:;&_\"'(),.-s",
        phone: "Invalid entry of phone. Only 9 to 12 digits are allowed.",
        required: 'This field is required.',
        within: 'This field is invalid.',
        max: 'Value exceeded the limit.',
        min: 'Value should be greater than the limit.',
        checkDate: 'Date is invalid.',
        checkTime: 'Time is invalid.',
        exact: 'Value is invalid.',
        digit: 'Value must consist of digits only.',
        decimal: 'Invalid decimal number.',
        alphaNum: 'Value should only contain alpha numeric',
        alpha: 'Value should only contain alpha characters.',
        uuid: 'Invalid UUID. Data is altered.',
        fileSize: 'Check the required file size limit.',
        fileExtension: 'Chosen file is invalid.',
    }

    #regxParams = {
        space: '\\s',
        comma: '\\,',
        hyphen: '\\-',
        dot: '\\.',
        brackets: '\\(\\)',
    }

    #regexDate = {
        'yyyy-mm-dd': /^(\d{4}-\d{2}-\d{2})$/,
        'yy-mm-dd': /^(\d{2}-\d{2}-\d{2})$/,
        'dd-mm-yyyy': /^(\d{2}-\d{2}-\d{4})$/,
        'dd-mm-yy': /^(\d{2}-\d{2}-\d{2})$/,
        'yyyy/mm/dd': /^(\d{4}\/\d{2}\/\d{2})$/,
        'yy/mm/dd': /^(\d{2}\/\d{2}\/\d{2})$/,
        'dd/mm/yyyy': /^(\d{2}\/\d{2}\/\d{4})$/,
        'dd/mm/yy': /^(\d{4}\/\d{2}\/\d{2})$/
    };
    #regexAddress = /^[\da-zA-Z@:;&_"'(),.\-\s]+$/
    #regexPhone = /^(\d{9,15})$/
    #regexAlpha = /^[a-zA-Z]+$/

    #timeFormats = ['12','24'];
    #timePatterns = {
        'seconds': /^(\d{1,2}):(\d{1,2}):(\d{1,2})$/,
        'minutes': /^(\d{1,2}):(\d{1,2})$/
    }
    #digitRegx = /^(\d)+$/;

    #form = [];
    #fields = [];
    #messageBox = [];
    #validationMethodsReturnValue = [];
    #disableInlineStyle = false;
    #showErrorCounts = true;
    #errorCount = 0;
    #fileEvents = ['keyup', 'keydown', 'click', 'focus'];
    #imagePreviewContainer = '';
    #imagePreviewShow = true;
    #ownErrorCountId;
    #defaultErrorCountId;

    /**
     *
     * @param obj
     */
    constructor(obj) {
        // formId check
        if ( obj.formId === '' || obj.formId === null || obj.formId === false || typeof obj.formId === 'undefined' ) {
            throw new Error('Form id is required.');
        }

         // formID parameter : mandatory
        this.#formId = obj.formId;

        // default parameters : optionals
        this.#fireEventHandler = obj.fireEventHandler ??= true;
        this.#eventName = obj.eventName ??= 'keyup'; // redundant
        this.#generalEvents = obj.generalEvents ??= ['keyup', 'keydown', 'click'];
        this.#selectEvents = obj.selectEvents ??= ['click', 'change'];
        this.#fileEvents = obj.selectEvents ??= ['keyup', 'keydown', 'click', 'focus'];
        this.#validationAttributeName = obj.validationAttributeName ??= 'data-validation';
        this.#flagName = obj.flagName ??= 'data-flag';
        this.#errorColor = obj.errorColor ??= 'rgba(255,0,0,0.15)';
        this.#successColor = obj.successColor ??= 'rgba(0,255,0,0.15)';
        this.#onPageLoad = obj.onPageLoad ??= false;
        this.#validationSeparator = obj.validationSeparator ??= '|';
        this.#validationArgumentSeparator = obj.validationArgumentSeparator ??= ':';
        this.#validationMessageSeparator = obj.validationMessageSeparator ??= '|';
        this.#validatorWithinSeparator = obj.validatorWithinSeparator ??= ',';
        this.#regexEmail = obj.emailRegex ??= /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        this.#usernameRegex = obj.usernameRegex ??= /^[a-zA-Z0-9_]+$/;
        this.#decimalRegex = obj.decimalRegex ??= /^-?[\d]+\.[\d]+$/;
        this.#showMessages = obj.showMessages ??= true;
        this.#showDefaultMessages = obj.showMessages ??= true;
        this.#showColorFormFields = obj.showMessages ??= true;
        this.#listStyle = obj.listStyle ??= 'ordered';
        this.#fieldSelectors = obj.fieldSelectors ??= 'input, select, textarea';
        this.#disableInlineStyle = obj.disableInlineStyle ??= this.#disableInlineStyle;
        this.#regexAddress = obj.regexAddress ??= /^[\da-zA-Z@:;&_"'(),.\-\s]+$/;
        this.#regexPhone = obj.regexPhone ??= /^(\d{9,12})$/;
        this.#regexAlpha = obj.regexAlpha ??= /^[a-zA-Z]+$/;
        this.#imagePreviewContainer = obj.imagePreviewContainer ??= '';
        this.#showErrorCounts = obj.showErrorCounts ??= true;
        this.#ownErrorCountId = obj.ownErrorCountId ??= null;
        this.#defaultErrorCountId = obj.defaultErrorCountId ??= 'form-errors-count';

        // setting up form
        this.#form = document.getElementById(this.#formId);

        // method calls
        this.#extractFields();
        this.#theSubmitter();
    }

    #extractFields() {
        /**
         * Scan all the fields in the form and form a nodeset
         * which will get stored into the #fields property.
         * The next step after this will be the extraction
         * of validation attribute from each element kept under
         * validation.
         *
         * @type {NodeListOf<HTMLElementTagNameMap[string]>}
         */
        this.#fields = this.#form.querySelectorAll(this.#fieldSelectors);
        this.#extractValidationAttribute();
    }

    #extractValidationAttribute() {
        /**
         * Its primary job is to extract validation attribute
         * from the extracted fields stored in #fields property.
         * BUT ...
         * If #fireEventHandler switch is on (By default, it is on.)
         * then it will send each field element to #activateEventHandler method
         * to activate event on each element behaviour. The behaviour
         * will be determined by the event applied. By default,
         * the event is "keyup". But you can change it whatever you
         * desire to be. Make sure it makes some sense.
         */
        this.#fields.forEach((element) => {
            if ( this.#fireEventHandler ) {
                this.#activateEventHandler(element)
            }
            if ( this.#onPageLoad ) {
                this.#commonExtraction(element);
            }
        })
    }

    #activateEventHandler(element) {
        /**
         * This will activate event on each element.
         * It also checks if #onPageLoad property (By default, which is true)
         * is true or not. If not true then make it true
         * which is necessary to submit the form.
         */
        if ( element.type === 'select-one' || element.type === 'select-multiple' ) {
            this.#selectEvents.forEach( (e) => {
                element.addEventListener(e, () => {
                    if ( ! this.#onPageLoad ) {
                        this.#onPageLoad = true;
                    }
                    this.#commonExtraction(element);
                });
            });
        } else if ( element.type === 'file' ) {
            this.#fileEvents.forEach( (e) => {
                element.addEventListener(e, () => {
                    if ( ! this.#onPageLoad ) {
                        this.#onPageLoad = true;
                    }
                    this.#commonExtraction(element);
                });
            });
        } else {
            this.#generalEvents.forEach( (e) => {
                element.addEventListener(e, () => {
                    if ( ! this.#onPageLoad ) {
                        // Place where onPageLoad turns on automatically if off
                        this.#onPageLoad = true;
                    }
                    this.#commonExtraction(element);
                });
            });
        }
    }

    #commonExtraction(element) {
        /**
         * This method is common to each element and on top of that it extracts.
         * Extracts what ?
         *  1. It will get the validation attribute (By default, it is "data-validation")
         *     from the element, if exists otherwise the function will return false.
         *  2. The validation string by default, looks like this 'password|min:8|max:40'
         *  3. After extraction, it will look like this ['password', 'min:8', 'max:40']
         *  4. These array strings are then passed to mediator which may split
         *     extracted string if contained arguments and transfer it to caller.
         *  5. It will also call two other main methods : - #designShop and #tagField
         *
         *  Note: -
         *  1. The validation attribute contains validation method which are seperated by
         *     #validationSeparator. This can be changed during the instantiation of this class.
         *  2.
         */
        let validationStr = element.getAttribute(this.#validationAttributeName);
        if ( !validationStr ) return false;
        let elementValue;

        // re initialization containers for each element
        // so that each element get fresh storage containers
        // to store their belongings like return boolean values and messages
        this.#validationMethodsReturnValue = [];
        this.#messageBox = [];

        if ( element.type === 'select-multiple' ) {
            // this is for multiple select field
            elementValue = Array.from(element.selectedOptions).map(option => option.value)
        } else { // TODO check of specific field types only.
            // this is for rest of the fields
            elementValue = element.value;
        }

        // Validation attribute seperated to validation methods array
        // i.e. 'password|min:8|max:40' becomes ['password', 'min:8', 'max:40']
        let validationMethodsWithArgs = FormValidation.#splitString(validationStr, this.#validationSeparator);

        validationMethodsWithArgs.forEach((methodString) => {
            // the return value from deep down validation methods will get stored in #validationMethodsReturnValue
            // which will use later on for other purposes
            this.#validationMethodsReturnValue.push(this.#theMediator(methodString, element, elementValue));
        });

        console.log(this.#validationMethodsReturnValue);

        this.#theDesignShop(element);
        this.#tagField(element)
    }

    #theDesignShop(element) {
        /**
         * UI and UX handlers of this class.
         */
        this.#colorFormFields(element);
        this.#makeMessage(element);
        //TODO append SVG Elements in the form fields
    }

    #tagField(element) {
        /**
         * Set validation flag on each field element
         * for recognition of its validity
         */
        if (this.#validationMethodsReturnValue.includes(false)) {
            element.setAttribute(this.#flagName, false)
        } else  {
            element.setAttribute(this.#flagName, true)
        }
    }

    #theMediator(methodString, element, elementValue) {
        /**
         * Mediator will check whether the validation method string
         * contain method arguments or not
         * which are separated by #validationArgumentSeparator.
         * By default, its value is ":" which can be changed
         * during initialization of this class.
         *
         * Its main purpose is to form an object and
         * send it to #theCaller method.
         * The object contains all the necessary ingredients
         * to check the validation of the field value.
         */
        if ( typeof methodString === "string" && methodString.indexOf(':') !== -1 ) {
            let finalValidationMethod = FormValidation.#splitString(
                methodString, this.#validationArgumentSeparator
            );
            if ( !finalValidationMethod ) return false;
            return this.#theCaller({
                element: element,
                value: elementValue,
                methodName: finalValidationMethod[0],
                methodArgument: FormValidation.#popFirst(finalValidationMethod)
            })
        } else if ( typeof methodString === "string" ) {
            return this.#theCaller({
                element: element,
                value: elementValue,
                methodName: methodString,
            })
        }
    }

    #theCaller(obj) {
        /**
         * The caller is going to call the related method
         * based on the value stored in the object.
         * Otherwise, it will return "null".
         */
        switch (obj.methodName) {
            case 'username':
                return this.#username(obj);
            case 'required':
                return this.#required(obj);
            case 'email':
                return this.#email(obj);
            case 'within':
                return this.#within(obj);
            case 'max':
                return this.#max(obj);
            case 'min':
                return this.#min(obj);
            case 'checkDate':
                return this.#checkDate(obj);
            case 'checkTime':
                return this.#checkTime(obj);
            case 'exactLength':
                return this.#exactLength(obj);
            case 'alphaNum':
                return this.#alphaNum(obj);
            case 'decimal':
               return this.#decimal(obj);
            case 'digit':
               return this.#digit(obj);
            case 'alpha':
               return this.#alpha(obj);
            case'uuid':
               return this.#uuid(obj);
           case'regex':
               return this.#regex(obj);
           case'address':
               return this.#address(obj);
           case'phone':
               return this.#phone(obj);
           case'number':
               return this.#number(obj);
           case'file':
               return this.#file(obj);
            default:
                return null;
        }
    }

    #colorFormFields(element) {
        /**
         * Color form fields will apply colors
         * to the validation fields based on their validity.
         * The colors can be changed during the instantiation of the class.
         */
        if ( ! this.#showColorFormFields ) return;

        if ( this.#validationMethodsReturnValue.includes(false) ) {
            if (this.#disableInlineStyle) {
                element.classList.remove('error-not-present');
                element.classList.add('error-present');
            } else {
                element.style.backgroundColor = this.#errorColor;
            }
        } else {
            if (this.#disableInlineStyle) {
                element.classList.remove('error-present');
                element.classList.add('error-not-present');
            } else {
                element.style.backgroundColor = this.#successColor;
            }
        }
    }

    #makeMessage(element) {
        // TODO need more documentation
        /**
         * It will make the message which will be
         * displayed right next to the validation field.
         * The message will only be displayed when
         * validation field is invalid.
         */
        if ( ! this.#showMessages ) return;

        let userDefinedMsg = FormValidation.#splitString(
            element.getAttribute('data-message'),
            this.#validationMessageSeparator
        )

        let siblings = element.parentElement.getElementsByClassName('error-message');
        if ( siblings.length > 0 ) {
            for (let elm of siblings) {
                elm.remove();
            }
        }

        let box = '<div class="error-message">';

        if ( this.#listStyle === 'ordered') box += '<ol>';
        else if ( this.#listStyle === 'unordered') box += '<ul>';

        for (let i=0; i < this.#validationMethodsReturnValue.length; i++ ) {
            if ( this.#validationMethodsReturnValue[i] === false
                && Array.isArray(userDefinedMsg)
                && userDefinedMsg[i].trim().length > 0 ) {
                box += '<li>' + userDefinedMsg[i] + '</li>';
            } else if ( typeof this.#messageBox[i] !== 'undefined'
                && this.#showDefaultMessages === true
                && this.#messageBox[i].trim().length > 0 ) {
                box += '<li>' + this.#messageBox[i] + '</li>';
            }
        }
        box += '</ol></div>';
        element.insertAdjacentHTML('afterend', box);
    }

    #theSubmitter() {
        /**
         * Its job is to submit the form using addEventListener
         * but will first verify whether all the fields
         * which kept under validation are valid.
         *
         * @type {FormValidation}
         * @private
         */
        let _this = this;

        // let flag = _this.#checkFlag();
        _this.#form.addEventListener('submit', function (event) {
            _this.#onPageLoad = true;
            _this.#extractFields();
            if ( _this.#checkFlag() ) {
                return true;
            } else {
                if ( _this.#showErrorCounts ) {
                    _this.#showErrorCountMessage();
                }
            }
            event.preventDefault();
        });
    }

    #checkFlag() {
        /**
         * It fetches the #flagName attribute from each
         * validation field element and then returns
         * accordingly if it contains "false".
         *
         * Note: -
         *  Initially, it won't work if #onPageLoad property is false
         *  (By default, which is false).
         *  The #onPageLoad property's job is to not check the form or
         *  validate the form when page loads (if false). Then it will
         *  check only when an event is fired on each field or
         *  when we click the submit button which will change the onPageLoad
         *  option from false to true
         */
        let x = [];

        if (this.#onPageLoad === false)
            return false;

        this.#fields.forEach((element) => {
            x.push(element.getAttribute(this.#flagName))
        });

        this.#errorCount = x.filter(i => i === 'false').length;
        return !x.includes('false');
    }

    #showErrorCountMessage() {
        let submitButton = this.#form.querySelector('[type="submit"]');
        // TODO: -  make an option for user to switch between button or an input
        let box = '';
        let count = this.#errorCount;
        let oneOrMany = 0;

        if ( count > 0 ) {
            oneOrMany = (count > 1) ? "errors found." : "error found.";
            if ( this.#ownErrorCountId ) {
                box = document.getElementById( this.#ownErrorCountId );
                box.innerHTML = count + ' ' + oneOrMany;
            } else {
                let e = submitButton.parentNode.querySelector('#' + this.#defaultErrorCountId);
                if ( e ) e.remove();
                box = '<div id="' + this.#defaultErrorCountId + '">' + count + ' ' + oneOrMany + '</div>';
                submitButton.insertAdjacentHTML('beforebegin', box);
            }
        }
    }

    /*-------------------------------------------------------------------------------------------- Validation Methods */

    #username(obj) {
        let re =  this.#usernameRegex;

        if ( typeof obj.value === 'undefined' || typeof obj.value !== 'string' ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        if ( obj.value  === '' ) {
            this.#messageBox.push('');
            return true;
        }

        if ( !re.test(obj.value) ) {
            this.#messageBox.push(this.#defaultMessage.username);
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    #required(obj) {
        let x = this.#initialValueCheck(obj, false);
        if (x !== 3) return (x !== 1);

        if ( !obj.value || obj.value === '' || obj.value.length <= 0 ) {
            this.#messageBox.push(this.#defaultMessage.required);

            if ( obj.element.type === 'file' ) {
                // File image preview container empty
                if ( this.#imagePreviewContainer ) {
                    document.getElementById(this.#imagePreviewContainer).innerHTML = '';
                }
            }
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    #phone(obj) {
        let x = this.#initialValueCheck(obj, false);
        if (x !== 3) return (x !== 1);

        if ( obj.value.length > 0 ) {
            if (!this.#regexPhone.test(obj.value)) {
                this.#messageBox.push(this.#defaultMessage.phone);
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #address(obj) {
        let x = this.#initialValueCheck(obj, false);
        if (x !== 3) return (x !== 1);

        if ( obj.value.length > 0 ) {
            if (!this.#regexAddress.test(obj.value)) {
                this.#messageBox.push(this.#defaultMessage.address);
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #email(obj) {
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( obj.value.length > 0 ) {
            if (!this.#regexEmail.test(obj.value)) {
                this.#messageBox.push(this.#defaultMessage.email);
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #within(obj) {
        /*
         * within:admin,coordinator,editor
         */
        let list = [];
        let listLength = 0;
        let msgStr = '';
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( this.#initialArgumentCheck(obj) ) {
            if ( typeof obj.methodArgument[0] !== 'string' || obj.methodArgument[0].length <= 0 )  {
                this.#messageBox.push('Something went wrong.');
                return false;
            }
            list = FormValidation.#splitString(obj.methodArgument[0], this.#validatorWithinSeparator);
        }

        listLength = list.length;

        if ( listLength <= 0 ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        list.forEach(( value, index ) => {
            if ( listLength === 1) {
                msgStr += value;
            } else if (index === listLength - 1) {
                msgStr += ' and ' + value;
            } else if ( index === listLength - 2) {
                msgStr += value;
            } else {
                msgStr += value + ', ';
            }
        });

        if ( obj.value instanceof Array ) { // multiple select case
            obj.value.forEach(( value ) => {
                if ( !list.includes(value) ) {
                    this.#messageBox.push(
                        this.#defaultMessage.within + ' It should contain ' + msgStr + ' only.'
                    );
                    return false;
                }
            });
        } else if (typeof obj.value === 'string') { // regular select case
            if ( !list.includes(obj.value) ) {
                this.#messageBox.push(
                    this.#defaultMessage.within + ' It should contain ' + msgStr + ' only.'
                );
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #max(obj) {
        // max:20
        let limit = this.#getLimit(obj);
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( (typeof obj.value === 'string' && isNaN(obj.value)) && obj.value.length > limit ) {
            this.#messageBox.push(this.#defaultMessage.max + ' Limit is ' + limit + ' characters.');
            return false;
        } else if ( ! isNaN(obj.value) && (obj.value > limit) ) {
            this.#messageBox.push(this.#defaultMessage.max + ' Limit is ' + limit + '.');
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    #min(obj) {
        // min:10
        let limit = this.#getLimit(obj);
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( (typeof obj.value === 'string' && isNaN(obj.value)) && obj.value.length < limit ) {
            this.#messageBox.push(this.#defaultMessage.min  + ' Limit is ' + limit + ' characters.');
            return false;
        } else if ( ! isNaN(obj.value) && obj.value < limit ) {
            this.#messageBox.push(this.#defaultMessage.min + ' Limit is ' + limit + '.');
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    #exactLength(obj) {
        /*
         * exactLength:12:digit
         */
        let lengthValue = 0;
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( !this.#initialArgumentCheck(obj)) {
            this.#messageBox.push('Something went wrong.');
            return false;
        } else {
            if ( typeof obj.methodArgument[0] !== 'string' || isNaN(obj.methodArgument[0]) )  {
                this.#messageBox.push('Something went wrong.');
                return false;
            }
            lengthValue = parseInt(obj.methodArgument[0]);
        }

        // first  argument check
        if ( obj.value.length !== lengthValue ) {
            this.#messageBox.push(this.#defaultMessage.exact  + ' It must be of length ' + lengthValue + '.');
            return false;
        }

        // second argument check if exist
        if ( typeof obj.methodArgument[1] !== 'undefined' &&
            obj.methodArgument[1] === 'digit' &&
            !FormValidation.#verifyPattern(this.#digitRegx, obj.value)
        ) {
            this.#messageBox.push(this.#defaultMessage.exact  + ' Only, digit are allowed.');
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    #checkDate(obj) {
        let datePattern = 'yyyy-mm-dd';
        let matchingRegex = '';
        let separator = '-';
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( this.#initialArgumentCheck(obj)) {
            if ( typeof obj.methodArgument[0] !== 'string' )  {
                this.#messageBox.push('Something went wrong.');
                return false;
            }
            datePattern = obj.methodArgument[0];
        }

        if ( !this.#regexDate.hasOwnProperty(datePattern) || datePattern === 'undefined' ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        matchingRegex = this.#regexDate[datePattern];

        if ( !FormValidation.#verifyPattern(matchingRegex, obj.value) ) {
            this.#messageBox.push(this.#defaultMessage.checkDate);
            return false;
        } else {
            let a = '';

            if ( datePattern.includes('/') ) {
                separator = '/';
                a = FormValidation.#splitString(datePattern, '/'); // ['yyyy', 'mm', 'dd']
            } else if ( datePattern.includes('-') ) {
                separator = '-';
                a = FormValidation.#splitString(datePattern, '-'); // ['yyyy', 'mm', 'dd']
            }

            if ( !FormValidation.#validateDate(a, obj.value, separator) ) {
                this.#messageBox.push(this.#defaultMessage.checkDate);
                return false;
            } else {
                this.#messageBox.push();
                return true;
            }
        }
    }

    #checkTime(obj) {
        let hours = '24';
        let splitArray = [];
        let splitArrayLength = 0;
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( this.#initialArgumentCheck(obj)) {
            if ( typeof obj.methodArgument[0] === 'undefined' ||
                typeof obj.methodArgument[0] !== 'string' ||
                !this.#timeFormats.includes( obj.methodArgument[0] )
            ) {
                this.#messageBox.push( 'Something went wrong.' );
                return false;
            }
            hours =  obj.methodArgument[0];
        }

        if ( !FormValidation.#verifyPattern(this.#timePatterns.seconds, obj.value ) &&
            !FormValidation.#verifyPattern( this.#timePatterns.minutes, obj.value )
        ) {
             this.#messageBox.push(this.#defaultMessage.checkTime);
             return false;
        }

        splitArray = FormValidation.#splitString(obj.value, ':'); // ['12', '04', '11']
        splitArrayLength = splitArray.length;

        if ( hours === '12' ) {
            if ( splitArrayLength === 2 ) {
                if ( parseInt(splitArray[0]) > 12 || parseInt(splitArray[0]) < 1 ||
                    parseInt(splitArray[1]) > 59 || parseInt(splitArray[1]) < 0 ) {
                    this.#messageBox.push(this.#defaultMessage.checkTime);
                    return false;
                }
            } else if ( splitArrayLength === 3 ) {
                if ( parseInt(splitArray[0]) > 12 || parseInt(splitArray[0]) < 1 ||
                    parseInt(splitArray[1]) > 59 || parseInt(splitArray[1]) < 0 ||
                    parseInt(splitArray[2]) > 59 || parseInt(splitArray[2]) < 0
                ) {
                    this.#messageBox.push(this.#defaultMessage.checkTime);
                    return false;
                }
            }
        } else if ( hours === '24' ) {
            if ( splitArrayLength === 2 ) {
                if ( parseInt(splitArray[0]) > 24 || parseInt(splitArray[0]) < 0 ||
                    parseInt(splitArray[1]) > 59 || parseInt(splitArray[1]) < 0 )
                {
                    this.#messageBox.push(this.#defaultMessage.checkTime);
                    return false;
                }
            } else if ( splitArrayLength === 3 ) {
                if ( parseInt(splitArray[0]) > 24 || parseInt(splitArray[0]) < 0 ||
                    parseInt(splitArray[1]) > 59 || parseInt(splitArray[1]) < 0 ||
                    parseInt(splitArray[2]) > 59 || parseInt(splitArray[2]) < 0
                ) {
                    this.#messageBox.push(this.#defaultMessage.checkTime);
                    return false;
                }
            }
        }
        this.#messageBox.push('');
        return true;
    }

    #digit(obj) {
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( !FormValidation.#verifyPattern(this.#digitRegx, obj.value) ) {
            this.#messageBox.push(this.#defaultMessage.digit);
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    // TODO use FormValidation.#verifyPattern instead test everywhere in this library

    #number(obj) {
        if ( typeof obj.value === 'undefined' ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        if (obj.value.length > 0) {
            if ( isNaN(obj.value) ) {
                this.#messageBox.push(this.#defaultMessage.number);
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #decimal(obj) {
        if ( typeof obj.value === 'undefined' ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        if (obj.value.length > 0) {
            if (!FormValidation.#verifyPattern(this.#decimalRegex, obj.value)) {
                this.#messageBox.push(this.#defaultMessage.decimal);
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #alphaNum(obj) {
        /**
         * alphaNum:space:comma:hyphen:dot:brackets
         * @type {string}
         */
        let attachStr = '';
        let msgStr = '';
        let argLength = 0;
        let pattern = '';
        let finalPattern = {};
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        // if there are other arguments
        if ( this.#initialArgumentCheck(obj)) {
            argLength = obj.methodArgument.length;
            if (argLength > 0) {
                obj.methodArgument.forEach((element, index) => {
                    if ( this.#regxParams.hasOwnProperty(element) &&
                        typeof this.#regxParams[element] !== 'undefined' ) {
                        attachStr += this.#regxParams[element]
                    }
                    if ( argLength === 1) {
                        msgStr += element;
                    } else if (index === argLength - 1) {
                        msgStr += ' and ' + element;
                    } else if ( index === argLength - 2) {
                        msgStr += element;
                    } else {
                        msgStr += element + ', ';
                    }
                });
            }
        }

        pattern = '^[a-zA-Z0-9'+ attachStr +']+$';
        finalPattern = new RegExp(pattern);

        if (obj.value.length > 0) {
            // check if value is alphanumeric and add other options also if are there
            if (!FormValidation.#verifyPattern(finalPattern, obj.value)) {
                let finalMessage = this.#defaultMessage.alphaNum;

                if (msgStr.length > 0) {
                    finalMessage = this.#defaultMessage.alphaNum + ' with ' + msgStr;
                }

                finalMessage += ' characters.';

                this.#messageBox.push(finalMessage);
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #alpha(obj) {
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( obj.value.length > 0 ) {
            if (!this.#regexAlpha.test(obj.value)) {
                this.#messageBox.push(this.#defaultMessage.alpha);
                return false;
            }
        }

        this.#messageBox.push('');
        return true;
    }

    #uuid(obj) {
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if (obj.value.length <= 0) {
            this.#messageBox.push('Something went wrong.');
            return true;
        }

        if (!this.#uuidRegex.test(obj.value)) {
            this.#messageBox.push(this.#defaultMessage.uuid);
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    #regex(obj) {
        let x = this.#initialValueCheck(obj);
        if (x !== 3) return (x !== 1);

        if ( this.#initialArgumentCheck(obj) ) {
            if ( typeof obj.methodArgument[0] !== 'string' )  {
                this.#messageBox.push('Something went wrong.');
                return false;
            }
        }

        if (obj.value.length <= 0) {
            this.#messageBox.push('');
            return true;
        }

        // if (!.test(obj.value)) {
        //     this.#messageBox.push(this.#defaultMessage.uuid);
        //     return false;
        // }

        this.#messageBox.push('');
        return true;
    }

    #file(obj) {
        // file:jpg,jpeg:2:MB
        let x = this.#initialValueCheck(obj);
        let checkExt = this.#getExtension(obj);
        let size = this.#getSize(obj);
        let fileSize = 0;
        if (x !== 3) return (x !== 1);

        if ( !this.#initialElementCheck(obj) || !this.#initialArgumentCheck(obj) ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        fileSize = obj.element.files[0].size;

        // File Size check
        if ( fileSize > this.#intoBytes(size) ) {
            this.#messageBox.push(this.#defaultMessage.fileSize + ' ' + size[0] + ' ' + size[1] +'.');
            return false;
        }

        // File Extension check
        if ( !this.#checkExtension(checkExt, obj) ) {
            this.#messageBox.push(this.#defaultMessage.fileExtension + ' Only ' + obj.methodArgument[0] + ' file extensions are allowed.');
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    /*----------------------------------------------------------------------------------------------- initial Methods */

    #initialValueCheck(obj, escape=true) {
        if ( !obj.hasOwnProperty('value') || typeof obj.value === 'undefined' ) {
            this.#messageBox.push('Something went wrong.');
            return 1;
        }

        if ( escape ) {
            if (obj.value.length <= 0) {
                this.#messageBox.push('');
                return 2;
            }
        }
        return 3;
    }

    #initialElementCheck(obj) {
        return obj.hasOwnProperty('element') || obj.methodArgument instanceof Object;
    }

    #initialArgumentCheck(obj) {
        return obj.hasOwnProperty('methodArgument') || obj.methodArgument instanceof Array;
    }

    #getLimit(obj) {
        if ( !this.#initialArgumentCheck(obj)) {
            this.#messageBox.push('Something went wrong.');
            return false;
        } else {
            if ( typeof obj.methodArgument[0] !== 'string' || isNaN(obj.methodArgument[0]) )  {
                this.#messageBox.push('Something went wrong.');
                return false;
            }
            return parseInt(obj.methodArgument[0]);
        }
    }

    #getExtension(obj) {
        let extensions = [];
        if (typeof obj.methodArgument[0] !== 'string') {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        extensions = FormValidation.#splitString(obj.methodArgument[0], ',');

        extensions.forEach( (x) => {
            if ( !this.#validFileExtensions.includes(x) ) {
                this.#messageBox.push('Something went wrong.');
                return false;
            }
        })

        return extensions;
    }

    #getSize(obj) {
        if ( typeof obj.methodArgument[1] !== 'string' || isNaN(obj.methodArgument[1]) ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        } else if ( typeof obj.methodArgument[2] !== 'string' || !this.#fileSizes.includes(obj.methodArgument[2]) ) {
            this.#messageBox.push('Something went wrong.');
            return false;
        }

        return [obj.methodArgument[1], obj.methodArgument[2]];
    }

    #intoBytes(size) {
        let sizeValue = size[0];
        let sizeFigure = size[1];

        if ( isNaN(sizeValue) || !this.#fileSizes.includes(sizeFigure) ) {
            return false;
        }

        if ( sizeFigure === 'MB' ) {
            return sizeValue*1024*1024;
        } else if ( sizeFigure === 'KB' ) {
            return sizeValue*1024;
        } else if ( sizeFigure === 'GB' ) {
            return sizeValue*1024*1024*1024;
        }
    }

    #checkExtension(checkExt, obj) {
        let ext = obj.value.substring(obj.value.lastIndexOf('.') + 1).toLowerCase();
        let _this = this;

        checkExt.forEach( (x) => {
            if ( !this.#validFileExtensions.includes(x) ) {
                this.#messageBox.push('Something went wrong.');
                return false;
            }
        })

        // Match the extension with the validation extension
        if ( !checkExt.includes(ext) ) {
            return false;
        }

        // if file is an image and user wants to see the preview only then perform below task
        if ( _this.#imageExtensions.includes(ext) && _this.#imagePreviewShow ) {
            if ( obj.element.files && obj.element.files[0] ) {
                let reader = new FileReader();
                reader.onload = function( e ) {
                    let i = document.getElementById(_this.#imagePreviewContainer);
                    i.innerHTML = '<img src="'+ e.target.result +'" alt="No Preview Available.">';
                }
                reader.readAsDataURL( obj.element.files[0] );
            }
        }

        return true;
    }

    /*------------------------------------------------------------------------------------------------ Helper Methods */

    static #splitString(str, separator) {
        if ( typeof str === 'undefined' || typeof str !== 'string' || typeof separator !== 'string') return false
        return str.split(separator)
    }

    static #popFirst(arr) {
        if ( typeof arr === 'undefined' || !arr instanceof Array ) return false
        const [,...a] = arr;
        return a;
    }

    static #verifyPattern(pattern, value) {
        //  let p = new RegExp(pattern)
        // console.log(p + " => " + value)
        // console.log(p.test(value))
        return pattern.test(value);
    }

    static #validateDate(a, value, separator) {
        let d = FormValidation.#splitString(value, separator);
        let day = '';
        let month = '';
        let year = '';
        let monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

        if ( a[0] === 'yyyy' || a[0] === 'yy' ) {

            if ( a[1] === 'mm') {
                day = parseInt(d[2], 10);
                month = parseInt(d[1], 10);
            } else if ( a[2] === 'mm' ) {
                day = parseInt(d[1], 10);
                month = parseInt(d[2], 10);
            }

            year = parseInt(d[0], 10);

        } else if ( a[2] === 'yyyy' || a[2] === 'yy' ) {

            if ( a[1] === 'mm') {
                day = parseInt(d[0], 10);
                month = parseInt(d[1], 10);
            } else if ( a[0] === 'mm' ) {
                day = parseInt(d[1], 10);
                month = parseInt(d[0], 10);
            }

            year = parseInt(d[2], 10);
        }

        if ( year < 1850 || year > 3000 || month < 1 || month > 12 ) return false;

        // leap year
        if ( year % 400 === 0 || ( year % 100 !== 0 && year % 4 === 0 ) )
            monthLength[1] = 29;

        return day > 0 && day <= monthLength[month - 1];
    }
}


