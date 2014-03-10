$(function() {

	$(".paccept").click(function() {
		var button = $(this);

		$.get("accept/"+button.attr("data-user")+"/", function(msg) {
			if(msg.successful) {
				$(".participants-table tbody").prepend(
					"<tr>" +
						"<td>" + msg.data.user__user__username + "</td>" +
						"<td>" + msg.data.age + "</td>" +
						"<td>" + msg.data.sex + "</td>" +
						"<td>" + msg.data.educationLevel + "</td>" +
						"<td>" + msg.data.firstLanguage + "</td>" +
						"<td>" + msg.data.country + "</td>" +
					"</tr>"
				);

				button.parents(".bid-row").remove();
			}
			else {
				alert("An error occurred, please try again.");
			}
		}, "json");
	});

	$(".preject").click(function () {
		var button = $(this);

		$.get("reject/"+button.attr("data-user")+"/", function(msg) {
			if(msg.successful)
				button.parents(".bid-row").remove();
			else
				alert("An error occurred, please try again.");
		}, "json");
	});

});