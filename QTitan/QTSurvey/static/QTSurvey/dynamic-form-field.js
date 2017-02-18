// Survey Object and Handlers
var CreateSurvey = class {
  // Constructor
  constructor() { this.fieldsVisible = 1; this.run(); }

  // Return current fields visible
  getFieldsVisible() { return this.fieldsVisible; }

  // Increment fields visible and return the new val
  incrementFieldsVisible() { return ++this.fieldsVisible; }

  // Decrement fields visible and return the new val
  decrementFieldsVisible() { return --this.fieldsVisible; }

  // Hide fields 2-30 on init
  hideFieldsOnInit() {
    for (var i = 2; i <= 30; i++) $('#field' + i).hide();
  }

  // Add new field handler
  handleAddNewField() {
    self = this;

    $('#add-field').click(function(e) {
      e.preventDefault();

      var fieldsVisible = self.getFieldsVisible();

      if ($('#field' + fieldsVisible).val() && fieldsVisible < 30) {
        fieldsVisible = self.incrementFieldsVisible()
        $('#field' + fieldsVisible).show();
        $('#field' + fieldsVisible).val('');
      }
    });
  }

  // Delete field handler (when user deletes text)
  handleDeleteFieldText() {
    self = this;

    for (var i = 1; i <= 30; i++) {
      $('#field' + i).on('input keyup paste', function() {
        var fieldsVisible = self.getFieldsVisible();
        var hasValue = $.trim(this.value).length;
        if (!hasValue) self.rearrangeInputs(this.id);
      });
    }
  }

  // Rearrange input values on delete
  rearrangeInputs(deletedField) {
    self = this;
    var fieldsVisible = self.getFieldsVisible();

    var n = deletedField.length;

    var deletedFieldNumber = parseInt(deletedField.slice(n - 2, n)) || parseInt(deletedField.slice(n - 1, n));

    // Deleted last field or first field
    if (deletedFieldNumber == fieldsVisible) {
      // Set field val to an empty string
      $('#' + deletedField).val('');

      // If the deleted field number is > 1, hide the field and decrement fieldsVisible
      if (deletedFieldNumber > 1) {
        $('#' + deletedField).hide();
        fieldsVisible = self.decrementFieldsVisible();
      }

    } else {
      for (var i = deletedFieldNumber; i < fieldsVisible; i++) {
        $('#field' + i).val($('#field' + (i + 1)).val());
        if (i + 1 == fieldsVisible) $('#field' + fieldsVisible).hide();
      }

      fieldsVisible = self.decrementFieldsVisible();
    }
  }

  // Run all handlers
  run() {
    // Initially hide fields 2-30
    this.hideFieldsOnInit();

    // Install handler for add new field
    this.handleAddNewField();

    // Install handler for delete field
    this.handleDeleteFieldText();
  }
}

// Save Object and Handlers
var Save = class {
  constructor() {
    this.errorMessages = {
      'title':        'Survey must have a title',
      'description':  'Survey must have a description',
      'numOptions':   'Survey must have a minimum of 5 options'};

    this.run();
  }

  handleSave() {
    var handleSaveError = this.handleSaveError;
    var errorMessages = this.errorMessages;

    $('#save-survey').click(function(e) {

      var errors = new Set();

      // Check for null title
      if (!$('#title').val()) errors.add('title');

      // Check for null description
      if (!$('#description').val()) errors.add('description');

      // Check for null options 1-5
      for (var i = 1; i <= 5; i++)
        if (!$('#field' + i).val()) errors.add('numOptions');

      handleSaveError(e, errors, errorMessages);
    });
  }

  handleSaveError(e, errors, errorMessages) {
    if (errors.size) {
      e.preventDefault();
      var errorMsg = ''
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
var hideDjangoErrorList = () => { $('.errorlist').hide(); };

// Run
$(document).ready(function() {
  hideDjangoErrorList();
  new Save();
  new CreateSurvey();
});
