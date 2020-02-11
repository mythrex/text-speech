$(function() {
	// on lcik of listen
	$("#btn-listen").click(event => {
		$.ajax({
			url: "/listen"
		}).done(function(data) {
			console.log(data);
		});
	});
});
