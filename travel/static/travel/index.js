////////////previous dates

$(function () {
  var dtToday = new Date();

  var month = dtToday.getMonth() + 1;
  var day = dtToday.getDate();
  var year = dtToday.getFullYear();
  if (month < 10) month = "0" + month.toString();
  if (day < 10) day = "0" + day.toString();

  var maxDate = year + "-" + month + "-" + day;

  // Initialize the departure datepicker
  $("#departure").flatpickr({
    minDate: maxDate,
    dateFormat: "Y-m-d",
    altInput: true,
    altFormat: "F j, Y",
    onChange: function (selectedDates, dateStr, instance) {
      // Update the minimum date of the return datepicker when the departure date changes
      returnDatepicker.set("minDate", dateStr);

      ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// Roundtrip bozuksa bunu kaldır
      // Set the return datepicker to open at the month of the selected departure date without selecting it
      returnDatepicker.jumpToDate(dateStr); // This makes the calendar jump to the month of the departure date

      //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    },
  });

  // Initialize the return datepicker
  var returnDatepicker = $("#return").flatpickr({
    minDate: maxDate,
    dateFormat: "Y-m-d",
    altInput: true,
    altFormat: "F j, Y",
  });

  // Initialize the date of birth datepicker to allow dates up to today
  var dateOfBirthDatepicker = $("#date").flatpickr({
    maxDate: maxDate, // Allow any past date up to today
    dateFormat: "Y-m-d",
    altInput: true,
    altFormat: "F j, Y",
  });
});

// function formatDate(input) {
//  const dateObject = new Date(input.value);
//  const options = { month: "long", day: "numeric", year: "numeric" };
//  input.value = dateObject.toLocaleDateString("en-US", options);
//}

// disable one way
const returnDatepicker = document.querySelector("#return-datepicker");
const returnDate = document.querySelector("#return");
const oneWayRadio = document.querySelector("#one-way");
const roundtripRadio = document.querySelector("#roundtrip");
const returnText = document.querySelector("#return-text");

function disableReturnDate() {
  returnDatepicker.style.opacity = "0.3";
  returnDatepicker.style.pointerEvents = "none";
  returnDate.value = "";
  returnText.style.color = "rgba(239, 239, 239, 0.3)";
  localStorage.setItem("selectedOption", "one-way");
}

function enableReturnDate() {
  returnDatepicker.style.opacity = "1";
  returnDatepicker.style.pointerEvents = "auto";
  returnDate.value = "";
  returnText.style.color = "white";
  localStorage.setItem("selectedOption", "roundtrip");
}

oneWayRadio.addEventListener("click", disableReturnDate);
roundtripRadio.addEventListener("click", enableReturnDate);

// Restore the selected option on page load
window.addEventListener("pageshow", function () {
  const selectedOption = localStorage.getItem("selectedOption");
  if (selectedOption === "one-way") {
    oneWayRadio.checked = true;
    disableReturnDate();
  } else {
    roundtripRadio.checked = true;
    enableReturnDate();
  }
});

// eski kodum bu ama buglıydı
// document.querySelector("#return")

// document.querySelector('#one-way').addEventListener('click', () => {
// returnDate.disabled = true
// returnDate.value = ''

// document.querySelector('#return-text').style.color = 'rgba(239, 239, 239, 0.3)'
// })

// document.querySelector('#roundtrip').addEventListener('click', () => {
// returnDate.disabled = false
// returnDate.value = ''

// document.querySelector('#return-text').style.color = 'white'
// })

////

var options = {
  shouldSort: true,
  threshold: 0.4,
  maxPatternLength: 32,
  keys: [
    {
      name: "iata",
      weight: 0.5,
    },
    {
      name: "name",
      weight: 0.3,
    },
    {
      name: "city",
      weight: 0.2,
    },
  ],
};

var fuse = new Fuse(airports, options);

var ac = $("#autocomplete")
  .on("click", function (e) {
    e.stopPropagation();
  })
  .on("focus keyup", search)
  .on("keydown", onKeyDown);

var wrap = $("<div>")
  .addClass("autocomplete-wrapper")
  .insertBefore(ac)
  .append(ac);

var list = $("<div>")
  .addClass("autocomplete-results")
  .on("click", ".autocomplete-result", function (e) {
    e.preventDefault();
    e.stopPropagation();
    selectIndex($(this).data("index"));
  })
  .appendTo(wrap);

$(document)
  .on("mouseover", ".autocomplete-result", function (e) {
    var index = parseInt($(this).data("index"), 10);
    if (!isNaN(index)) {
      list.attr("data-highlight", index);
    }
  })
  .on("click", clearResults);

function clearResults() {
  results = [];
  numResults = 0;
  list.empty();
}

function selectIndex(index) {
  if (results.length >= index + 1) {
    ac.val(results[index].iata);
    clearResults();
  }
}

var results = [];
var numResults = 0;
var selectedIndex = -1;

function search(e) {
  if (e.which === 38 || e.which === 13 || e.which === 40) {
    return;
  }

  if (ac.val().length > 0) {
    results = _.take(fuse.search(ac.val()), 7);
    numResults = results.length;

    var divs = results.map(function (r, i) {
      return (
        '<div class="autocomplete-result" data-index="' +
        i +
        '">' +
        "<div><b>" +
        r.iata +
        "</b> - " +
        r.name +
        "</div>" +
        '<div class="autocomplete-location">' +
        r.city +
        ", " +
        r.country +
        "</div>" +
        "</div>"
      );
    });

    selectedIndex = -1;
    list.html(divs.join("")).attr("data-highlight", selectedIndex);
  } else {
    numResults = 0;
    list.empty();
  }
}

function onKeyDown(e) {
  switch (e.which) {
    case 38: // up
      selectedIndex--;
      if (selectedIndex <= -1) {
        selectedIndex = -1;
      }
      list.attr("data-highlight", selectedIndex);
      break;
    case 13: // enter
      selectIndex(selectedIndex);
      break;
    case 9: // enter
      selectIndex(selectedIndex);
      e.stopPropagation();
      return;
    case 40: // down
      selectedIndex++;
      if (selectedIndex >= numResults) {
        selectedIndex = numResults - 1;
      }
      list.attr("data-highlight", selectedIndex);
      break;

    default:
      return; // exit this handler for other keys
  }
  e.stopPropagation();
  e.preventDefault(); // prevent the default action (scroll / move caret)
}
