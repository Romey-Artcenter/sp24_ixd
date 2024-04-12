let vid1, vid2;
let currentVideo, nextVideo;
let pressure = 5000;
let distance = 300; 
let fade = 0; 
let isTransitioning = false;
let volumeTransitionSpeed = 0.05;
let currentVolume = 0;
let nextVolume = 0;

function setup() {
    createCanvas(windowWidth, windowHeight);
    vid1 = createVideo("video1.mp4");
    vid2 = createVideo("video2.mp4");

    vid1.size(windowWidth, windowHeight);
    vid2.size(windowWidth, windowHeight);

    vid1.hide();
    vid2.hide();

    currentVideo = vid1; 
    nextVideo = null;

    vid1.volume(0);
    vid2.volume(0);

    vid1.loop();
    vid2.loop();
}

function draw() {
    background(0);

    let newVideo = (pressure > 4000) ? vid1 : vid2;
    if (newVideo !== currentVideo && !isTransitioning) {
        nextVideo = newVideo;
        isTransitioning = true;
        nextVideo.time(0);
        nextVolume = 0;
    }

    if (isTransitioning) {
        fade += 2;
        currentVolume = max(0, currentVolume - volumeTransitionSpeed);
        nextVolume = min(1, nextVolume + volumeTransitionSpeed);

        if (fade >= 255) {
            fade = 0;
            currentVideo.hide();
            currentVideo = nextVideo;
            nextVideo = null;
            isTransitioning = false;
            currentVolume = nextVolume;
            nextVolume = 0;
        }
    } else {
        if (distance >= 100) {
            currentVolume = 0;
        } else if (distance <= 50) {
            currentVolume = 1;
        } else {
            currentVolume = map(distance, 50, 100, 1, 0);
        }
    }

    currentVideo.volume(currentVolume);
    if (nextVideo) nextVideo.volume(nextVolume);

    tint(255, 255 - fade);
    image(currentVideo, 0, 0, windowWidth, windowHeight);
    if (nextVideo) {
        tint(255, fade);
        image(nextVideo, 0, 0, windowWidth, windowHeight);
    }
}

function updateSensorData(dataString) {
    let data = dataString.split(',');
    if (data.length >= 2) {
        if (data[0] === "Distance invalid") {
            distance = 50;
        } else {
            distance = parseInt(data[0]);
        }
        pressure = parseInt(data[1]);
    }
}
