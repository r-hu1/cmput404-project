$("#post-image").

$("form").submit(function(event) {
  event.preventDefault();
  var imageFile =
});

// http://stackoverflow.com/questions/34972072/how-to-send-image-to-server-with-http-post-in-javascript-and-store-base64-in-mon
// 11/01/2016

// converts an image to Base64 encoding for sending in http request
function convertToBase64(url, imagetype, callback) {

    var img = document.createElement('IMG'),
        canvas = document.createElement('CANVAS'),
        ctx = canvas.getContext('2d'),
        data = "";

    img.crossOrigin = 'Anonymous'

    // Because image loading is asynchronous, we define an event listening function that will be called when the image has been loaded
    img.onLoad = function() {
        // When the image is loaded, this function is called with the image object as its context or 'this' value
        canvas.height = this.height;
        canvas.width = this.width;
        ctx.drawImage(this, 0, 0);
        data = canvas.toDataURL(imagetype);
        callback(data);
    };

    // We set the source of the image tag to start loading its data. We define
    // the event listener first, so that if the image has already been loaded
    // on the page or is cached the event listener will still fire

    img.src = url;
}

// Here we define the function that will send the request to the server.
// It will accept the image name, and the base64 data as arguments
var sendBase64ToServer = function(name, base64){
    var httpPost = new XMLHttpRequest(),
        path = "http://127.0.0.1:8000/uploadImage/" + name,
        data = JSON.stringify({image: base64});
    httpPost.onreadystatechange = function(err) {
            if (httpPost.readyState == 4 && httpPost.status == 200){
                console.log(httpPost.responseText);
            } else {
                console.log(err);
            }
        };
    // Set the content type of the request to json since that's what's being sent
    httpPost.setHeader('Content-Type', 'application/json');
    httpPost.open("POST", path, true);
    httpPost.send(data);
};

// This wrapper function will accept the name of the image, the url, and the
// image type and perform the request

var uploadImage = function(src, name, type){
    convertToBase64(src, type, function(data){
        sendBase64ToServer(name, data);
    });
};

uploadImage(imgsrc, name, 'image/jpeg');
var postForm = document.getElementById("post-form"),
    data = [],
    JSONobj = {
      "title":postForm.elements["title"].value,
      "description":postForm.elements["desc"].value,
      "contentType":postForm.elements["text-type"].value;



}
