Dropzone.autoDiscover = false;
var btn = document.getElementById("btn-listen");
var btnTranscribe = document.getElementById("btn-transcribe");
var trans = document.getElementById("transcription");
var transH = document.getElementById("transcription-hidden");
var lang = $("#lang").text();
var filePath = $("#file-path").text();
var $spinner = $("#spinner");

// on lcik of listen
// Disabling autoDiscover, otherwise Dropzone will try to attach twice.
// or disable for specific dropzone:
// Dropzone.options.myDropzone = false;

// Now that the DOM is fully loaded, create the dropzone, and setup the
// event listeners
//   myDropzone.on("addedfile", function(file) {

$(function() {
	$spinner.hide();
	btn.addEventListener("click", function(e) {
		$spinner.show();
		$.ajax({
			url: "/listen",
			data: { lang: lang }
		}).done(function(data) {
			trans.innerText = data;
			if (lang.split("-")[0] == "en") {
				get_sentiment(data, "en");
			}
			$spinner.hide();
		});
	});

	btnTranscribe.addEventListener("click", function(e) {
		trans.innerText = "Wait...";
		$.ajax({
			url: "/transcribe",
			data: { lang: lang }
		}).done(function(res) {
			data = processResp(res["result"]);
			trans.innerHTML = data["html"];
			transH.innerText = data["plainText"];
			if (lang.split("-")[0] == "en") {
				get_sentiment(data["plainText"]);
				updateProgBars();
			}
		});
	});
});

function processResp(res) {
	let sentences = "";
	let plainSentences = "";
	for (let i = 0; i < res.length; i++) {
		let sentence = "";
		let plainSentence = "";
		let words = res[i]["words"];
		for (let j = 0; j < words.length; j++) {
			let obj = words[j];
			let word = obj.word;
			let speaker = obj.speakerTag;
			let text = `<span class="trans-speaker-${speaker}" data-speaker="${speaker}" data-toggle="tooltip" data-placement="top" title="Speaker-${speaker}"> ${word} </span>`;
			sentence += text;
			plainSentence += word + " ";
		}
		sentences += sentence;
		plainSentences += plainSentence;
	}
	return { html: sentences, plainText: plainSentences };
}

function get_sentiment(text, lang = "en") {
	$.post(
		"/sentiment",
		{
			inputText: text,
			inputLanguage: lang
		},
		function(data) {
			let textHtml = "";
			let $progBar = $("#prog-bar");
			for (let i = 0; i < data["sentences"].length; i++) {
				let t = data["sentences"][i]["text"]["content"];
				let c = "";
				let score = data["sentences"][i]["sentiment"]["score"];
				let magnitude = data["sentences"][i]["sentiment"]["magnitude"];
				if (score < -0.15) {
					c = "text-danger";
				} else if (score > 0.15) {
					c = "text-success";
				}
				if (t.length) {
					textHtml += `<span class="${c}" data-toggle="tooltip" data-placement="top" title="Score: ${score}, Magnitude: ${magnitude}"> ${t}. </span>`;
				}
			}
			// append the html
			$("#sentiment-text").html(textHtml);
		}
	);
}

function updateProgBars() {
	var speaker1Text = getSpeakerText("1");
	var speaker2Text = getSpeakerText("2");
	updateProgBar($("#prog-bar-1"), speaker1Text);
	updateProgBar($("#prog-bar-2"), speaker2Text);
}

function getSpeakerText(speaker) {
	var span = $(".trans-speaker-" + speaker);
	var text = "";
	var textArr = span.map((currentValue, index, arr) => {
		text += span[currentValue].innerText;
		return span[currentValue].innerText;
	});
	return text;
}

function updateProgBar($progBar, text) {
	$.post(
		"/sentiment",
		{
			inputText: text,
			inputLanguage: lang
		},
		function(data) {
			let documentScore = data["documentSentiment"]["score"];
			if (documentScore > 0) {
				$progBar.removeClass("bg-danger").addClass("bg-success");
			} else if (documentScore < 0) {
				$progBar.removeClass("bg-success").addClass("bg-danger");
			}
			$progBar.css({
				width: `${Math.abs(documentScore) * 100}%`
			});
			$("#prog-val").text(documentScore);
		}
	);
}
