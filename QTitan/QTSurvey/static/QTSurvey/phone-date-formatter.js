// Months/days
const daysInMonths = {
  1: 31,
  2: 28,
  3: 31,
  4: 30,
  5: 31,
  6: 30,
  7: 31,
  8: 31,
  9: 30,
  10: 31,
  11: 30,
  12: 31
};

// Check for leap year
isLeapYear = (year) => { return ((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0); }

// Check for valid DOB
isValidDOB = (dob) => {
  const month = parseInt(dob.substr(0, 2));
  const day = parseInt(dob.substr(3, 2));
  const year = parseInt(dob.substr(6, 4));

  return (month in daysInMonths) &&
         (day > 0) &&
         (month == 2 ? day <= (isLeapYear(year) ? daysInMonths[month] + 1 : daysInMonths[month]) : day <= daysInMonths[month]) &&
         (year >= 1900 && year <= 2017);
}

// Formatting for phone number
$('#phone-number').mask('(999) 999-9999');

// Formatting for DOB
$('#date-of-birth').mask('99/99/9999');

// DOB validity
$('#submit-registration').click(function(e) {
  if (!isValidDOB($('#date-of-birth').val())) {
    e.preventDefault();
    document.getElementById('error-message').innerHTML = 'Please enter a valid date of birth';
  } else {
    const phone = $('#phone-number').val()
                                    .replace('(', '')
                                    .replace(')', '')
                                    .replace('-', '')
                                    .replace(' ', '');
    $('#phone-number').val(phone);
  }
});
