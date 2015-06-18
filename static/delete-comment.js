 $(function() {
 	$('.delete_comment').click(function(){
 		$.get('/delete/', {uuid: $(this).attr("comment-id")});
 	});
 });