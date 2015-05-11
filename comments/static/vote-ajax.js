 $(function() {
 $('.upvote').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
     $.get('/like_category/', {category_id: catid, id: $(this).attr("id")}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
           });
});
});