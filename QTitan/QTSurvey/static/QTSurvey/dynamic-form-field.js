// Survey Object and Handlers
const CreateSurvey = (fieldID) => {
  // Constructor
  //constructor(fieldID) { eval(`this.${fieldID}Visible = 1`); this.maxFields = 15; this.fieldID = fieldID; this.run(); }
  let _fieldID = fieldID;
  let _maxFields = 15;
  let _fieldsVisible = 1;

  // Return max fields
  const getMaxFields = () => { return _maxFields; };

  // Return fieldID
  const getFieldID = () => { return _fieldID; };

  // Return current fields visible
  const getFieldsVisible = () => { return _fieldsVisible; };

  // Increment fields visible and return the new val
  const incrementFieldsVisible = () => { return ++_fieldsVisible; };

  // Decrement fields visible and return the new val
  const decrementFieldsVisible = () => { return --_fieldsVisible; };

  // Hide fields 2-maxFields on init
  const hideFieldsOnInit = () => {
    const fieldID = getFieldID();
    const maxFields = getMaxFields();

    for (let i = 2; i <= maxFields; i++) $(`#${fieldID}${i}`).hide();
  }

  // Add new field handler
  const handleAddNewField = () => {
    const fieldID = getFieldID();
    const maxFields = getMaxFields();

    $(`#add-${fieldID}`).click(function(e) {
      e.preventDefault();

      let fieldsVisible = getFieldsVisible();

      if ($(`#${fieldID}${fieldsVisible}`).val() && fieldsVisible < maxFields) {
        fieldsVisible = incrementFieldsVisible();
        $(`#${fieldID}${fieldsVisible}`).show();
        $(`#${fieldID}${fieldsVisible}`).val('');
      }

      document.getElementById(`${fieldID}${fieldsVisible}`).focus();
    });
  }

  // Delete field handler (when user deletes text)
  const handleDeleteFieldText = () => {
    const fieldID = getFieldID();
    const maxFields = getMaxFields();

    for (let i = 1; i <= maxFields; i++) {
      $(`#${fieldID}${i}`).on('input keyup paste', function() {
        let fieldsVisible = getFieldsVisible();
        let hasValue = $.trim(this.value).length;
        if (!hasValue) rearrangeInputs(this.id);
      });
    }
  }

  // Rearrange input values on delete
  const rearrangeInputs = (deletedField) => {
    const fieldID = getFieldID();
    let fieldsVisible = getFieldsVisible();

    let n = deletedField.length;

    let deletedFieldNumber = parseInt(deletedField.slice(n - 2, n)) || parseInt(deletedField.slice(n - 1, n));

    // Deleted last field or first field
    if (deletedFieldNumber == fieldsVisible) {
      // Set field val to an empty string
      $(`#${deletedField}`).val('');

      // If the deleted field number is > 1, hide the field and decrement fieldsVisible
      if (deletedFieldNumber > 1) {
        $(`#${deletedField}`).hide();
        fieldsVisible = decrementFieldsVisible();
      }

    } else {
      for (let i = deletedFieldNumber; i < fieldsVisible; i++) {
        $(`#${fieldID}${i}`).val($(`#${fieldID}${i + 1}`).val());
        if (i + 1 == fieldsVisible) $(`#${fieldID}${fieldsVisible}`).hide();
      }

      fieldsVisible = decrementFieldsVisible();
    }
  }

  // Run all handlers
  const run = () => {
    // Initially hide fields 2-maxFields
    hideFieldsOnInit();

    // Install handler for add new field
    handleAddNewField();

    // Install handler for delete field
    handleDeleteFieldText();
  }

  run();
}

// Save Object and Handlers
const Save = class {
  constructor(fieldID) {
    this.fieldID = fieldID;
    this.errorMessages = {
      'title':        'Survey must have a title',
      'description':  'Survey must have a description',
      'numOptions':   'Survey must have a minimum of 5 options',
      'duplicates':   'Survey cannot have duplicate options',
      'nullFields':   'Survey cannot have null fields'};

    this.run();
  }

  getFieldID() { return this.fieldID; }

  handleSave() {
    const fieldID = this.getFieldID();
    const handleSaveError = this.handleSaveError;
    const errorMessages = this.errorMessages;

    $('#save-survey').click(function(e) {

      const errors = new Set();

      const options = new Set();

      // Check for null title
      if (!$('#title').val()) errors.add('title');

      // Check for null description
      if (!$('#description').val()) errors.add('description');

      // Check for null options 1-5
      for (let i = 1; i <= 5; i++)
        if (!$(`#${fieldID}${i}`).val()) errors.add('numOptions');

      // Check for duplicate values
      for (let i = 1; i <= 15; i++) {
        let fieldValue = $(`#${fieldID}${i}`).val().trim()
        if (fieldValue && options.has(fieldValue)) errors.add('duplicates');
        options.add(fieldValue);
      }

      // Check for null fields
      for (let i = 1; i <= 15; i++) {
        let fieldValue = $(`#${fieldID}${i}`).val();
        if (fieldValue && !fieldValue.trim()) errors.add('nullFields');
      }

      handleSaveError(e, errors, errorMessages);
    });
  }

  handleSaveError(e, errors, errorMessages) {
    if (errors.size) {
      e.preventDefault();
      let errorMsg = ''
      for (let error of errors) errorMsg += '- ' + errorMessages[error] + "<br>";

      $('#form-errors').css('color', 'red');
      $('#form-errors').html(errorMsg);
    }
  }

  run() {
    this.handleSave();
  }
}


// Temporary hide ul class "errorList" <-- Fix if there's time, otherwise it works as is.
// Django by default will display an ugly <ul> that says "this field is required" for required fields
// This gets around that by just hiding the errorlist class.
// First 5 survey options are required.
const hideDjangoErrorList = () => { $('.errorlist').hide(); };

// Run
$(document).ready(function() {
  hideDjangoErrorList();
  const saveHandler = new Save('field');

  // Survey Fields
  CreateSurvey('field');

  // Demographic Fields
  CreateSurvey('demographicfield');
});
