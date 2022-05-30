


  const element = document.getElementById("testMethode");
element.addEventListener("click", myFunction);

function myFunction() {
    console.log("Test");
  document.getElementById("demo").innerHTML = "Hello World";
  var text = "HTobi Stinkt!";

cordova.plugins.clipboard.copy(text);
}