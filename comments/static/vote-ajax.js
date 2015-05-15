 $(function() {
 	$('.upvote').click(function(){
 		$.get('/vote/', {vote: 1, id: $(this).attr("id")});
 	});
 	$('.downvote').click(function(){
 		$.get('/vote/', {vote: -1, id: $(this).attr("id")});
 	});
 });