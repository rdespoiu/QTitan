$(document).ready(function() {

  var next = 1;
  $(".add-more").click(function(e) {
    e.preventDefault();
    var addto = "#field" + (next);
    var addRemove = "#field" + (next);
    next++;

    var newIn = '<input autocomplete="off" class="form-control create-survey-form input survey-option" id="field' + next + '" name="field' + next + '" type="text" placeholder="survey option">';
    var newInput = $(newIn);
    var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >-</button></div><div id="field">';
    var removeButton = $(removeBtn);

    $(addto).after(newInput);
    $(addRemove).after(removeButton);
    $("#field" + next).attr('data-source', $(addto).attr('data-source'));
    $("#count").val(next);

      $('.remove-me').click(function(e) {
        e.preventDefault();
        var fieldNum = this.id.charAt(this.id.length - 1);
        var fieldID = "#field" + fieldNum;
        $(this).remove();
        $(fieldID).remove();
      });

  });

});
