home_prefix = 'http://cs-sys-1.uis.georgetown.edu/~jw1498/Memex_Search_Interface/';

$(document).ready(function() {
    //parent.logCurrentPage(location);
    $("#displayList li").click(function () {
	todoc = $(this).text();
    location = home_prefix + domain_url.replace('search','check') + "?e=" + todoc;
    /* commented for log
	$.ajax({
	    method: "post",
	    url: "http://infosense.cs.georgetown.edu/annotation/otherlog.cgi",
	    data:{
		username: location.href.slice(location.href.indexOf('username')+9, location.href.length),
		type: location.href.slice(location.href.indexOf('type')+5,location.href.indexOf('topic_id')-1),
		topic_id: location.href.slice(location.href.indexOf('topic_id')+9, location.href.indexOf('domain_id')-1),
		docno: todoc,
		flag: 'click'	
	    },
	    complete: function(){
		location = domain_url.replace('search','check') + "?e=" + todoc;
	    }
	    });
    
    */
    });
});
