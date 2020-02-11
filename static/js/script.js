$(function() {
	var btn = document.getElementById("btn-listen");
	var cvs = document.getElementById("cvs");
	var ctx = cvs.getContext("2d");

	var bell = new WaveBell();

	// on lcik of listen

	btn.addEventListener("click", function(e) {
		bell.start(1000 / 25);
		$.ajax({
			url: "/listen"
		}).done(function(data) {
			console.log(data);
			bell.stop();
		});
	});

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
		btn.innerText = "Stop";
	});
	bell.on("stop", function() {
		btn.innerText = "Start";
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
		ctx.strokeStyle = "#6c4";
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
});
