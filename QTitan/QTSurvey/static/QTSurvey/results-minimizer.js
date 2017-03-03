$(document).ready(function() {
  $('.minimizer').click(function() {
    // Get participant ID
    let participantID = this.getAttribute('participantid');

    // Get div for current participant's results
    let participantResults = $(`#participant${participantID}`);

    // slideUp/slideDown toggle
    participantResults.is(':visible') ? participantResults.slideUp('fast') : participantResults.slideDown('fast');

    // Change button class
    $(this).attr({'class': $(this).attr('class') == 'minimizer btn btn-danger' ? 'minimizer btn btn-primary' : 'minimizer btn btn-danger'});

    // Set button text
    this.innerHTML = this.innerHTML == '-' ? '+' : '-';
  });
});
