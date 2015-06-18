 $(function() {
 	$('.edit_comment').click(function(){
 		var edit_id = $(this).attr('data-id');
 		var id = edit_id.split("_")[1];
 		var selector = '#add_comment_' + id;
 		console.log("selector is ", selector);
 		$("#textarea_"+id).show();
 		$("#comment_"+id).hide();
 		$(this).text("Submit");
 		$(this).click(function(){
 			var content = $("#textarea_"+id).val();
 			$("#comment_" + id).text(content);
 			$("#comment_"+id).show();
 			$("#textarea_"+id).hide();
 			$.get("/edit-comment/",{id: id, content: content});
 		});
 		// $("#edit-"+id).text("Submit");
 		// console.log(selector);
 		// console.log($(selector));
 		// var content = $($(selector)[0]).children('.content')[0];
 		// $(selector).remove();
 		// console.log("content is ", content);
 		// $.post('/edit-comment/', )
 	});
 });