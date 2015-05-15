 $(function() {
 	$('.delete_comment').click(function(){
 		$.get('/delete/', {uuid: $(this).attr("id")});
 	});
 });