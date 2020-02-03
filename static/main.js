// Create a new color picker instance
// https://iro.js.org/guide.html#getting-started
var colorPicker = new iro.ColorPicker('#color-picker-container', {
  width: 380,
  color: "rgb(255, 0, 0)",
  borderWidth: 1,
  borderColor: "#fff",
});

var color_swatch = document.getElementById("color_swatch");

colorPicker.on(["color:init", "color:change"], function(color){
  // Show the current color in different formats
  // Using the selected color: https://iro.js.org/guide.html#selected-color-api
  color_swatch.style.backgroundColor = color.hexString;
  //console.log(color.hexString);
});

function setPeriod() {
  var x = document.getElementById("period_time").value;

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("status").innerHTML = this.responseText;
    }
  };
  xhttp.open("POST", "/send_req", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(JSON.stringify({'period': x}));
}

function playGradient(gradient) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("status").innerHTML = this.responseText;
    }
  };
  document.getElementById("status").innerHTML = "Set gradient to "+gradient+" gradient"
  xhttp.open("POST", "/send_req", true);
  xhttp.setRequestHeader("Content-type", "application/json");

  if(gradient == 'fade_colour'){
    xhttp.send(JSON.stringify({'gradient' : colorPicker.color.hexString}));
  } else {
    xhttp.send(JSON.stringify({'gradient' : gradient}));
  }
}

function sendHSVData() {
  var xhttp = new XMLHttpRequest();
  //xhttp.onreadystatechange = function() {
  //  if (this.readyState == 4 && this.status == 200) {
  //    document.getElementById("status").innerHTML = this.responseText;
  //  }
  //};

  xhttp.open("POST", "/send_req", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(JSON.stringify({"colour":colorPicker.color.hexString}));
}
