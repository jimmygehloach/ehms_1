/*
 * Form Validation class
 *
 * @author Jimmy Gehloach
 * */
class FormValidation {
    // Form require to validate
    #formId;

    // Common events fire on field elements
    #generalEvents = ['keyup', 'keydown', 'click'];

    // event fire on select field elements
    #selectEvents = ['click', 'change'];

    // event fire on file field elements
    #fileEvents = ['keyup', 'keydown', 'click', 'focus', 'change'];

    #fireEventHandler = true;
    #elementTypes = ['select-one', 'select-multiple', 'file', 'checkbox', 'radio'];
    #elementTypeEvents = {
        'select-one': this.#selectEvents,
        'select-multiple': this.#selectEvents,
        file: this.#fileEvents,
        checkbox: this.#selectEvents,
        radio: this.#selectEvents,
        general: this.#generalEvents,
    };

    // it will determine which field is going to validate
    #validationAttributeName = 'data-validation';

    // it will determine which error message will be displayed
    #validationMessageAttributeName = 'data-message';

    // to figure out whether a field is valid or not
    #flagName = 'data-flag';

    // style used for highlighting
    #errorColor = 'rgba(255,0,0,0.15)';
    #successColor = 'rgba(0,255,0,0.15)';
    #disableInlineStyle = false;
    #successClassName = 'error-not-present';
    #errorClassName = 'error-present';

    // Load the class when the page is loaded or load it on some event
    #onPageLoad = false;

    // separators used in validation attribute and validation messages
    #validationSeparator = '|';
    #validationArgumentSeparator = ':';
    #validatorWithinSeparator = ',';
    #validationMessageSeparator = '|';

    // regex patterns
    #emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    #usernameRegex = {
        underscore: /^[a-zA-Z0-9_]+$/,
        dot: /^[a-zA-Z0-9_]+$/,
        dash: /^[a-zA-Z0-9_]+$/,
        rate: /^[a-zA-Z0-9@]+$/,
        email: this.#emailRegex,
        all: /^[a-zA-Z0-9_.-@]+$/,
        plain: /^[a-zA-Z0-9]+$/,
    };
    #decimalRegex = /^-?\d+\.\d+$/;
    #addressRegex = /^[\da-zA-Z@:;&_"'(),.\-\s]+$/;
    #phoneRegex = {
        uk: /^([0-9]{10,11})$/,
        in: /^([0-9]{10,11})$/,
    };
    #postcodeRegex = {
        uk: /^[\dA-Za-z]{2,4}\s[\dA-Za-z]{3}$/,
        in: /^\d{6}$/,
    };
    #alphaRegex = /^[a-zA-Z]+$/;
    #uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
    #positiveIntegerRegex = /^\d*\.?\d+$/;
    #dateRegex = {
        'yyyy-mm-dd': /^(\d{4}-\d{2}-\d{2})$/,
        'yy-mm-dd': /^(\d{2}-\d{2}-\d{2})$/,
        'dd-mm-yyyy': /^(\d{2}-\d{2}-\d{4})$/,
        'dd-mm-yy': /^(\d{2}-\d{2}-\d{2})$/,
        'yyyy/mm/dd': /^(\d{4}\/\d{2}\/\d{2})$/,
        'yy/mm/dd': /^(\d{2}\/\d{2}\/\d{2})$/,
        'dd/mm/yyyy': /^(\d{2}\/\d{2}\/\d{4})$/,
        'dd/mm/yy': /^(\d{4}\/\d{2}\/\d{2})$/,
    };
    #dateTimeRegex = {
        'yyyy-mm-dd His': /^(\d{4}-\d{2}-\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'yy-mm-dd His': /^(\d{2}-\d{2}-\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'dd-mm-yyyy His': /^(\d{2}-\d{2}-\d{4}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'dd-mm-yy His': /^(\d{2}-\d{2}-\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'yyyy/mm/dd His': /^(\d{4}\/\d{2}\/\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'yy/mm/dd His': /^(\d{2}\/\d{2}\/\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'dd/mm/yyyy His': /^(\d{2}\/\d{2}\/\d{4}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'dd/mm/yy His': /^(\d{4}\/\d{2}\/\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        'yyyy-mm-dd Hi': /^(\d{4}-\d{2}-\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'yy-mm-dd Hi': /^(\d{2}-\d{2}-\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'dd-mm-yyyy Hi': /^(\d{2}-\d{2}-\d{4}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'dd-mm-yy Hi': /^(\d{2}-\d{2}-\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'yyyy/mm/dd Hi': /^(\d{4}\/\d{2}\/\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'yy/mm/dd Hi': /^(\d{2}\/\d{2}\/\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'dd/mm/yyyy Hi': /^(\d{2}\/\d{2}\/\d{4}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'dd/mm/yy Hi': /^(\d{4}\/\d{2}\/\d{2}) ([01][0-9]|2[0-3]):([0-5][0-9])$/,
        'yyyy-mm-dd his': /^(\d{4}-\d{2}-\d{2}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'yy-mm-dd his': /^(\d{2}-\d{2}-\d{2}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'dd-mm-yyyy his': /^(\d{2}-\d{2}-\d{4}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'dd-mm-yy his': /^(\d{2}-\d{2}-\d{2}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'yyyy/mm/dd his': /^(\d{4}\/\d{2}\/\d{2}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'yy/mm/dd his': /^(\d{2}\/\d{2}\/\d{2}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'dd/mm/yyyy his': /^(\d{2}\/\d{2}\/\d{4}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'dd/mm/yy his': /^(\d{4}\/\d{2}\/\d{2}) (0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        'yyyy-mm-dd hi': /^(\d{4}-\d{2}-\d{2}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
        'yy-mm-dd hi': /^(\d{2}-\d{2}-\d{2}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
        'dd-mm-yyyy hi': /^(\d{2}-\d{2}-\d{4}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
        'dd-mm-yy hi': /^(\d{2}-\d{2}-\d{2}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
        'yyyy/mm/dd hi': /^(\d{4}\/\d{2}\/\d{2}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
        'yy/mm/dd hi': /^(\d{2}\/\d{2}\/\d{2}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
        'dd/mm/yyyy hi': /^(\d{2}\/\d{2}\/\d{4}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
        'dd/mm/yy hi': /^(\d{4}\/\d{2}\/\d{2}) (0[0-9]|1[0-2]):([0-5][0-9])$/,
    };
    #dateSeparators = ['/', '-'];
    #timeSeparator = ':';
    #time12Regex = {
        his: /^(0[0-9]|1[0-2]):([0-5][0-9]):([0-5][0-9])$/,
        hi: /^(0[0-9]|1[0-2]):([0-5][0-9])$/,
    };
    #time24Regex = {
        His: /^([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/,
        Hi: /^([01][0-9]|2[0-3]):([0-5][0-9])$/,
    };
    #timeFormats = {
        12: this.#time12Regex,
        24: this.#time24Regex,
    };

    #booleanEntries = [
        'YES',
        'NO',
        'Yes',
        'No',
        'yes',
        'no',
        true,
        false,
        'true',
        'false',
        'True',
        'False',
        'TRUE',
        'FALSE',
        0,
        1,
        '0',
        '1',
    ];

    #regexParams = {
        space: '\\s',
        comma: '\\,',
        hyphen: '\\-',
        dot: '\\.',
        brackets: '\\(\\)',
        underscore: '\\_',
    };

    // message properties
    #showMessages = true;
    #showDefaultMessages = true;
    #showColorFormFields = true;
    #listStyle = 'ordered'; // ordered || unordered || paragraph || ''
    #listStyleTags = ['ordered', 'unordered'];
    #messageOpeningWrappers = {
        ordered: '<ol>',
        unordered: '<ul>',
        paragraph: '<p>',
    };
    #messageClosingWrappers = {
        ordered: '</ol>',
        unordered: '</ul>',
        paragraph: '</p>',
    };
    #defaultMessage = {
        username: 'Username is invalid.',
        boolean: 'Invalid boolean value.',
        email: 'Email is invalid.',
        address: 'Invalid entry of address. Characters allowed are @:;&_"\'(),.-s',
        phone: 'The phone/telephone number is invalid.',
        postcode: 'The postcode is invalid.',
        required: 'This field is required.',
        within: 'This field is invalid.',
        max: 'Value exceeded the limit.',
        greater: 'Value is greater than the',
        smaller: 'Value is smaller than the',
        min: 'Value should be greater than the limit.',
        checkDate: 'Date is invalid.',
        checkTime: 'Time is invalid.',
        dateTime: 'Datetime is invalid.',
        exact: 'Value is invalid.',
        digit: 'Value must consist of digits only.',
        decimal: 'Invalid decimal number.',
        alphaNum: 'Value should only contain alpha numeric',
        alpha: 'Value should only contain alpha characters.',
        uuid: 'Invalid UUID. Data is altered.',
        fileSize: 'Check the required file size limit.',
        fileExtension: 'Chosen file is invalid.',
        reload: 'Something went wrong. Reload the page.',
        generic: 'Something went wrong. Check the syntax in the form.',
        number: 'The value is not a valid number.',
        invalid: 'The value is invalid.',
        text: 'One of the character typed by you is invalid. Please search and remove it.',
    };
    #messageBox = [];

    // file upload properties
    #fileSizes = ['GB', 'MB', 'KB'];
    #validFileExtensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'xlx', 'xlsx'];
    #imageExtensions = ['jpg', 'jpeg', 'png', 'gif'];
    #imagePreviewContainer = null;
    #imagePreviewShow = false;

    // error related properties
    #showErrorCounts = true;
    #ownErrorCountId = null;
    #realTimeErrorCheck = true;
    #ownErrorCountClass = null;
    #defaultErrorCountId = 'form-errors-count';
    #errorCount = 0;
    #errorMessageClassName = 'error-message-box';

    #textRegex = /^[a-zA-Z\d\s\,\.\@\"\(\)\'\"\-\£\%\&\!\?]+$/;

    #regexMethodPatterns = '';

    // save form in this property
    #form;

    // save fields from the form in this property
    #fields;

    // form fields identifier
    #fieldSelectors =
        '[data-type="radio"], ' +
        'input[' +
        this.#validationAttributeName +
        '], ' +
        'select[' +
        this.#validationAttributeName +
        '], ' +
        'textarea[' +
        this.#validationAttributeName +
        ']';

    #validationMethodsReturnValue = [];

    #validationMethods = {
        username: {
            method: ['username'],
            arguments: ['plain', 'underscore', 'dot', 'dash', 'rate', 'email', 'all'],
            modifications: ['usernameRegex'],
            examples: ['username:plain', 'username:dot', 'username:all'],
        },
        boolean: {
            method: ['boolean'],
            arguments: [],
            modifications: [this.#booleanEntries],
            examples: ['boolean'],
        },
        required: {
            method: ['required'],
            arguments: [],
            modifications: [],
            examples: ['required'],
        },
        phone: {
            method: ['phone'],
            arguments: ['uk', 'in'],
            modifications: ['phoneRegex'],
            examples: ['phone:uk', 'phone:in'],
        },
        address: {
            method: ['address'],
            arguments: [],
            modifications: ['addressRegex'],
            examples: ['address'],
        },
        email: {
            method: ['email'],
            arguments: [],
            modifications: ['emailRegex'],
            examples: ['email'],
        },
        within: {
            method: ['within'],
            arguments: ['...range...'],
            modifications: [],
            recommendedUseWith: ['select', 'radio'],
            examples: ['within:1,2,3,4,5,6', 'within:yes,no', 'within:true,false', 'within:male,female,others'],
        },
        max: {
            method: ['max'],
            arguments: ['...digits...'],
            modifications: [],
            examples: ['max:20'],
        },
        min: {
            method: ['min'],
            arguments: ['...digits...'],
            modifications: [],
            examples: ['min:4'],
        },
        exactLength: {
            method: ['exactLength'],
            arguments: ['...digits...'],
            modifications: [],
            examples: ['exactLength:10'],
        },
        checkDate: {
            method: ['checkDate'],
            arguments: ['...datePattern...'],
            modifications: ['dateRegex', 'dateSeparators'],
            examples: ['checkDate:yyyy-mm-dd', 'checkDate:yyyy/mm/dd'],
        },
        checkTime: {
            method: ['checkTime'],
            arguments: ['...timeFormats...'],
            modifications: ['timeSeparator', 'time12Regex', 'time24Regex'],
            examples: ['checkTime:12:hi:his', 'checkTime:24:His:Hi'],
        },
        dateTime: {
            method: ['dateTime'],
            arguments: ['...dateTimePattern...'],
            modifications: ['dateTimeRegex', 'dateSeparators'],
            examples: ['dateTime:yyyy-mm-dd His', 'dateTime:yyyy-mm-dd Hi'],
        },
        digit: {
            method: ['digit'],
            arguments: [],
            modifications: ['positiveIntegerRegex'],
            examples: ['digit'],
        },
        number: {
            method: ['number'],
            arguments: [],
            modifications: [],
            examples: ['number'],
        },
        decimal: {
            method: ['decimal'],
            arguments: [],
            modifications: ['decimalRegex'],
            examples: ['decimal'],
        },
        checkBox: {
            method: ['checkBox'],
            arguments: [],
            modifications: [],
            examples: ['checkBox'],
        },
        alphaNum: {
            method: ['alphaNum'],
            arguments: ['space', 'comma', 'hyphen', 'dot', 'brackets', 'underscore'],
            modifications: ['regexParams'],
            examples: ['alphaNum:space:hyphen:dot', 'alphaNum:dot:hyphen'],
        },
        alpha: {
            method: ['alpha'],
            arguments: [],
            modifications: ['alphaRegex'],
            examples: ['alpha'],
        },
        uuid: {
            method: ['uuid'],
            arguments: [],
            modifications: ['uuidRegex'],
            examples: ['uuid'],
        },
        regex: {
            method: ['regex'],
            arguments: ['...pattern...'],
            modifications: ['regexMethodPatterns'],
            examples: ['regex'],
        },
        file: {
            method: ['file'],
            arguments: ['...extensions...', '...size...', '...sizeType...', '...previewId...'],
            modifications: ['filSizes', 'validFileExtensions', 'imagePreviewShow'],
            examples: ['file:jpg,jpeg:2:MB', 'file:pdf,docx,doc:500:KB', 'file:pdf,docx,doc:500:KB:imagePreviewId'],
        },
        postcode: {
            method: ['postcode'],
            arguments: ['uk', 'in'],
            modifications: ['postcodeRegex'],
            examples: ['postcode:uk', 'postcode:in'],
        },
        text: {
            method: ['text'],
            arguments: [],
            modifications: ['textRegex'],
            examples: ['text'],
        },
        fcUpper: {
            method: ['fcUpper'],
            arguments: ['all'],
            modifications: [],
            examples: ['fcUpper', 'fcUpper:all'],
        },
        upper: {
            method: ['upper'],
            arguments: ['all'],
            modifications: [],
            examples: ['upper'],
        },
    };

    #debug = true;
    #printConsole = {};
    #submitButton;
    #submitButtonType = 'input';
    #submitResponse = false;

    /**
     *
     * @param obj
     */
    constructor(obj) {
        // formID parameter : mandatory
        this.#formId = obj.formId ??= null;

        // formId check
        if (
            this.#formId === '' ||
            this.#formId === null ||
            this.#formId === false ||
            typeof this.#formId === 'undefined'
        ) {
            throw new Error('Form id is required.');
        }

        // default parameters : optionals
        this.#generalEvents = obj.generalEvents ??= this.#generalEvents;
        this.#selectEvents = obj.selectEvents ??= this.#selectEvents;
        this.#fileEvents = obj.fileEvents ??= this.#fileEvents;
        this.#validationAttributeName = obj.validationAttributeName ??= this.#validationAttributeName;
        this.#validationMessageAttributeName = obj.validationMessageAttributeName ??=
            this.#validationMessageAttributeName;
        this.#flagName = obj.flagName ??= this.#flagName;
        this.#errorColor = obj.errorColor ??= this.#errorColor;
        this.#successColor = obj.successColor ??= this.#successColor;
        this.#disableInlineStyle = obj.disableInlineStyle ??= this.#disableInlineStyle;
        this.#successClassName = obj.successClassName ??= this.#successClassName;
        this.#errorClassName = obj.errorClassName ??= this.#errorClassName;
        this.#onPageLoad = obj.onPageLoad ??= this.#onPageLoad;
        this.#validationSeparator = obj.validationSeparator ??= this.#validationSeparator;
        this.#validationArgumentSeparator = obj.validationArgumentSeparator ??= this.#validationArgumentSeparator;
        this.#validatorWithinSeparator = obj.validatorWithinSeparator ??= this.#validatorWithinSeparator;
        this.#validationMessageSeparator = obj.validationMessageSeparator ??= this.#validationMessageSeparator;
        this.#emailRegex = obj.emailRegex ??= this.#emailRegex;
        this.#usernameRegex = obj.usernameRegex ??= this.#usernameRegex;
        this.#decimalRegex = obj.decimalRegex ??= this.#decimalRegex;
        this.#addressRegex = obj.addressRegex ??= this.#addressRegex;
        this.#phoneRegex = obj.phoneRegex ??= this.#phoneRegex;
        this.#booleanEntries = obj.booleanEntries ??= this.#booleanEntries;

        // Date exposed properties
        this.#dateRegex = obj.dateRegex ??= this.#dateRegex;
        this.#dateSeparators = obj.dateSeparaters ??= this.#dateSeparators;
        this.#timeSeparator = obj.timeSeparator ??= this.#timeSeparator;
        this.#time12Regex = obj.time12Regex ??= this.#time12Regex;
        this.#time24Regex = obj.time24Regex ??= this.#time24Regex;
        this.#dateTimeRegex = obj.dateTimeRegex ??= this.#dateTimeRegex;

        this.#alphaRegex = obj.alphaRegex ??= this.#alphaRegex;
        this.#uuidRegex = obj.uuidRegex ??= this.#uuidRegex;
        this.#positiveIntegerRegex = obj.positiveIntegerRegex ??= this.#positiveIntegerRegex;
        this.#showMessages = obj.showMessages ??= this.#showMessages;
        this.#showDefaultMessages = obj.showMessages ??= this.#showDefaultMessages;
        this.#showColorFormFields = obj.showMessages ??= this.#showColorFormFields;
        this.#listStyle = obj.listStyle ??= this.#listStyle;
        this.#validFileExtensions = obj.validFileExtensions ??= this.#validFileExtensions;
        this.#imagePreviewShow = obj.imagePreviewShow ??= this.#imagePreviewShow;
        this.#showErrorCounts = obj.showErrorCounts ??= this.#showErrorCounts;
        this.#ownErrorCountId = obj.ownErrorCountId ??= this.#ownErrorCountId;
        this.#ownErrorCountClass = obj.ownErrorCountClass ??= this.#ownErrorCountClass;
        this.#defaultErrorCountId = obj.defaultErrorCountId ??= this.#defaultErrorCountId;
        this.#errorCount = obj.errorCount ??= this.#errorCount;
        this.#errorMessageClassName = obj.errorMessageClassName ??= this.#errorMessageClassName;
        this.#fieldSelectors = obj.fieldSelectors ??= this.#fieldSelectors;
        this.#regexParams = obj.regexParams ??= this.#regexParams;
        this.#fileSizes = obj.fileSizes ??= this.#fileSizes;
        this.#debug = obj.debug ??= this.#debug;
        this.#realTimeErrorCheck = obj.realTimeErrorCheck ??= this.#realTimeErrorCheck;
        this.#submitButtonType = obj.submitButtonType ??= this.#submitButtonType;
        this.#textRegex = obj.textRegex ??= this.#textRegex;
        this.#regexMethodPatterns = obj.regexMethodPatterns ??= this.#regexMethodPatterns;

        // setting up form
        this.#form = document.getElementById(this.#formId);
        this.#setSubmitButton();

        // method calls
        this.#extractFields();
        this.#theSubmitter();
    }

    #setSubmitButton() {
        if (this.#submitButtonType === 'input') {
            this.#submitButton = this.#form.querySelector('[type="submit"]');
        } else if (this.#submitButtonType === 'data-type') {
            this.#submitButton = this.#form.querySelector('[data-type="submit"]');
        } else if (this.#submitButtonType === 'data-outside') {
            const id = this.#form.getAttribute('data-outside');
            this.#submitButton = document.getElementById(id);
        } else {
            this.#submitButton = this.#form.querySelector('[type="submit"]');
        }
    }

    /**
     * Scan all the fields in the form and form a nodeset which will get
     * stored into the #fields property.
     *
     * The next step after this will be the extraction of validation
     * attribute from each element with validation data attribute.
     */
    #extractFields() {
        this.#fields = this.#form.querySelectorAll(this.#fieldSelectors);

        this.#extractValidationAttribute();
    }

    /**
     * Its primary job is to extract validation data from the extracted
     * fields stored in #fields property.
     * BUT ...
     * If #fireEventHandler switch is on (By default, it is on.)
     * then it will send each field element to #activateEventHandler method
     * to activate event on each element behaviour. The behaviour
     * will be determined by the events applied.
     */
    #extractValidationAttribute() {
        this.#fields.forEach((element, i) => {
            if (this.#fireEventHandler) {
                this.#activateEventHandler(element);
            }

            // if you want to do the verification on page load otherwise on
            // submit
            if (this.#onPageLoad) {
                this.#commonExtraction(element);
            }
        });
    }

    /**
     * This will activate event on each element. It also checks if #onPageLoad
     * property (By default, which is true) is true or not. If not true then
     * make it true which is necessary to submit the form.
     *
     * @param element Field element on which event is going to activate
     */
    #activateEventHandler(element) {
        let type = element.type;

        if (!this.#elementTypes.includes(type)) {
            type = 'general';
        }

        this.#addElementEventListener(element, this.#elementTypeEvents[type]);
    }

    /**
     * Loop the events to specific "form field element" type using
     * addEventListener function
     *
     * @param element Field element
     * @param elementTypeEvents Events going to apply on Field element
     */
    #addElementEventListener(element, elementTypeEvents) {
        elementTypeEvents.forEach((e) => {
            // Attach the event listener to the element
            element.addEventListener(e, () => {
                this.#commonExtraction(element);
            });
        });
    }

    /**
     * This method is common to each element and on top of that it extracts.
     *
     * Extracts what?
     *  1. It will get the validation attribute (By default, it is
     *     "data-validation") from the element, if exists otherwise the function
     *     will return false.
     *
     *  2. The validation string by default, looks like this
     *     'password|min:8|max:40'. After extraction, it will look like this
     *     ['password', 'min:8', 'max:40']
     *
     *  3. These array strings are then passed to mediator which will split
     *     extracted string, if contained arguments and transfer it to caller.
     *
     *  4. It will also call two other main methods : - #designShop and
     *     #tagField
     *     // TODO explain design shop and tag field little bit here
     *
     *  Note: -
     *  1. The validation attribute contains validation method which are
     *     seperated by #validationSeparator. This can be changed during the
     *     instantiation of this class.
     *
     * @param element Field element
     */
    #commonExtraction(element) {
        // 'password|min:8|max:40'
        let validationStr = element.getAttribute(this.#validationAttributeName);
        if (!validationStr) return false;
        let elementValue;

        // re initialization containers for each element
        // so that each element get fresh storage containers
        // to store their belongings like return boolean values and messages
        this.#validationMethodsReturnValue = [];
        this.#messageBox = [];

        if (element.type === 'select-multiple') {
            // this is for multiple select field
            elementValue = Array.from(element.selectedOptions).map((option) => option.value);
        } else if (element.getAttribute('data-type') === 'radio') {
            const name = element.children[0].getAttribute('name');
            const radios = document.getElementsByName(name);
            let checked = [];

            radios.forEach((e) => {
                checked.push(e.checked);
                if (e.checked) {
                    elementValue = e.value;
                }
            });

            if (!checked.includes(true)) {
                elementValue = '';
            }
        } else {
            // TODO check of specific field types only.
            // this is for rest of the fields
            elementValue = element.value;
        }

        // Validation attribute seperated to validation methods array
        // i.e. 'password|min:8|max:40' becomes ['password', 'min:8', 'max:40']
        let validationMethodsWithArgs = FormValidation.#splitString(validationStr, this.#validationSeparator);

        // loop every element in the validationMethodsWithArgs array
        validationMethodsWithArgs.forEach((methodString) => {
            // the return value from deep down validation methods will get
            // stored in #validationMethodsReturnValue which will use later on
            // for other purposes
            this.#validationMethodsReturnValue.push(this.#theMediator(methodString, element, elementValue));
        });

        this.#theDesignShop(element);
        this.#tagField(element);
        this.#realTimeErrors();
    }

    /**
     * Mediator will check whether the validation method string contain method
     * arguments or not which are separated by #validationArgumentSeparator.
     * By default, its value is ":" which can be changed during initialization
     * of this class.
     *
     * Its main purpose is to form an object and send it to #theCaller method.
     * The object contains all the necessary ingredients to check the validation
     * of the field value.
     *
     * @param methodString 'password' | 'min:8' | 'max:40' ...
     * @param element Form element
     * @param elementValue Form element value
     * @returns {boolean|boolean}
     */
    #theMediator(methodString, element, elementValue) {
        let validationResponse;

        if (typeof methodString === 'string' && methodString.indexOf(this.#validationArgumentSeparator) !== -1) {
            let finalValidationMethod = FormValidation.#splitString(methodString, this.#validationArgumentSeparator);

            if (!finalValidationMethod) return false;

            validationResponse = this.#theCaller({
                element: element,
                value: elementValue,
                methodName: finalValidationMethod[0],
                methodArgument: FormValidation.#popFirst(finalValidationMethod),
            });
        } else if (typeof methodString === 'string') {
            validationResponse = this.#theCaller({
                element: element,
                value: elementValue,
                methodName: methodString,
            });
        }

        return validationResponse;
    }

    /**
     * The caller is going to call the validation method as per the methodName
     * in the object. Otherwise, it will return "null".
     *
     * @param obj object contain element, its value, validation method, its args
     * @returns {null|boolean}
     */
    #theCaller(obj) {
        if (!this.#initialObjectCheck(obj)) {
            return false;
        }

        switch (obj.methodName) {
            case 'username':
                return this.#entryPoint(this.#username, obj, ['string']);
            case 'boolean':
                return this.#entryPoint(this.#boolean, obj, ['string']);
            case 'required':
                return this.#entryPoint(this.#required, obj, [], false);
            case 'email':
                return this.#entryPoint(this.#email, obj, ['string']);
            case 'within':
                return this.#entryPoint(this.#within, obj, ['string', 'object']);
            case 'max':
                return this.#entryPoint(this.#max, obj, ['string']);
            case 'min':
                return this.#entryPoint(this.#min, obj, ['string']);
            case 'checkDate':
                return this.#entryPoint(this.#checkDate, obj, ['string']);
            case 'checkTime':
                return this.#entryPoint(this.#checkTime, obj, ['string']);
            case 'dateTime':
                return this.#entryPoint(this.#dateTime, obj, ['string']);
            case 'exactLength':
                return this.#entryPoint(this.#exactLength, obj, ['string']);
            case 'checkBox':
                return this.#entryPoint(this.#checkBox, obj, ['string']);
            case 'alphaNum':
                return this.#entryPoint(this.#alphaNum, obj, ['string']);
            case 'decimal':
                return this.#entryPoint(this.#decimal, obj, ['string']);
            case 'digit':
                return this.#entryPoint(this.#digit, obj, ['string']);
            case 'alpha':
                return this.#entryPoint(this.#alpha, obj, ['string']);
            case 'uuid':
                return this.#entryPoint(this.#uuid, obj, ['string']);
            case 'regex':
                return this.#entryPoint(this.#regex, obj, ['string']);
            case 'address':
                return this.#entryPoint(this.#address, obj, ['string']);
            case 'phone':
                return this.#entryPoint(this.#phone, obj, ['string']);
            case 'number':
                return this.#entryPoint(this.#number, obj, ['string']);
            case 'file':
                return this.#entryPoint(this.#file, obj, ['string']);
            case 'postcode':
                return this.#entryPoint(this.#postcode, obj, ['string']);
            case 'text':
                return this.#entryPoint(this.#text, obj, ['string']);
            case 'fcUpper':
                return this.#entryPoint(this.#fcUpper, obj, ['string']);
            case 'upper':
                return this.#entryPoint(this.#upper, obj, ['string']);
            default:
                return null;
        }
    }

    /**
     *  Design the "form field elements" and attached the message related to it.
     *
     * @param element Field element
     */
    #theDesignShop(element) {
        if (this.#showColorFormFields) this.#colorFormFields(element);
        if (this.#showMessages) this.#createMessage(element);
        //TODO append SVG Elements in the form fields
    }

    /**
     * Color form fields will apply colors to the validated form field elements
     * based on their #flagName value. The colors used here can be changed
     * during the instantiation of the class.
     *
     * @param element
     */
    #colorFormFields(element) {
        !this.#validationMethodsReturnValue.includes(false)
            ? this.#elementGotSuccessStyle(element)
            : this.#elementGotErrorStyle(element);
    }

    /**
     * Add class or add inline style on successful validation of the element
     *
     * @param element Form element
     */
    #elementGotSuccessStyle(element) {
        if (this.#disableInlineStyle) {
            element.classList.remove(this.#errorClassName);
            element.classList.add(this.#successClassName);
        } else {
            element.style.backgroundColor = this.#successColor;
        }
    }

    /**
     * Add class or add inline style on unsuccessful validation of the element
     *
     * @param element Form element
     */
    #elementGotErrorStyle(element) {
        if (this.#disableInlineStyle) {
            element.classList.remove(this.#successClassName);
            element.classList.add(this.#errorClassName);
        } else {
            element.style.backgroundColor = this.#errorColor;
        }
    }

    /**
     * It will create the message which will be displayed right next to the
     * validation "form field element".
     *
     * Note: -
     * The message will only be displayed when validation field is invalid.
     *
     * @param element
     */
    #createMessage(element) {
        // message string from the element = 'Message1||Message3'
        // after split this message string = ['Message1', '', 'Message3']
        let userDefinedMsg = FormValidation.#splitString(
            element.getAttribute(this.#validationMessageAttributeName),
            this.#validationMessageSeparator
        );

        // Elements next sibling is going to be message box
        let sibling = element.nextElementSibling;

        // if it is already exist then remove this element
        if (sibling && sibling.getAttribute('class') === this.#errorMessageClassName) {
            sibling.remove();
        }

        // otherwise insert the new message string next to the element
        element.insertAdjacentHTML('afterend', this.#createMessageBox(userDefinedMsg));
    }

    /**
     * Create Message Box that write the HTML content of error message
     *
     * @param userDefinedMsg Array of Message Strings
     * @returns {string} HTML code of error message box with error inside it
     */
    #createMessageBox(userDefinedMsg) {
        let box = `<div class="${this.#errorMessageClassName}">`;

        box += this.#openingList();

        // validationMethodsReturnValue = [false, false, false]
        // length = 3
        for (let i = 0; i < this.#validationMethodsReturnValue.length; i++) {
            /*
                if ith element of validationMethodsReturnValue is false
                check userDefinedMsg ith element and if it is there then proceed
                with that otherwise go for default messages.

                eg: - validationMethodsReturnValue = [false, false, false]
                userDefinedMsg = ['Message1', '', 'Message3']
                it will be an ith element match.

                Here as the third element is empty string in userDefinedMsg it
                will switch to default message.
             */
            if (
                this.#validationMethodsReturnValue[i] === false &&
                Array.isArray(userDefinedMsg) &&
                typeof userDefinedMsg[i] !== 'undefined' &&
                userDefinedMsg[i].trim().length > 0
            ) {
                box += this.#listStyleTags.includes(this.#listStyle)
                    ? `<li> ${userDefinedMsg[i]}</li>`
                    : `${userDefinedMsg[i]}`;
            } else if (
            /*
                messageBox is a container which contains the default messages
                during the validation of the element if there is an error
                otherwise it will contain empty strings.

                ith element of validationMethodsReturnValue is going to match
                with the messageBox ith element as it is happening in a sequence.

                eg: - validationMethodsReturnValue = [false, false, false]
                messageBox = [
                    'Default message1', 'Default message2', 'Default message3'
                ]

                Note: -
                1. To display default messages #showDefaultMessages flag needs
                to be true.
             */
                typeof this.#messageBox[i] !== 'undefined' &&
                this.#showDefaultMessages === true &&
                this.#messageBox[i].trim().length > 0
            ) {
                box += this.#listStyleTags.includes(this.#listStyle)
                    ? `<li> ${this.#messageBox[i]}</li>`
                    : `<li> ${this.#messageBox[i]}</li>`;
            }
        }

        // closing list
        box += this.#closingList();

        return box;
    }

    /**
     * Opening list is the opening tag of the error list if allowed
     *
     * @returns {*|string}
     */
    #openingList() {
        return this.#messageOpeningWrappers.hasOwnProperty(this.#listStyle)
            ? this.#messageOpeningWrappers[this.#listStyle]
            : '';
    }

    /**
     * Closing list is the closing tag of the error list if allowed
     *
     * @returns {*|string}
     */
    #closingList() {
        return this.#messageClosingWrappers.hasOwnProperty(this.#listStyle)
            ? this.#messageClosingWrappers[this.#listStyle]
            : '';
    }

    /**
     * Set validation flag on "form field element" according to their return
     * values.
     *
     * @param element Field element
     */
    #tagField(element) {
        let attribute = !this.#validationMethodsReturnValue.includes(false);
        element.setAttribute(this.#flagName, attribute);
    }

    /**
     * Its job is to submit the form using addEventListener
     * but will first verify whether all the fields
     * which kept under validation are valid.
     */
    #theSubmitter() {
        if (this.#submitButtonType === 'input') {
            this.#form.addEventListener('submit', (event) => {
                this.#onPageLoad = true;
                this.#extractValidationAttribute();
                if (this.#checkFlag()) {
                    return true;
                } else {
                    if (this.#showErrorCounts) {
                        this.#showErrorCountMessage();
                    }
                }
                event.preventDefault();
            });
        } else if (this.#submitButtonType === 'data-type') {
            this.#submitButton.addEventListener('click', (event) => {
                this.#onPageLoad = true;
                this.#extractValidationAttribute();
                if (this.#checkFlag()) {
                    this.#submitResponse = true;
                } else {
                    if (this.#showErrorCounts) {
                        this.#showErrorCountMessage();
                    }
                }
                event.preventDefault();
            });
        } else if (this.#submitButtonType === 'data-outside') {
            this.#submitButton.addEventListener('click', (event) => {
                this.#onPageLoad = true;
                this.#extractValidationAttribute();
                if (this.#checkFlag()) {
                    this.#form.submit();
                } else {
                    if (this.#showErrorCounts) {
                        this.#showErrorCountMessage();
                    }
                }
                event.preventDefault();
            });
        }
    }

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
    #checkFlag() {
        let allValidationFieldFlags = [];

        // get the value of flag from field = element and store inside
        // allValidationFieldFlags
        this.#fields.forEach((element) => {
            allValidationFieldFlags.push(element.getAttribute(this.#flagName));
        });

        // Based on the false value figure out error count
        this.#errorCount = allValidationFieldFlags.filter((i) => i === 'false').length;

        return !allValidationFieldFlags.includes('false');
    }

    /**
     * Display error count message when you submit the form
     */
    #showErrorCountMessage() {
        let box = '';
        let oneOrMany;

        if (this.#errorCount > 0) {
            oneOrMany = this.#errorCount > 1 ? 'errors found.' : 'error found.';

            if (this.#ownErrorCountId) {
                box = document.getElementById(this.#ownErrorCountId);
                box.innerHTML = this.#errorCount + ' ' + oneOrMany;
            } else if (this.#ownErrorCountClass) {
                box = document.getElementsByClassName(this.#ownErrorCountClass);

                Array.from(box).forEach((e) => {
                    e.innerHTML = this.#errorCount + ' ' + oneOrMany;
                });
                // box.innerHTML = this.#errorCount + ' ' + oneOrMany;
            } else {
                this.#removeErrorCountContainer(this.#defaultErrorCountId);
                box = '<div id="' + this.#defaultErrorCountId + '">' + this.#errorCount + ' ' + oneOrMany + '</div>';
                this.#submitButton.insertAdjacentHTML('beforebegin', box);
            }
        } else {
            if (this.#ownErrorCountId) {
                document.getElementById(this.#ownErrorCountId).innerHTML = '';
            } else if (this.#ownErrorCountClass) {
                box = document.getElementsByClassName(this.#ownErrorCountClass);
                Array.from(box).forEach((e) => {
                    e.innerHTML = '';
                });
            } else {
                this.#removeErrorCountContainer(this.#defaultErrorCountId);
            }
        }
    }

    /**
     * Helper method of showErrorCountMessage
     * It will remove the existing error count container
     *
     * @param id
     */
    #removeErrorCountContainer(id) {
        // Todo see if you can search for the selector through formId
        let e = this.#submitButton.parentNode.querySelector('#' + id);
        if (e) e.remove();
    }

    #realTimeErrors() {
        if (this.#realTimeErrorCheck) {
            this.#checkFlag();
            if (this.#showErrorCounts) {
                this.#showErrorCountMessage();
            }
        }
    }

    /*----------------------------------------------------------------------------------------------- Initial Methods */

    /**
     * Initial check on object
     *
     * @param obj
     * @returns {boolean}
     */
    #initialObjectCheck(obj) {
        return ![
            this.#initialElementCheck(obj),
            this.#initialValueCheck(obj),
            this.#initialMethodCheck(obj),
            this.#initialArgumentCheck(obj),
        ].includes(false);
    }

    /**
     * Element property check of obj
     *
     * @param obj
     * @returns {boolean}
     */
    #initialElementCheck(obj) {
        if (!obj.hasOwnProperty('element') || !obj.element instanceof Object) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }
        return true;
    }

    /**
     * Initial value check of obj
     *
     * @param obj
     * @returns {boolean}
     */
    #initialValueCheck(obj) {
        // check the value of the element
        // TODO: check in depth the value if it is an array or string see what
        // TODO: kind of values we get from the html side

        if (!obj.hasOwnProperty('value') || typeof obj.value === 'undefined') {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }
        return true;
    }

    /**
     * Initial methodName check of obj
     *
     * @param obj
     * @returns {boolean}
     */
    #initialMethodCheck(obj) {
        if (!obj.hasOwnProperty('methodName') || !this.#validationMethods.hasOwnProperty(obj.methodName)) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }
        return true;
    }

    /**
     * Initial Method Argument check of obj
     *
     * @param obj
     * @returns {boolean}
     */
    #initialArgumentCheck(obj) {
        if (obj.hasOwnProperty('methodArgument') && !obj.methodArgument instanceof Array) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }
        return true;
    }

    /**
     * Entry point for validation methods
     *
     * @param funcCall Validation method to call
     * @param obj object which is passed through validation method
     * @param type type of value; element of obj passed
     * @param flag by default = true; it says the validation method is going to
     * call after some check; if false straight way validation method call
     * @returns {boolean}
     */
    #entryPoint(funcCall, obj, type, flag = true) {
        if (flag === true && (obj.value.length <= 0 || !type.includes(typeof obj.value))) {
            this.#messageBox.push('');
            return true;
        } else {
            if (funcCall.call(this, obj)) {
                this.#messageBox.push('');
                return true;
            }
            return false;
        }
    }

    /*-------------------------------------------------------------------------------------------- Validation Methods */

    /**
     * Validate username field in the form
     * Options available: => username:plain|underscore|dot|dash|rate|email|all
     * Modifications: => this.#usernameRegex = obj.usernameRegex
     *
     * @param obj
     * @returns {boolean}
     */
    #username(obj) {
        if (!this.#usernameRegex.hasOwnProperty(obj.methodArgument[0])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        } else if (!FormValidation.#verifyPattern(this.#usernameRegex[obj.methodArgument[0]], obj.value)) {
            this.#messageBox.push(this.#defaultMessage.username);
            return false;
        }

        return true;
    }

    /**
     * Validate boolean field in the form
     * Options available: => boolean
     * Modifications: => None
     *
     * @param obj
     * @returns {boolean}
     */
    #boolean(obj) {
        if (!this.#booleanEntries.includes(obj.value)) {
            this.#messageBox.push(this.#defaultMessage.boolean);
            return false;
        }

        return true;
    }

    /**
     * Validate the mandatory fields
     * Options available: = > required
     * Modifications: = > None
     *
     * @param obj
     * @returns {boolean}
     */
    #required(obj) {
        if (obj.element.type === 'radio') {
            const name = obj.element.getAttribute('name');
            const radios = document.getElementsByName(name);
            let checked = [];

            radios.forEach((e) => {
                checked.push(e.checked);
            });

            if (radios.length === checked.length && checked.includes(true)) {
                return true;
            } else {
                this.#messageBox.push(this.#defaultMessage.required);
                return false;
            }
        } else if (obj.element.type === 'checkbox' && !obj.element.checked) {
            this.#messageBox.push(this.#defaultMessage.required);
            return false;
        } else if (obj.value.length > 0) {
            return true;
        } else {
            this.#messageBox.push(this.#defaultMessage.required);
            return false;
        }
    }

    /**
     * Validate phone number field in the form
     * Options available: => phone:uk,in
     * Modifications: => this.#phoneRegex = obj.phoneRegex
     * TODO check for multiple country codes right now it is checking only one.
     * @param obj
     * @returns {boolean}
     */
    #phone(obj) {
        if (
            this.#phoneRegex.hasOwnProperty(obj.methodArgument[0]) &&
            !FormValidation.#verifyPattern(this.#phoneRegex[obj.methodArgument[0]], obj.value)
        ) {
            this.#messageBox.push(this.#defaultMessage.phone);
            return false;
        }
        return true;
    }

    /**
     * Validate address field in the form
     * Options available: => address
     * Modifications: => this.#addressRegex = obj.addressRegex
     *
     * @param obj
     * @returns {boolean}
     */
    #address(obj) {
        if (!FormValidation.#verifyPattern(this.#addressRegex, obj.value)) {
            this.#messageBox.push(this.#defaultMessage.address);
            return false;
        }
        return true;
    }

    /**
     * Validate email address field in the form
     * Options available: => email
     * Modifications: => this.#emailRegex = obj.emailRegex
     *
     * @param obj
     * @returns {boolean}
     */
    #email(obj) {
        if (!FormValidation.#verifyPattern(this.#emailRegex, obj.value)) {
            this.#messageBox.push(this.#defaultMessage.email);
            return false;
        }
        return true;
    }

    /**
     * Validate values with in options like select field in the form
     * Options available: = > within:2005,2006,2007,2008,2012
     * Modifications: = > None
     *
     * @param obj
     * @returns {boolean}
     */
    #within(obj) {
        let withinOptions = [];
        let withinOptionsLength = 0;
        let messageString = '';

        // example => methodArgument[0] = '2005,2006,2007,2008,2012'
        if (typeof obj.methodArgument[0] !== 'string' || obj.methodArgument[0].length <= 0) {
            this.#messageBox.push(this.#defaultMessage.reload);
            return false;
        }

        // methodArgument[0] needed to be split example: => [2005,2006,2007,2008,2012]
        withinOptions = FormValidation.#splitString(obj.methodArgument[0], this.#validatorWithinSeparator);
        withinOptionsLength = withinOptions.length;

        if (withinOptionsLength <= 0) {
            this.#messageBox.push(this.#defaultMessage.reload);
            return false;
        }

        // make the message string
        withinOptions.forEach((optionValue, index) => {
            if (withinOptionsLength === 1) {
                if (obj.element.type === 'select-one') {
                    let option = obj.element.querySelector('option[value="' + optionValue + '"]') || "";
                    if (option) {
                        messageString += option.innerHTML;
                    } else {
                        messageString += "Invalid option"
                    }
                } else if ( obj.element.type === 'select-multiple' ) { //TODO
                    messageString += optionValue;
                }
            } else if (index === withinOptionsLength - 1) {
                if(obj.element.type === 'select-one') {
                    let option = obj.element.querySelector('option[value="' + optionValue + '"]');
                    if (option) {
                        messageString += ' and ';
                        messageString += option.innerHTML;
                    }
                } else if ( obj.element.type === 'select-multiple' ) { // TODO
                    messageString += optionValue;
                }
            } else {
                if(obj.element.type === 'select-one') {
                    let option = obj.element.querySelector('option[value="' + optionValue + '"]');
                    if (option) {
                        messageString += option.innerHTML;
                    }
                } else if ( obj.element.type === 'select-multiple' ) { // TODO
                    messageString += optionValue;
                }
                messageString += ', ';
            }
        });

        // multiple select case
        if (obj.value instanceof Array) {
            let trigger = true;
            obj.value.forEach((value) => {
                if (!withinOptions.includes(value)) {
                    this.#messageBox.push(
                        this.#defaultMessage.within + ' It should contain ' + messageString + ' only.'
                    );
                    trigger = false;
                }
            });
            return trigger;
        }
        // regular select case
        else if (typeof obj.value === 'string') {
            if (!withinOptions.includes(obj.value)) {
                this.#messageBox.push(this.#defaultMessage.within + ' It should contain ' + messageString + ' only.');
                return false;
            }
        }

        return true;
    }

    /**
     * Validate maximum limit of characters or numeric data
     * Options available: = > max:10, here 10 could be characters or number
     * Modifications: = > None
     *
     * Note: = for number check use number word after limit e.g. max:10:number
     *
     * @param obj
     * @returns {boolean}
     */
    #max(
        obj // TODO combine max and min
    ) {
        let limit = Number(obj.methodArgument[0]);

        if (typeof obj.methodArgument[1] !== 'undefined' && obj.methodArgument[1] !== 'number') {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        } else if (
            typeof obj.methodArgument[1] !== 'undefined' &&
            obj.methodArgument[1] === 'number' &&
            isNaN(Number(obj.value))
        ) {
            this.#messageBox.push(this.#defaultMessage.number);
            return false;
        } else if (
            typeof obj.methodArgument[1] !== 'undefined' &&
            obj.methodArgument[1] === 'number' &&
            Number(obj.value) &&
            obj.value > limit
        ) {
            this.#messageBox.push(this.#defaultMessage.greater + ' ' + limit + '.');
            return false;
        } else if (typeof obj.methodArgument[1] === 'undefined' && obj.value.length > limit) {
            this.#messageBox.push(this.#defaultMessage.max + ' Limit is ' + limit + ' characters.');
            return false;
        }

        return true;
    }

    /**
     * Validate minimum limit of characters or numeric data
     * Options available: = > min:10, here 10 could be characters or number
     * Modifications: = > None
     *
     * Note: = for number check use number word after limit e.g. min:10:number
     *
     * @param obj
     * @returns {boolean}
     */
    #min(obj) {
        let limit = Number(obj.methodArgument[0]);

        if (typeof obj.methodArgument[1] !== 'undefined' && obj.methodArgument[1] !== 'number') {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        } else if (
            typeof obj.methodArgument[1] !== 'undefined' &&
            obj.methodArgument[1] === 'number' &&
            isNaN(Number(obj.value))
        ) {
            this.#messageBox.push(this.#defaultMessage.number);
            return false;
        } else if (
            typeof obj.methodArgument[1] !== 'undefined' &&
            obj.methodArgument[1] === 'number' &&
            Number(obj.value) &&
            obj.value < limit
        ) {
            this.#messageBox.push(this.#defaultMessage.smaller + ' ' + limit + '.');
            return false;
        } else if (typeof obj.methodArgument[1] === 'undefined' && obj.value.length < limit) {
            this.#messageBox.push(this.#defaultMessage.min + ' Limit is ' + limit + ' characters.');
            return false;
        }

        return true;
    }

    /**
     * Validate minimum limit of characters
     * Options available: = > exactLength:12, here 12 could be the exact length
     * of characters
     * Modifications: = > None
     *
     * @param obj
     * @returns {boolean}
     */
    #exactLength(obj) {
        let length;

        if (isNaN(obj.methodArgument[0])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        length = Math.floor(obj.methodArgument[0]);

        if (obj.value.length !== length) {
            this.#messageBox.push(this.#defaultMessage.exact + ' It must be of length ' + length + '.');
            return false;
        }

        return true;
    }

    /**
     * Validate date format
     * Options available: = > checkDate:datePattern
     * Modifications: = > dateRegex
     *
     * These are the datePatterns available: -
     * 'yyyy-mm-dd', 'yy-mm-dd', 'dd-mm-yyyy', 'dd-mm-yy',
     * 'yyyy/mm/dd', 'yy/mm/dd', 'dd/mm/yyyy', 'dd/mm/yy'
     * If we want something different then overwrite the default dateRegex
     * object.
     *
     * @param obj
     * @returns {boolean}
     */
    #checkDate(obj) {
        // check the user supplied pattern if matches
        if (!this.#dateRegex.hasOwnProperty(obj.methodArgument[0])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        // verify value matches the pattern
        if (!FormValidation.#verifyPattern(this.#dateRegex[obj.methodArgument[0]], obj.value)) {
            this.#messageBox.push(this.#defaultMessage.checkDate);
            return false;
        } // value matches the pattern
        else {
            // retrieve dateSeparator and verify the date
            let dateSeparator = null;

            for (const i in this.#dateSeparators) {
                if (obj.methodArgument[0].includes(this.#dateSeparators[i])) {
                    dateSeparator = this.#dateSeparators[i];
                    break;
                }
            }

            if (!dateSeparator) {
                this.#messageBox.push(this.#defaultMessage.generic);
                return false;
            }

            if (
                !FormValidation.#validateDate(
                    FormValidation.#splitString(obj.methodArgument[0], dateSeparator),
                    obj.value,
                    dateSeparator
                )
            ) {
                this.#messageBox.push(this.#defaultMessage.checkDate);
                return false;
            }

            return true;
        }
    }

    /**
     * Validate time format
     * Options available: = > checkTime:timeFormats:timeLayouts
     * Modifications: = > timeSeparator, time12Regex, time24Regex
     *
     * These are the timeFormats = [12, 24] are available
     * These are the timeLayouts = [His,his,Hi,hi] are available
     *
     * @param obj
     * @returns {boolean}
     */
    #checkTime(obj) {
        let separatedTime = [];
        let separatedTimeLength = 0;

        // obj.methodArgument[0] = hours format; could be 12 or 24
        if (!this.#timeFormats.hasOwnProperty(obj.methodArgument[0])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        if (
            obj.methodArgument[1] !== undefined &&
            !this.#timeFormats[obj.methodArgument[0]].hasOwnProperty(obj.methodArgument[1])
        ) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        } else if (
            obj.methodArgument[1] !== undefined &&
            this.#timeFormats[obj.methodArgument[0]].hasOwnProperty(obj.methodArgument[1])
        ) {
            if (
                FormValidation.#verifyPattern(
                    this.#timeFormats[obj.methodArgument[0]][obj.methodArgument[1]],
                    obj.value
                )
            ) {
                return true;
            }
        } else {
            for (const pattern in this.#timeFormats[obj.methodArgument[0]]) {
                if (FormValidation.#verifyPattern(this.#timeFormats[obj.methodArgument[0]][pattern], obj.value)) {
                    return true;
                }
            }
        }

        this.#messageBox.push(this.#defaultMessage.checkTime);
        return false;
    }

    /**
     * Validate datetime format
     * Options available: = > dateTime:dateTimePatterns
     * Modifications: = > dateTimePatterns, dateSeparators
     *
     *
     * @param obj
     * @returns {boolean}
     */
    #dateTime(obj) {
        if (!this.#dateTimeRegex.hasOwnProperty(obj.methodArgument[0])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        if (FormValidation.#verifyPattern(this.#dateTimeRegex[obj.methodArgument[0]], obj.value)) {
            let x = FormValidation.#splitString(obj.value, ' ');
            let dateSeparator = null;

            for (const i in this.#dateSeparators) {
                if (obj.methodArgument[0].includes(this.#dateSeparators[i])) {
                    dateSeparator = this.#dateSeparators[i];
                    break;
                }
            }

            if (
                FormValidation.#validateDate(
                    FormValidation.#splitString(obj.methodArgument[0], dateSeparator),
                    obj.value,
                    dateSeparator
                )
            ) {
                return true;
            }
        }

        this.#messageBox.push(this.#defaultMessage.dateTime);
        return false;
    }

    /**
     * Validate digit
     * Options available: = > digit
     * Modifications: = > positiveIntegerRegex
     *
     * @param obj
     * @returns {boolean}
     */
    #digit(obj) {
        if (!FormValidation.#verifyPattern(this.#positiveIntegerRegex, obj.value)) {
            this.#messageBox.push(this.#defaultMessage.digit);
            return false;
        }
        return true;
    }

    /**
     * Validate number
     * Options available: = > number
     * Modifications: = > None
     *
     * @param obj
     * @returns {boolean}
     */
    #number(obj) {
        if (isNaN(obj.value)) {
            this.#messageBox.push(this.#defaultMessage.number);
            return false;
        }
        return true;
    }

    /**
     * Validate decimal
     * Options available: = > decimal
     * Modifications: = > decimalRegex
     *
     * @param obj
     * @returns {boolean}
     */
    #decimal(
        obj // decimal // TODO give an option of decimal point
    ) {
        if (!FormValidation.#verifyPattern(this.#decimalRegex, obj.value)) {
            this.#messageBox.push(this.#defaultMessage.decimal);
            return false;
        }
        return true;
    }

    /**
     * Validate checkbox
     * Options available: = > checkbox
     * Modifications: = > none
     *
     * @param obj
     * @returns {boolean}
     */
    #checkBox(
        obj // decimal // TODO give an option of decimal point
    ) {
        console.log(obj.element.checked);
        console.log(obj.element.value);
        // {
        //     this.#messageBox.push(this.#defaultMessage.checkbox);
        //     return false;
        // }
        return true;
    }

    /**
     * Validate alphaNum
     * Options available: = > alphaNum:space:comma:hyphen:dot:brackets
     * Modifications: = > regexParams
     *
     * @param obj
     * @returns {boolean}
     */
    #alphaNum(obj) {
        let attachStr = '';
        let msgStr = '';
        let argLength = 0;
        let pattern;
        let finalPattern;

        // if there are other arguments
        if (obj.hasOwnProperty('methodArgument')) {
            argLength = obj.methodArgument.length;
            if (argLength > 0) {
                obj.methodArgument.forEach((param, index) => {
                    if (this.#regexParams.hasOwnProperty(param) && typeof this.#regexParams[param] !== 'undefined') {
                        attachStr += this.#regexParams[param];

                        msgStr +=
                            argLength === 1
                                ? param // if there is only one param
                                : index === argLength - 1
                                ? ' and ' + param //  the last param if more than one
                                : index === argLength - 2
                                ? param // the second last param
                                : param + ', '; // otherwise
                    }
                });
            }
        }

        pattern = '^[a-zA-Z0-9' + attachStr + ']+$';
        finalPattern = new RegExp(pattern);

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
        return true;
    }

    /**
     * Validate alpha
     * Options available: = > alpha
     * Modifications: = > alphaRegex
     *
     * @param obj
     * @returns {boolean}
     */
    #alpha(obj) {
        if (!this.#alphaRegex.test(obj.value)) {
            this.#messageBox.push(this.#defaultMessage.alpha);
            return false;
        }
        return true;
    }

    /**
     * Validate uuid
     * Options available: = > uuid
     * Modifications: = > uuidRegex
     *
     * @param obj
     * @returns {boolean}
     */
    #uuid(obj) {
        if (!this.#uuidRegex.test(obj.value)) {
            this.#messageBox.push(this.#defaultMessage.uuid);
            return false;
        }

        this.#messageBox.push('');
        return true;
    }

    /**
     * Validate via regex
     * Options available: = > regex:pattern
     * Modifications: = > None
     *
     * @param obj
     * @returns {boolean}
     */
    #regex(obj) {
        if (!this.#regexMethodPatterns.hasOwnProperty(obj.methodArgument[0])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        if (!FormValidation.#verifyPattern(this.#regexMethodPatterns[obj.methodArgument[0]], obj.value)) {
            this.#messageBox.push(this.#defaultMessage.invalid);
            return false;
        }

        return true;
    }

    /**
     * Validate file upload
     * Options available: = > file:extensions:size:sizeType:previewContainer
     * Modifications: = > fileSizes, validFileExtensions, imagePreviewShow
     *
     * extension: = > jpeg,jpeg,png,pdf...
     * size: = > 2
     * sizeType: = > MB
     *
     * @param obj
     * @returns {boolean}
     */
    #file(obj) {
        let checkExt = this.#getExtension(obj);
        let size = this.#getSize(obj);
        let fileSize;
        let sizeBytes;

        fileSize = obj.element.files[0].size;
        sizeBytes = this.#intoBytes(size);

        if (obj.hasOwnProperty('methodArgument') && obj.methodArgument[3] !== 'undefined') {
            this.#imagePreviewContainer = obj.methodArgument[3];
        }

        // File image preview container empty
        if (obj.element.type === 'file' && this.#imagePreviewContainer) {
            const imgPreviewContainer = document.getElementById(this.#imagePreviewContainer);
            if (imgPreviewContainer) {
                imgPreviewContainer.innerHTML = '';
            }
        }

        if (!sizeBytes) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        // File Size check
        if (fileSize > sizeBytes) {
            this.#messageBox.push(this.#defaultMessage.fileSize + ' ' + size[0] + ' ' + size[1] + '.');
            return false;
        }

        // File Extension check
        if (!this.#checkExtension(checkExt, obj)) {
            this.#messageBox.push(
                this.#defaultMessage.fileExtension + ' Only ' + obj.methodArgument[0] + ' file extensions are allowed.'
            );
            return false;
        }

        return true;
    }

    /**
     * Validate postcode country wise
     * Options available: = > postcode:country code
     * Modifications: = > none
     *
     * @param obj
     * @returns {boolean}
     */
    #postcode(obj) {
        if (
            this.#postcodeRegex.hasOwnProperty(obj.methodArgument[0]) &&
            !FormValidation.#verifyPattern(this.#postcodeRegex[obj.methodArgument[0]], obj.value)
        ) {
            this.#messageBox.push(this.#defaultMessage.postcode);
            return false;
        }
        return true;
    }

    /**
     * Validate text with regex
     * Options available: = > text
     * Modifications: = > none
     *
     * @param obj
     * @returns {boolean}
     */
    #text(obj) {
        if (!FormValidation.#verifyPattern(this.#textRegex, obj.value)) {
            this.#messageBox.push(this.#defaultMessage.text);
            return false;
        }
        return true;
    }

    /* ------------------------------------------------------------------------------------- Validation Helper Methods*/

    /**
     * Return file extensions set on user side with proper validation
     *
     * @param obj
     * @returns {boolean|*[]} false or array of valid extensions
     * eg: ['jpg', 'jpeg']
     */
    #getExtension(obj) {
        // 'file:jpg,jpeg,png' = > obj.methodArgument[0] = ['jpg', 'jpeg', 'png']
        let extensions = FormValidation.#splitString(obj.methodArgument[0], ',');
        let trigger = true;

        if (!extensions) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        // check extensions are one of the validFileExtensions
        extensions.forEach((x) => {
            if (!this.#validFileExtensions.includes(x)) {
                this.#messageBox.push(this.#defaultMessage.generic);
                trigger = false;
            }
        });

        return trigger ? extensions : false;
    }

    /**
     * Get size of the file uploaded
     *
     * @param obj
     * @returns {boolean|*[]} false or an array of size eg: ['2', 'MB']
     */
    #getSize(obj) {
        if (isNaN(obj.methodArgument[1])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        } else if (!this.#fileSizes.includes(obj.methodArgument[2])) {
            this.#messageBox.push(this.#defaultMessage.generic);
            return false;
        }

        return [obj.methodArgument[1], obj.methodArgument[2]];
    }

    /**
     * Convert the required size of file into bytes
     *
     * @param size [size, sizeType] ['2', 'MB']
     * @returns {boolean|number}
     */
    #intoBytes(size) {
        let sizeValue = size[0];
        let sizeType = size[1];

        return sizeType === 'MB'
            ? sizeValue * 1024 * 1024
            : sizeType === 'KB'
            ? sizeValue * 1024
            : sizeType === 'GB'
            ? sizeValue * 1024 * 1024 * 1024
            : false;
    }

    /**
     * Check the extension of the file uploaded and also set a preview of image
     * files.
     *
     * @param checkExt It is an array of valid extensions.
     * @param obj followed object
     * @returns {boolean}
     */
    #checkExtension(checkExt, obj) {
        let ext = obj.value.substring(obj.value.lastIndexOf('.') + 1).toLowerCase();

        // Match the extension with the validation extension
        if (!checkExt.includes(ext)) {
            return false;
        }

        // if file is an image and user wants to see the preview only then
        // perform below task
        if (this.#imageExtensions.includes(ext)) {
            if (obj.element.files && obj.element.files[0] && this.#imagePreviewShow && this.#imagePreviewContainer) {
                let reader = new FileReader();
                reader.onload = (e) => {
                    let i = document.getElementById(this.#imagePreviewContainer);
                    i.innerHTML = '<img src="' + e.target.result + '" alt="No Preview Available.">';
                };

                reader.readAsDataURL(obj.element.files[0]);
            }
        }

        return true;
    }

    /**
     * Validate the date
     *
     * @param dateParts ['yyyy', 'mm', 'dd']
     * @param dateValue obj.value
     * @param dateSeparator '/' or '-' ...
     * @returns {boolean}
     */
    static #validateDate(dateParts, dateValue, dateSeparator) {
        if (!dateParts) {
            return false;
        }

        let d = FormValidation.#splitString(dateValue, dateSeparator);
        let day = '';
        let month = '';
        let year = '';
        let monthLength = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

        if (dateParts[0] === 'yyyy' || dateParts[0] === 'yy') {
            if (dateParts[1] === 'mm') {
                day = parseInt(d[2], 10);
                month = parseInt(d[1], 10);
            } else if (dateParts[2] === 'mm') {
                day = parseInt(d[1], 10);
                month = parseInt(d[2], 10);
            }

            year = parseInt(d[0], 10);
        } else if (dateParts[2] === 'yyyy' || dateParts[2] === 'yy') {
            if (dateParts[1] === 'mm') {
                day = parseInt(d[0], 10);
                month = parseInt(d[1], 10);
            } else if (dateParts[0] === 'mm') {
                day = parseInt(d[1], 10);
                month = parseInt(d[0], 10);
            }

            year = parseInt(d[2], 10);
        }

        if (year < 1850 || year > 3000 || month < 1 || month > 12) return false;

        // leap year
        if (year % 400 === 0 || (year % 100 !== 0 && year % 4 === 0)) monthLength[1] = 29;

        return day > 0 && day <= monthLength[month - 1];
    }

    /* ------------------------------------------------------------------------------------ Data Manipulation Methods */

    /**
     * Capitalize or uppercase the first character of the word or every
     * character of the string.
     *
     * Options available: = > fcUpper or fcUpper:all
     * Modifications: = > None
     *
     * @param obj
     * @returns {boolean}
     */
    #fcUpper(obj) {
        if (obj.hasOwnProperty('methodArgument') && obj.methodArgument[0] === 'all') {
            let finalString = [];
            obj.value.split(' ').forEach(function (word) {
                finalString.push(word.charAt(0).toUpperCase() + word.slice(1));
            });
            obj.element.value = finalString.join(' ');
        } else {
            obj.element.value = obj.value.charAt(0).toUpperCase() + obj.value.slice(1);
        }

        return true;
    }

    /**
     * Upper case the string
     * Options available: = > upper
     * Modifications: = > None
     *
     * @param obj
     * @returns {boolean}
     */
    #upper(obj) {
        obj.element.value = obj.value.toUpperCase();
        return true;
    }

    /*------------------------------------------------------------------------------------------------ Getter Methods */

    /**
     *  Get an overview of all the validation methods supported by this class
     *  along with their usage and behaviour.
     *
     * @param viewType log || html || pdf || excel || object || json
     * @returns {string}
     */
    getAllValidationMethods(viewType = 'log') {
        switch (viewType) {
            case 'log':
                console.log(this.#validationMethods);
                break;
            case 'html':
                break;
            case 'pdf':
                break;
            case 'excel':
                break;
            case 'json':
                let x = JSON.stringify(this.#validationMethods);
                console.log(x);
        }
    }

    getSubmitResponse() {
        return this.#submitResponse;
    }

    /*------------------------------------------------------------------------------------------ Class Helper Methods */

    /**
     *  Split the string using split method in JavaScript using a separator.
     *
     * @param str String which is going to split
     * @param separator The separator based on which the string is going to be
     * separator.
     * @returns {boolean|string[]} return array of strings or false
     */
    static #splitString(str, separator) {
        if (typeof str === 'undefined' || typeof str !== 'string' || typeof separator !== 'string') {
            return false;
        }
        return str.split(separator);
    }

    /**
     * Pop first will return the first element of an array.
     *
     * @param arr Array
     * @returns {boolean|*} return false or the element from the array
     */
    static #popFirst(arr) {
        if (typeof arr === 'undefined' || !arr instanceof Array || arr.length <= 0) {
            return false;
        }

        const [, ...a] = arr;
        return a;
    }

    /**
     * Verify the regex patterns using test method of JavaScript
     *
     * @param pattern regex pattern
     * @param value the string which is going to match against the pattern
     * @returns {boolean}
     */
    static #verifyPattern(pattern, value) {
        const p = new RegExp(pattern);
        return p.test(value);
    }

    /*--------------------------------------------------------------------------------------------- DEBUGGING METHODS */
    /**
     * Generate random integer value
     *
     * @returns {number}
     */
    static #getRandomInt() {
        return Math.floor(Math.random() * 8999 + 9999);
    }

    /**
     * return new Error().stack
     *
     * @returns {string|number}
     */
    static #line() {
        let stack;
        let frame;
        let frameRE = /:(\d+):(?:\d+)[^\d]*$/;
        let e = new Error();

        if (!e.stack)
            try {
                // IE requires the Error to actually be thrown or else the Error's
                // 'stack' property is undefined.
                throw e;
            } catch (e) {
                if (!e.stack) {
                    return 0; // IE < 10, likely
                }
            }

        stack = e.stack.toString().split(/\r\n|\n/);

        // We want our caller's frame. It's index into |stack| depends on the
        // browser and browser version, so we need to search for the second frame:

        do {
            frame = stack.shift();
        } while (!frameRE.exec(frame) && stack.length);

        return frameRE.exec(stack.shift())[1];
    }

    /**
     * DEBUGGING METHOD
     *
     * Create an array all the console.log prints.
     * The str = message = key whereas color, size, weight = style = value
     *
     * @param str It is the string message.
     * @param color The color of the string message.
     * @param size The font size of the string message.
     * @param weight The font weight of the string message.
     */
    #print(str, color, size, weight) {
        let c = color || 'white';
        let s = size || '12px';
        let w = weight || 'normal';
        this.#printConsole[
            '%c' + '@' + FormValidation.#getRandomInt() + ' ' + str
        ] = `color:${c};font-size:${s}px;font-weight:${w}`;
    }

    /**
     * DEBUGGING METHOD
     *
     * Final print will clear the console and print all the elements in print
     * console.
     *
     */
    #finalPrint() {
        if (!this.#debug) {
            return false;
        }

        // DEBUGGING
        this.#print(
            `|===========================================================================================|`,
            'pink'
        );

        console.clear();
        for (const i in this.#printConsole) {
            console.log(i, this.#printConsole[i]);
        }
    }
}
