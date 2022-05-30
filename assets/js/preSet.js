let brightnessInput = document.getElementById("brightnessInput"),
  brightnessLabel = document.getElementById("brightnessLabel"),
  BGColor = document.getElementById("BGColor"),
  MarkerColor = document.getElementById("MarkerColor"),
  preview = document.getElementById("preview"),
  startButton = document.getElementById("startButton"),
  MarkerSize = document.getElementById("MarkerSize"),
  MarkerDensity = document.getElementById("MarkerDensity"),
  MarkerType = document.getElementById("MarkerType"),
  confirmcopy = document.getElementById("confirmcopy");

const marker_circle = "assets/img/marker_circle.svg",
  marker_cross = "assets/img/marker_cross.svg",
  marker_pie = "assets/img/marker_pie.svg",
  marker_triangle = "assets/img/marker_triangle.svg";

var imgPath = "";
var width = "";

const bgColor = "bgC",
  markerColor = "mC",
  markerDensity = "mD",
  markerSize = "mS",
  markerType = "mT";

let isFullScreen = false;
// Default Values
brightnessLabel.innerHTML = "Overall brightness: " + brightnessInput.value;
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
if(queryString !== '' && queryString !== null && queryString !== undefined){
  BGColor.value = urlParams.get(bgColor)
  MarkerColor.value = urlParams.get(markerColor)
  MarkerDensity.value = urlParams.get(markerDensity)
  MarkerSize.value = urlParams.get(markerSize)
  MarkerType.value = urlParams.get(markerType)
}


// Set Brightness
brightnessInput.addEventListener('input', function () {
  brightnessLabel.innerHTML = "Overall brightness: " + brightnessInput.value;
  preview.style.filter = "brightness(" + brightnessInput.value + "%)";
}, false);

// Set BG Color
BGColor.addEventListener('input', function () {
  preview.style.backgroundColor = BGColor.value;
}, false);

// Set Marker Color
MarkerColor.addEventListener('input', function () {
  Array.from(preview.getElementsByClassName("svg")).forEach(function (element) {
    element.contentDocument.querySelectorAll("svg")[0].setAttribute("style", "fill: " + MarkerColor.value);
  });
}, false);

// Set Marker Density
MarkerDensity.addEventListener('input', function () {
  updatePreview();
}, false);

MarkerSize.addEventListener('input', function () {
  updatePreview();
}, false);

// Set marker type
MarkerType.addEventListener('input', function () {
  switch (MarkerType.value) {
    case "circle":
      imgPath = marker_circle;
      break;
    case "cross":
      imgPath = marker_cross;
      break;
    case "pie":
      imgPath = marker_pie;
      break;
    case "triangle":
      imgPath = marker_triangle;
      break;
    default:
      console.log("Sorry, we are out of " + expr + ".");
  }
  Array.from(preview.getElementsByClassName("svg")).forEach(function (element) {
    element.data = "";
    element.data = imgPath;
  });
  setTimeout(function () {
    Array.from(preview.getElementsByClassName("svg")).forEach(function (element) {
      element.contentDocument.querySelectorAll("svg")[0].setAttribute("style", "fill: " + MarkerColor.value);
    });
  }, 500);
}, false);

// fill on start
preview.style.backgroundColor = BGColor.value;
updatePreview();

function updatePreview() {
  preview.style.position = "relative";

  while (preview.hasChildNodes()) {
    preview.removeChild(preview.firstChild);
    preview.style.backgroundColor = BGColor.value;
  }
  switch (MarkerType.value) {
    case "circle":
      imgPath = marker_circle;
      break;
    case "cross":
      imgPath = marker_cross;
      break;
    case "pie":
      imgPath = marker_pie;
      break;
    case "triangle":
      imgPath = marker_triangle;
      break;
    default:
      console.log("Sorry, we are out of " + expr + ".");
  }
  setDefaultTracker(imgPath);
  if (MarkerDensity.value >= 2) {
    setDefaultTracker2(imgPath);
    if (MarkerDensity.value == 3) {
      setDefaultTracker3(imgPath);
    }
  }
  // UGLY - Wartet bis alle SVGs geladen sind
  setTimeout(function () {
    Array.from(preview.getElementsByClassName("svg")).forEach(function (element) {
      element.contentDocument.querySelectorAll("svg")[0].setAttribute("style", "fill: " + MarkerColor.value);
    });
  }, 500);
}

function handlerfunktion(event) {
  
if(device.platform != 'browser'){
  if (!isFullScreen) {
    isFullScreen = true;
    window.powermanagement.acquire();
  } else {
    isFullScreen = false;
    window.powermanagement.release();

  }
}
}

function startPreSet() {
  if (preview.requestFullscreen) {
    preview.requestFullscreen();
  } else if (preview.msRequestFullscreen) { // for IE11 (remove June 15, 2022)
    preview.msRequestFullscreen();
  } else if (preview.webkitRequestFullscreen) { // iOS Safari
    preview.webkitRequestFullscreen();
  }
}

  preview.onfullscreenchange = handlerfunktion;


