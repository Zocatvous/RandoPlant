/* Move the image element horizontally */
var container = document.getElementById("container");
var image = document.getElementById("image");
var left = 0;
var speed = 1;
function update() {
    left -= speed;
    if (left < -image.width) {
        left = container.offsetWidth;
    }
    image.style.left = left + "px";
    requestAnimationFrame(update);
}
update();