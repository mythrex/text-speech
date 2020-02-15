Dropzone.autoDiscover = false;
var btn = document.getElementById("btn-listen");
var btnTranscribe = document.getElementById("btn-transcribe");
var cvs = document.getElementById("cvs");
var ctx = cvs.getContext("2d");
var trans = document.getElementById("transcription");
var bell = new WaveBell();
var lang = $("#lang").text();
var filePath = $("#file-path").text();

// on lcik of listen
// Disabling autoDiscover, otherwise Dropzone will try to attach twice.
// or disable for specific dropzone:
// Dropzone.options.myDropzone = false;

// Now that the DOM is fully loaded, create the dropzone, and setup the
// event listeners
//   myDropzone.on("addedfile", function(file) {

$(function() {
	btn.addEventListener("click", function(e) {
		bell.start(1000 / 25);
		$.ajax({
			url: "/listen",
			data: { lang: lang }
		}).done(function(data) {
			trans.innerText = data;
			if (lang.split("-")[0] == "en") {
				get_sentiment(data, "en");
			}
			bell.stop();
		});
	});

	btnTranscribe.addEventListener("click", function(e) {
		trans.innerText = "Wait...";
		$.ajax({
			url: "/transcribe",
			data: { lang: lang }
		}).done(function(data) {
			trans.innerText = data;
			if (lang.split("-")[0] == "en") {
				get_sentiment(data, "en");
			}
		});
	});
});

function get_sentiment(text, lang = "en") {
	$.post(
		"/sentiment",
		{
			inputText: text,
			inputLanguage: lang
		},
		function(data) {
			var data = {
				documents: [{ id: "1", score: 0.7847611904144287 }]
			};
			let scores = [];
			for (let i = 0; i < data["documents"].length; i++) {
				let sentence = data["documents"][i];
				scores.push((parseFloat(sentence["score"]) * 100).toFixed(2));
			}

			let text = trans.innerText;
			let textArr = text.split(".");
			let textHtml = "";
			for (let i = 0; i < textArr.length; i++) {
				let t = textArr[i];
				let c = "";
				if (scores[i] < 0.35) {
					c = "text-danger";
				} else if (scores[i] > 0.7) {
					c = "text-success";
				}
				if (t.length) {
					textHtml += `<span class="${c}" data-toggle="tooltip" data-placement="top" title="Score: ${scores[i]}"> ${t}. </span>`;
				}
			}
			console.log(textArr, textHtml);
			console.log($("#sentiment-text"));
			$("#sentiment-text").html(textHtml);

			let percent =
				scores.reduce((total, num) => {
					return total + num;
				}, 0) / scores.length;

			$("#prog-bar").css({
				width: `${percent}%`
			});
			$("#prog-val").text(percent);
		}
	);
}

window.addEventListener("load", function(e) {
	// start animation on loaded
	animate();
});

var currentValue = 0;

// buffered wave data
var BUF_SIZE = 500;
var buffer = new Array(BUF_SIZE).fill(0);
var cursor = 0;

bell.on("wave", function(e) {
	// update current wave value
	currentValue = e.value;
});

bell.on("start", function() {
	btn.innerHTML = '<i class="fa fa-pause"></i>';
	btn.setAttribute("disabled", true);
});
bell.on("stop", function() {
	btn.innerHTML = '<i class="fa fa-play"></i>';
	btn.removeAttribute("disabled");
	currentValue = 0;
});

function updateBuffer() {
	// loop update buffered data
	buffer[cursor++ % BUF_SIZE] = currentValue;
}

function drawFrame() {
	ctx.save();
	// empty canvas
	ctx.clearRect(0, 0, 500, 300);
	// draw audio waveform
	ctx.strokeStyle = "#f96332";
	for (var i = 0; i < BUF_SIZE; i++) {
		var h = 250 * buffer[(cursor + i) % BUF_SIZE];
		var x = i;
		ctx.beginPath();
		ctx.moveTo(x, 150.5 - 0.5 * h);
		ctx.lineTo(x, 150.5 + 0.5 * h);
		ctx.stroke();
	}
	// draw middle line
	ctx.beginPath();
	ctx.moveTo(0, 150.5);
	ctx.lineTo(500, 150.5);
	ctx.strokeStyle = "#000";
	ctx.stroke();
	ctx.restore();
}

function animate() {
	requestAnimationFrame(animate);
	// update wave data
	updateBuffer();
	// draw next frame
	drawFrame();
}
