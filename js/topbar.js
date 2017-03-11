home_prefix = 'http://cs-sys-1.uis.georgetown.edu/~jw1498/Memex_Search_Interface/';

function getCount(){
    $.ajax({
        url: "countHandler.cgi",
        data:{
            topic_id: tid
        },
        success: function(response){
            $("#total_count").html(response);
        }
    })
}

function lockscreen(){
    $screen_lock = $("<div class='screen-cover'></div>");
    $screen_lock.css({
        "position" : "absolute",
        "z-index" : 10000,
        "background-color" : "#000",
        "opacity" : 0.15,
        "cursor": "wait"
    });
    $screen_lock.width($("body").width());
    $screen_lock.height($("body").height());
    $screen_lock.prependTo($("body"));
}

function moodFeedback(m){
    r = window.prompt("Are you " +m +" at this moment? It is about which document/query/subtopic? What do you want to search? Tell us why:");
    if (r != null){
        $.ajax({
            method: "post",
            url: "./moodFeedback.cgi",
            data:{
                mood: m,
                reason: r,
                topic_id: tid,
                source: mode
            }
        })
    }   
}

function runQuery(){
    //mode = $(this).val();
    //if ($(this).html() == "lemur"){
    //    url = dict["domains"][1];
    //}
    //else{
	    //url = dict["domains"][1].replace("search","solr");
    //    url = dict["domains"][1].replace('search', $(this).html());
    //}
    mode = "T"
    url = dict["domains"][1].replace('search',"elasticsearch")
    level = 'L';
    para = "T=" + tid + "&q=" + encodeURIComponent($("#querybox").val());
    //thequery = $("#querybox").val();
    thequery = $("#querybox").val();
    search_signal = 1;
    // ?? set mode or level ??
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");

    lockscreen();

    $("#lemurbox").attr("src", home_prefix + url + "?" + para);

    $.ajax({
        method: "post",
        url: home_prefix + "otherlog.cgi",
        data:{
            source: mode,
            topic_id: tid,
            query: thequery,
            flag: 'query'
        }
    })
    
    // if parent.tname == '' #lemurdiscard.hide()
}

function phoneSearch(){
    mode = "T";
    para = "T=" + tid + "&q=" + "" + encodeURIComponent("phone:"+$("#phoneInput").val()+";");
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);
}

function emailSearch() {
    mode = "T";
    query = "email:"+$("#emailInput").val()+";"
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);	

}

function nameSearch() {
    mode = "T";
    query = "name:"+$("#nameInput").val()+";"
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);
}

function socialMediaSearch() {
    mode = "T";
    query = "";
    if ($("#socialMediaInput").val())  {
        query += "socialMedia:"+$("#socialMediaInput").val()+";";
    }
    if ($("#socialMediaIDInput").val())  {
        query += "socialMediaID:"+$("#socialMediaIDInput").val()+";";
    }
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);
}

function reviewSiteSearch() {
    mode = "T";
    query = ""
    if ($("#reviewSiteInput").val())  {
        query += "reviewSite:"+$("#reviewSiteInput").val()+";";
    }
    if ($("#reviewSiteIDInput").val())  {
        query += "reviewSiteID:"+$("#reviewSiteIDInput").val()+";";
    }
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);
}

function startnewSearch() {
    mode = "T";
    phone = $("#phoneInput").val()
    if (phone.length>=9) {
    	query = phone.substr(0,3)+" "+phone.substr(3,6)+" "+phone.substr(6)+$("#emailInput").val();
    }
    else {
	query = phone + $("#emailInput").val();
    }
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);               
    }                 

