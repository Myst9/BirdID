var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

var imagePreview = document.getElementById("image-preview");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");

function getMimeType(src) {
  // Get the MIME type of the image based on its extension
  var extension = src.substring(src.lastIndexOf('.') + 1).toLowerCase();
  switch (extension) {
    case 'png':
      return 'image/png';
    case 'gif':
      return 'image/gif';
    case 'jpeg':
    case 'jpg':
      return 'image/jpeg';
    default:
      return 'image/jpeg'; // default to JPEG
  }
}

function submitImage() {
  //Submit Image
  console.log("Submit");

  if (!imagePreview.src) {
    window.alert("Please select an image before submit.");
    return;
  }

  loader.classList.remove("hidden");
  
  var canvas = document.createElement('canvas');
  var ctx = canvas.getContext('2d');
  var image = new Image();
  image.src = imagePreview.src;
  image.onload = function() {
    canvas.width = image.width;
    canvas.height = image.height;
    ctx.drawImage(image, 0, 0);
    var base64Image = canvas.toDataURL(getMimeType(imagePreview.src));
    
    predictImage(base64Image);
  };
}

function clearImage() {
  //Clear Image
  console.log("Clear")

  fileSelect.value = "";
  imagePreview.src = "";
  predResult.innerHTML = "";

  hide(imagePreview);
  hide(loader);
  hide(predResult);
  show(uploadCaption);
}

function previewFile(file) {
  // Show preview of the uploaded image
  console.log(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);
    show(imagePreview);
    hide(uploadCaption);
    predResult.innerHTML = "";
  };
}

function predictImage(image) {
  // Send HTTP POST request to make prediction
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error occured.", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function displayResult(data) {
  // display the prediction result
  hide(loader);
  predResult.innerHTML = data.result;
  show(predResult);
}

function hide(element) {
  // hide an element
  element.classList.add("hidden");
}

function show(element) {
  // show an element
  element.classList.remove("hidden");
}