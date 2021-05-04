//colorpicker logic from https://dzone.com/articles/creating-your-own-html5

$(function(){
    var colorPreview = true;
    var canvas = document.getElementById('picker');
    var canvasPosition = canvas.getContext('2d');
    var image = new Image();
    image.onload = function () {
        canvasPosition.drawImage(image, 0, 0, image.width, image.height);
    }
    var imageSrc="../static/colorwheel3.png";
    image.src = imageSrc;
    $('#picker').mousemove(function(e) {
        if (colorPreview) {
            var canvasOffset = $(canvas).offset();
            var canvasX = Math.floor(e.pageX - canvasOffset.left);
            var canvasY = Math.floor(e.pageY - canvasOffset.top);
            var imageData = canvasPosition.getImageData(canvasX, canvasY, 1, 1);
            var pixel = imageData.data;
            var pixelColor = "rgb("+pixel[0]+", "+pixel[1]+", "+pixel[2]+")";
            $('.preview').css('backgroundColor', pixelColor);
            //send color to Flask route: https://www.codegrepper.com/code-examples/typescript/how+to+pass+js+data+to+flask+and+bac
            const URL = '/color_picker'
            const xhr = new XMLHttpRequest();
            rgbPackage = pixel[0]+", "+pixel[1]+", "+pixel[2]
            xhr.open("POST", URL);
            xhr.send(rgbPackage);
            $('#rVal').val(pixel[0]);
            $('#gVal').val(pixel[1]);
            $('#bVal').val(pixel[2]);
        }
    });
    $('#picker').click(function(e) {
        colorPreview = !colorPreview;
    });
    $('.preview').click(function(e) {
        $('.colorpicker').fadeToggle("slow", "linear");
        colorPreview = true;
    });
});
