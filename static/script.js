
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}


// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}


    var src = document.getElementById("file").onchange = function (e) {
    var image = e.target.files[0];
    window.loadImage(image, function (img) {
        if (img.type === "error") {
            console.log("couldn't load image:", img);
        } else {
            window.EXIF.getData(image, function () {
                console.log("done!");
                var orientation = window.EXIF.getTag(this, "Orientation");
                var canvas = window.loadImage.scale(img, {orientation: orientation || 0, canvas: true});
                $("#image").attr("src",canvas.toDataURL());
            });
        }
    });
  };


    var src = document.getElementById("receipt").onload = function (e) {
    var image = e.target.files[0];
    window.loadImage(image, function (img) {
        if (img.type === "error") {
            console.log("couldn't load image:", img);
        } else {
            window.EXIF.getData(image, function () {
                console.log("done!");
                var orientation = window.EXIF.getTag(this, "Orientation");
                var canvas = window.loadImage.scale(img, {orientation: orientation || 0, canvas: true});
                $("#image").attr("src",canvas.toDataURL());
            });
        }
    });
  };