function refineSearch(age,height) {
    mode = "T";
    query = ""
    if ($("#phoneInput").val()) {
        query += "phone:"+$("#phoneInput").val()+";";
    }
    if ($("#emailInput").val()) {
        query += "email:"+$("#emailInput").val()+";";
    }
    //if ($( "#ageSlider" ).slider( "values", 0 ) != 20 && $( "#ageSlider" ).slider( "values", 1) != 40) {
    //    query += "age:"+$( "#ageSlider" ).slider( "values", 0 )+$( "#ageSlider" ).slider( "values", 1 )+";";
    //}
    if (age == 1) {
	query += "age:"+$( "#ageSlider" ).slider( "values", 0 )+$( "#ageSlider" ).slider( "values", 1 )+";";
    }
    if (height== 1) {
	query += "height:"+$( "#heightSlider" ).slider( "values", 0 )+$( "#heightSlider" ).slider( "values", 1 )+";";
    }
    if ($("#nameInput").val()) {
        query += "name:"+$("#nameInput").val()+";";
    }
    if ($("#stateInput").val()) {
        query += "state:"+$("#stateInput").val()+";";
    }
    if ($("#cityInput").val())  {
        query += "city:"+$("#cityInput").val()+";";
    }
    if ($("#whiteHairBox").is(":checked"))  {
        query += "hairColor:"+$("#whiteHairBox").val()+";";
    }
    if ($("#blackHairBox").is(":checked"))  {
        query += "hairColor:"+$("#blackHairBox").val()+";";
    }
    if ($("#brownHairBox").is(":checked"))  {
        query += "hairColor:"+$("#brownHairBox").val()+";";
    }
    if ($("#blondeHairBox").is(":checked"))  {
        query += "hairColor:"+$("#blondeHairBox").val()+";";
    }
    if ($("#redHairBox").is(":checked"))  {
        query += "hairColor:"+$("#redHairBox").val()+";";
    }
    if ($("#blueHairBox").is(":checked"))  {
        query += "hairColor:"+$("#blueHairBox").val()+";";
    }
    if ($("#brownEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#brownEyeBox").val()+";";
    }
    if ($("#blackEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#blackEyeBox").val()+";";
    }
    if ($("#blueEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#blueEyeBox").val()+";";
    }
    if ($("#amberEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#amberEyeBox").val()+";";
    }
    if ($("#greyEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#greyEyeBox").val()+";";
    }
    if ($("#greenEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#greenEyeBox").val()+";";
    }
    if ($("#ethnicityInput").val()) {
	query += "ethnicity:"+$("#ethnicityInput").val()+";"
    }
    if ($("#nationalityInput").val())  {
        query += "nationality:"+$("#nationalityInput").val()+";";
    }
    if ($("#socialMediaInput").val())  {
        query += "socialMedia:"+$("#socialMediaInput").val()+";";
    }
    if ($("#socialMediaIDInput").val())  {
        query += "socialMediaID:"+$("#socialMediaIDInput").val()+";";
    }
    if ($("#reviewSiteInput").val())  {
        query += "reviewSite:"+$("#reviewSiteInput").val()+";";
    }
    if ($("#reviewSiteIDInput").val())  {
        query += "reviewSiteID:"+$("#reviewSiteIDInput").val()+";";
    }
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    url = dict["domains"][1].replace('search',"elasticsearch");
    search_signal = 1;
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);

}

function move(opnum){
    if ((opnum == 'd' || opnum =='r')&& tname ==''){
        alertdialog(1);
        return;
    }
    if (opnum == 'd' || opnum =='r') {lockscreen();}
    $.ajax({
            method: "post",
            url: "http://cs-sys-1.uis.georgetown.edu/~jw1498/Memex_Search_Interface/moveHandler.cgi",
	    data: {
                topic_id: tid,
                docno: doc_id, // ?? make sure set doc_id ??
                signal: opnum,
            },
            success: function(response){
                response = response.trim();
                if (response == "-1"){
                    $(".screen-cover").remove();
                    if (opnum == 'r') alertdialog(11);
                    if (opnum == 'd') alertdialog(13);
                }
                else if (response == "0"){
                    goback();
                }
                else{
                    doc_id = response.trim();
                    $("#lemurbox").attr("src", home_prefix+url+'?e='+response)
                }
            }
            // what about 0 response ??
        });
};

function switchDoc(op) {
    if (op != "p" &&  op != "n") {
        alertdialog(1);
        return;
    }
    $.ajax({
        method: "post",
        url: "http://cs-sys-1.uis.georgetown.edu/~jw1498/Memex_Search_Interface/switchDocHandler.cgi",
	    data: {
                topic_id: tid,
                docno: doc_id, // ?? make sure set doc_id ??
                signal: op,
            },
            success: function(response){
                response = response.trim();
                if (response == "-1"){
                    $(".screen-cover").remove();
                }
                else if (response == "0"){
                    goback();
                }
                else{
                    doc_id = response.trim();
                    $("#lemurbox").attr("src", home_prefix+url+'?e='+response)
                }
            }
            // what about 0 response ??
   });
}

function goback(){
    level = 'L';
    lockscreen();
    $.ajax({
        method: "get",
        url: home_prefix + "otherlog.cgi",
        data:{
            source: mode,
            topic_id: tid,
            docno: doc_id,
            flag: 'goback',
        }
    })
    $("#lemurbox").attr("src", home_prefix+url+'?'+para);
    //$("#highlight input").val("");
}

function prepareTopbar(){
    $("#control_panel .search_button").click(runQuery);
    $("#docback").click(goback);
    $("#docdiscard").click(function(){
        move('r');
    });
    $("#docdup").click(function(){
        move('d');
    });
    $("#docnext").click(function(){
        switchDoc('n');
    });
    $("#docprev").click(function(){
        switchDoc('p');
    });

    $("#assesshappy").tooltip();

    $("#assesssad").tooltip();

    $("#highlight button").click(function(){
	$("#lemurbox")[0].contentWindow.highlight($("#highlightText").val());
    })
}
