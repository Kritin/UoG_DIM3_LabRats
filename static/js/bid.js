$(function() {

	$(".bidbtn").click(function() {

		var btn = $(this);
		var eid = btn.attr("data-exp");

		$.get("/labRatsApp/bid/" + eid + "/", function(data) {

			alert(data.msg);
			if(data.successful)
				btn.hide();

		}, "json");

	});

});