function setDefaultTracker(imgPath) {
  switch (MarkerSize.value) {
    case "1":
      width = "3%";
      break;
    case "2":
      width = "6%";
      break;
    case "3":
      width = "9%";
      break;
    case "4":
      width = "12%";
      break;
    case "5":
      width = "15%";
      break;
  }

  var imgLeftTop = document.createElement('object');
  imgLeftTop.classList.add("marker", "svg");
  imgLeftTop.data = imgPath;
  imgLeftTop.style.top = "3%";
  imgLeftTop.style.left = "3%";
  imgLeftTop.style.width = width;

  var imgRightTop = document.createElement('object');
  imgRightTop.classList.add("marker", "svg");
  imgRightTop.data = imgPath;
  imgRightTop.style.top = "3%";
  imgRightTop.style.right = "3%";
  imgRightTop.style.width = width;

  var imgLeftBottom = document.createElement('object');
  imgLeftBottom.classList.add("marker", "svg");
  imgLeftBottom.data = imgPath;
  imgLeftBottom.style.bottom = "3%";
  imgLeftBottom.style.left = "3%";
  imgLeftBottom.style.width = width;

  var imgRightBottom = document.createElement('object');
  imgRightBottom.classList.add("marker", "svg");
  imgRightBottom.data = imgPath;
  imgRightBottom.style.bottom = "3%";
  imgRightBottom.style.right = "3%";
  imgRightBottom.style.width = width;

  var imgCenter = document.createElement('object');
  imgCenter.data = imgPath;
  imgCenter.classList.add("marker", "svg");
  imgCenter.style.top = "50%";
  imgCenter.style.left = "50%";
  imgCenter.style.width = width;
  imgCenter.style.transform = "translate(-50%, -50%)";

  preview.append(imgLeftTop, imgRightTop, imgLeftBottom, imgRightBottom, imgCenter);

}


function setDefaultTracker2(imgPath) {
  var imgLeft = document.createElement('object');
  imgLeft.data = imgPath;
  imgLeft.classList.add("marker", "svg");
  imgLeft.style.left = "3%";
  imgLeft.style.top = "50%";
  imgLeft.style.bottom = "50%";
  imgLeft.style.width = width;
  imgLeft.style.transform = "translateY(-50%)";

  var imgRight = document.createElement('object');
  imgRight.data = imgPath;
  imgRight.classList.add("marker", "svg");
  imgRight.style.right = "3%";
  imgRight.style.top = "50%";
  imgRight.style.bottom = "50%";
  imgRight.style.width = width;
  imgRight.style.transform = "translateY(-50%)";

  var imgTop = document.createElement('object');
  imgTop.id = "imgLeftBottom";
  imgTop.data = imgPath;
  imgTop.classList.add("marker", "svg");
  imgTop.style.top = "3%";
  imgTop.style.left = "50%";
  imgTop.style.right = "50%";
  imgTop.style.width = width;
  imgTop.style.transform = "translateX(-50%)";

  var imgBottom = document.createElement('object');
  imgBottom.id = "imgBottom";
  imgBottom.classList.add("marker", "svg");
  imgBottom.data = imgPath;
  imgBottom.style.bottom = "3%";
  imgBottom.style.left = "50%";
  imgBottom.style.right = "50%";
  imgBottom.style.width = width;
  imgBottom.style.transform = "translateX(-50%)";

  preview.append(imgLeft, imgRight, imgTop, imgBottom);
}

function setDefaultTracker3(imgPath){
  var imgBetweenLeftTop = document.createElement('object');
  imgBetweenLeftTop.classList.add("marker", "svg");
  imgBetweenLeftTop.data = imgPath;
  imgBetweenLeftTop.style.left = "25%";
  imgBetweenLeftTop.style.top = "25%";
  imgBetweenLeftTop.style.width = width;


  var imgBetweenRightTop = document.createElement('object');
  imgBetweenRightTop.classList.add("marker", "svg");
  imgBetweenRightTop.data = imgPath;
  imgBetweenRightTop.style.right = "25%";
  imgBetweenRightTop.style.top = "25%";
  imgBetweenRightTop.style.width = width;

  var imgBetweenLeftBottom = document.createElement('object');
  imgBetweenLeftBottom.classList.add("marker", "svg");
  imgBetweenLeftBottom.data = imgPath;
  imgBetweenLeftBottom.style.left = "25%";
  imgBetweenLeftBottom.style.bottom = "25%";
  imgBetweenLeftBottom.style.width = width;

  var imgBetweenRightBottom = document.createElement('object');
  imgBetweenRightBottom.classList.add("marker", "svg");
  imgBetweenRightBottom.data = imgPath;
  imgBetweenRightBottom.style.right = "25%";
  imgBetweenRightBottom.style.bottom = "25%";
  imgBetweenRightBottom.style.width = width;

  preview.append(imgBetweenLeftTop, imgBetweenRightTop, imgBetweenLeftBottom, imgBetweenRightBottom);
  
}