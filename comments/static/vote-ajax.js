 $(function() {
 $('.upvote').click(function(){
    // var catid;
    // catid = $(this).attr("data-catid");
     $.get('/vote/', {vote: 1, id: $(this).attr("id")}, function(data){
               // $('#like_count').html(data);
               // $('#likes').hide();
           });
});
});