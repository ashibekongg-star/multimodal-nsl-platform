document.addEventListener("DOMContentLoaded", function () {

    // ===========================
    // Speech Recognition
    // ===========================

    const startBtn = document.getElementById("startBtn");
    const speechText = document.getElementById("speechText");
    const speechForm = document.getElementById("speechForm");
    const statusBox = document.getElementById("statusBox");

    if (
        !("webkitSpeechRecognition" in window) &&
        !("SpeechRecognition" in window)
    ) {

        statusBox.innerHTML =
            "<div class='alert alert-danger'>Speech Recognition is not supported in this browser.</div>";

        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    startBtn.addEventListener("click", function () {

        statusBox.innerHTML = `
            <div class="text-center">
                <h5 class="text-danger">🎤 Listening...</h5>
                <p>Please speak now.</p>
            </div>
        `;

        recognition.start();

    });

    recognition.onresult = function (event) {

        const transcript = event.results[0][0].transcript;

        speechText.value = transcript;

        statusBox.innerHTML = `
            <div class="text-center">
                <h5 class="text-success">
                    ✓ Speech Recognized
                </h5>
            </div>
        `;

        speechForm.submit();

    };

    recognition.onerror = function (event) {

        let message = event.error;

        switch (event.error) {

            case "no-speech":
                message = "No speech detected.";
                break;

            case "audio-capture":
                message = "No microphone found.";
                break;

            case "not-allowed":
                message = "Microphone permission denied.";
                break;

            case "network":
                message = "Network error.";
                break;
        }

        statusBox.innerHTML =
            `<div class="alert alert-danger">${message}</div>`;
    };

    // ====================================
    // Sequential Video Playback
    // ====================================

    if (
        typeof videoQueue !== "undefined" &&
        Array.isArray(videoQueue) &&
        videoQueue.length > 0
    ) {

        console.log("Video Queue:", videoQueue);

        const video = document.getElementById("translatorVideo");

        let currentVideo = 0;

        function playCurrentVideo() {

            if (currentVideo >= videoQueue.length) {

                console.log("Translation finished.");

                statusBox.innerHTML = `
                    <div class="alert alert-success">
                        Translation Completed
                    </div>
                `;

                return;
            }

            console.log("Playing:", videoQueue[currentVideo]);

            // Stop current video
            video.pause();

            // Remove old source completely
            video.removeAttribute("src");

            // Force browser to reload new video
            video.src =
                videoQueue[currentVideo] +
                "?t=" +
                new Date().getTime();

            video.load();

            video.onloadeddata = function () {

                video.play()
                    .then(() => {

                        console.log(
                            "Now playing:",
                            video.currentSrc
                        );

                    })
                    .catch(err => {

                        console.log("Play error:", err);

                    });

            };

        }

        video.onended = function () {

            console.log(
                "Finished video:",
                currentVideo + 1
            );

            currentVideo++;

            setTimeout(function () {

                playCurrentVideo();

            }, 300);

        };

        playCurrentVideo();

    }

});