$( document ).ready(function() {
 	// inflateOpinions();

 	console.log('hello world');
 	var state = $('.active').text();
 	$('.btn-toggle').click(function() {
 		console.log('clicked toggle');
 		state = $('.active').text();
 		console.log('clicked: state = ' + state);
 		if (state == 'Categorized')
 			categorized();
 		else
 			inflateOpinions();
 	});
 	if (state == 'Categorized')
 		categorized();
 	else
 		inflateOpinions();
 	$('.btn-toggle').click(function() {
 		console.log('clicked toggle');
 		state = $('.active').text();
 		console.log('clicked: state = ' + state);
 		if (state == 'Categorized')
 			categorized();
 		else
 			inflateOpinions();
 	});
 	function categorized() {
 		console.log('in categorized');
 		$('.jumbotron').html('');
 		$('.col-sm-4').html('Loading News ...');
 		$.getJSON('/loadAllNews/', function(data) {
 			var list = data.pages;
 		// var news = "";
 		// news += '<div class=opinionsPerNews></div>'
 		var News = '<ul>';
 		for (var i = 0; i < list.length; i++) {
 			var newsId = 'news-id = ' + list[i].hashid
 			//  + 'href=' + 'http://newsinshorts.com/news/'
 			News += '<li> <button ' + newsId + ' class="news-title btn btn-link" ' + '>' + list[i].title + '</button>' + '</li>';
 			// news += '<div class="news-opinions"' + newsId + '></div>'
 		}
 		News += '</ul>';
 		$('.col-sm-4').html(News);
 		$('.news-title').click(function() {
 			var news_id = $(this).attr('news-id');
 			var html = '<a href=' + 'http://newsinshorts.com/news/' + news_id + '>' + $(this).text() + '</a>';
 			html += '<button type="button" news-id="' + news_id + '" class="btn btn-primary approve-all">Approve All</button>';
 			html += '<button type="button" news-id="' + news_id + '" class="btn btn-danger reject-all">Reject All</button>';
 			var url = '/api/v1/opinions/?is_approved=none&news_id=' + news_id;
 			opinionsAsHTML(url, html);
 		});

 	});
}

});

function inflateOpinions()
{
	console.log('in inflateOpinions');
	$('.col-sm-4').html('');
	$('.col-sm-8').html('');
	$.get("/api/v1/opinions/?is_approved=none",{},function(data){
		inflateData(data);
	}).fail(function(){
		//showError("Server Error!! Try again.");
	});
}

function opinionsAsHTML(url, html) // takes a url, GETs opinions from there in JSON & returns HTML of opinions as a string
{
	$.get(url, {}, function(data){
		makeHTML(data, html)
	});
}

function makeHTML(data, html) {
	var opinions = data.objects;
	for(var i = 0; i < opinions.length; i++) {
		html += '<div class="opinion-box">';
		html += '<div class="opinion">' + opinions[i].text + '</div>';
		html += '<button type="button" opinion-id="' + opinions[i].id + '" class="btn btn-primary approve">Approve</button>';
		html += '<button type="button" opinion-id="' + opinions[i].id + '"  class="btn btn-danger reject">Reject</button>';
		html += '</div>';
	}
	$('.col-sm-8').html(html);
	addClickProperties();
}

function inflateData(data)
{
	var opinions = data.objects;
	var html = "";
	for(var i = 0; i < opinions.length; i++)
	{	
		html += '<p>';
		html += '<a class="news-title" href="' + 'http://newsinshorts.com/news/' + opinions[i].news_id + '">' + opinions[i].news_id + '</a>';
		html += '<div class="opinion">' + opinions[i].text + '</div>';
		html += '<button type="button" opinion-id="' + opinions[i].id + '" class="btn btn-primary approve">Approve</button>';
		html += '<button type="button" opinion-id="' + opinions[i].id + '"  class="btn btn-danger reject">Reject</button>';
		html += '</p>';
	}

	$(".jumbotron").html(html);
	addClickProperties();
}

function addClickProperties()
{
	$(".approve").click(function(){
 		$.get('approve/', {flag: 1, id: $(this).attr("opinion-id")});
 		$(this).text('Approved!');
 	});
 	$(".reject").click(function(){
 		$.get('approve/', {flag: 0, id: $(this).attr("opinion-id")});
 		$(this).text('Rejected!');
 	});
 	$(".approve-all").click(function(){
 		$.get('allApprove/', {flag: 1, 'news-id': $(this).attr("news-id")});
 		$(this).text('All Approved!');
 	});
 	$(".reject-all").click(function(){
 		$.get('allApprove/', {flag: 0, 'news-id': $(this).attr("news-id")});
 		$(this).text('All Rejected!');
 	});
 	$('.news-title').on('click', function() {
 		$('body').scrollTop(0);
 	});
}

