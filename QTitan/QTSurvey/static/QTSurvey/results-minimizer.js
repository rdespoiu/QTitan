$(document).ready(function() {
  $('.minimizer').click(function() {
    let participantID = this.getAttribute('participantid');
    let participantResults = document.getElementById(`participant${participantID}`);

    participantResults.hide();
  });
});
