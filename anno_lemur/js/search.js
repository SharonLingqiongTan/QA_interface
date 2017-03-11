function lockscreen(){
    $screen_lock = $("<div class='screen-cover'></div>");
    $screen_lock.css({
        "position" : "absolute",
        "z-index" : 10000,
        "background-color" : "#000",
        "opacity" : 0.15,
        "cursor": "wait"
    });
    $screen_lock.width($("body", parent.document).width());
    $screen_lock.height($("body", parent.document).height());
    $screen_lock.prependTo($("body", parent.document));
}

function logSnippet(){
    /*
    list = new Array();
    $("ol li").each(function(){
        list.push([$("a", this).eq(0).text(), $(this).text().replace(/^.*\n/,'')]);
    });
    if (list.length<=1){
        return;
    }
    jsonlist = JSON.stringify(list);*/
    $.ajax({
        method: "post",
        url: parent.home_prefix + "otherlog.cgi",
        data:{
            topic_id: parent.tid,
            flag: 'list'
        },
    });
    parent.search_signal = 0;
};

function fillSearchMode(){
    var smode;
    switch (parent.mode){
        case 'G':
            smode = 'Pink find more';
            break;
        case 'N':
            smode = 'Blue find more';
            break;
        case 'L':
            smode = 'Lemur';
            break;
        case 'S':
            smode = 'Solr';
            break;
        case 'T':
            smode = 'Terrier';
    }
    $("#search_mode_display").html(smode);
}

$(document).ready(function(){
    $(".screen-cover", parent.document).remove();
    $("#control_panel_2", parent.document).hide();
    //$("#highlight input", parent.document).val("");

    $("#result_page a").attr("href", function(){
        return $(this).attr("href").split("?").join("?T="+parent.tid+"&")}
    );

    //fillSearchMode();
    parent.getCount();

    $("#result_page a").click(function(e){
        e.preventDefault();
        parent.para = $(this).attr("href").split("?")[1];
        lockscreen();
        location.href = $(this).attr("href");
        }
    );

    $("ol a").click(function(e){
        e.preventDefault();
        parent.doc_id = $(this).html();
        parent.level = 'D';
        start = parseInt($("ol").attr("start"));
        lockscreen();
        $.ajax({
            method: "get",
            url: parent.home_prefix + "otherlog.cgi",
            data:{
                source: parent.mode,
                flag: 'click',
                topic_id: parent.tid,
                docno: parent.doc_id
            },
            complete: function(){
                $(".screen-cover", parent.document).remove();
                $("#control_panel_2", parent.document).show();
                location.href = './lemur.cgi?e=' + parent.doc_id;
            }
        })
    });

    $.ajax({
        method: "get",
        url: parent.home_prefix + "getNumOfTagged.cgi",
        data:{
            topic_id: parent.tid
        },
        success: function(response){
            $("#numoftagged").html(response);
        }
    });

    if (parent.search_signal==1) {logSnippet();}
});
