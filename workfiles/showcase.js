var current = -1;
var initialized = false;
var available = []; //["entry0", "entry1", "entry2"];
var list_elements = [];

function make_onclick(i) {
  // required to work as expected, as of: https://stackoverflow.com/a/22122473
  return function () {
    show(i);
  };
}

function initialize_showcase() {
  // first step: collect all available entries

  // OLD METHOD FROM ENTRY STORAGE
  for (const elem of document
    .getElementById("entry-storage")
    .getElementsByClassName("showcase-content")) {
    available.push(elem.id);
  }

  // second step, populate contents list with correct number and callback

  // the prototype div used for content list elements
  const entry_prototype = document.getElementById(
    "showcase-navbar-entry-prototype",
  );

  // the root for all content list items
  const contents_root = document.getElementById("showcase-navbar-root");

  var index = 0;
  for (const id of available) {
    var clone = entry_prototype.cloneNode(true);
    clone.onclick = make_onclick(index);
    list_elements.push(clone);

    //console.log("found element: " + clone);

    contents_root.appendChild(clone);
    index += 1;
  }

  initialized = true;

  // assure everything is synced correctly
  show(index-1);
}

function show(index) {
  if (!initialized) initialize_showcase();
  if (index == current) return;

  if (index >= available.length) index = 0;
  if (index < 0) index = available.length - 1;

  //console.log("show " + index);

  const current_element = document.getElementById("current_entry");
  current_element.innerHTML = document.getElementById(
    available[index],
  ).innerHTML;

  current_element.style.animation = "none";
  current_element.offsetHeight;
  current_element.style.animation = "fadein 0.3s ease";

  // remove selected state from current, then add to index
  if (current != -1) {
    list_elements[current].classList.remove("showcase-navbar-entry-current");
    list_elements[current].classList.add("showcase-navbar-entry");
  }

  list_elements[index].classList.remove("showcase-navbar-entry");
  list_elements[index].classList.add("showcase-navbar-entry-current");

  current = index;
}

function show_next(dir) {
  show(current + dir);
}

window.onload = function () {
  //console.log("laod showcase!");
  initialize_showcase();
};
