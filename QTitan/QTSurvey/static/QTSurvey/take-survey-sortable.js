var TakeSurvey = class {
  constructor() { this.run(); }

  // Updates hidden form fields on drag-and-drop
  handleDrop() {
    // Drag and drop fields
    var visibleFields = this.getElementsByTagName("li");

    // Length of arguments
    const n = visibleFields.length

    // On drop, set hiddenField values to the corresponding visibleField values.
    for (var i = 0; i < n; i++) document.getElementById(i).value = visibleFields[i].innerHTML;

    for (var i = 0; i < n; i++) {
      console.log(visibleFields[i].innerHTML + " == " + document.getElementById(i).value + '&& ' + i + ' == ' + document.getElementById(i).id);
    }
  }

  // Sortable factory
  makeSortable() {
    $("#sortableSurveyFields").sortable();
    $("#sortableSurveyFields").disableSelection();
  }

  // Drop handler factory
  makeDrop() {
    $("#sortableSurveyFields").sortable({ stop: this.handleDrop });
  }

  // Run
  run() {
    this.makeSortable();
    this.makeDrop();
  }
}

var hideDjangoErrorList = () => { $('.errorlist').hide(); };

$(document).ready(function() {
  hideDjangoErrorList();
  const survey = new TakeSurvey();
});
