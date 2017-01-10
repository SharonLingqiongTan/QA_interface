/* -------------------------------- */
/* ----general---- */

loptions = ["hide tagged", "show tagged"];


//global variables
/*
    uid
    uname
    did
    tid
    tname
    level
    para
    doc_id
    url
    loption
*/

function loptionChange(){
    loption = 1 - loption;
    $.ajax({
        method: "GET",
        url: "loption.cgi",
        data: {
            userid: uid,
            l: loption,
            topic_id: tid
        },
        success: function(){
            level = 'L';
            lockscreen();
            $("#lemurbox").attr("src", home_prefix+url+'?'+para);
        }
    });
    $(this).html(loptions[loption]);
}

function fillDomainBar(){
    var $option;

    for (i=2; i<dict["domains"].length;i++){
        $option = $("<option></option>").val(dict["domains"][i][0]).text(dict["domains"][i][1]);
        if (dict["domains"][i][0] == dict['domains'][0]){
            $option.prop("selected",true);
        };
        $("#Sdomain").append($option)
    };
}

function fillInfo(){
    $("#username").text('Hi, ' + dict['username'])
    $("#topicname2 span").text($("#Stopic option:selected").text());
    loption = parseInt(dict['loption']);
    $("#loption button").html(loptions[loption]);
    search_signal = 0;
}

function lemurBoxJump(){
    if ( mode == 'L'){
        url = dict["domains"][1];
    }
    else if (mode == 'S')
    {
        url = dict["domains"][1].replace('search', 'solr');
    }
    else if (mode == 'T'){
        url = dict["domains"][1].replace('search', 'terrier');
    }
    else if (mode == 'G'){
        url = dict["domains"][1].replace('search', 'gtown');
    }
    else{
        url = dict["domains"][1].replace('search', 'nist');
    }
    
    

    if (level == 'L'){
        $("#control_panel_2").hide();
        $("#lemurbox").attr("src", home_prefix+url+'?'+para);       
    }
    else{
        $("#control_panel_2").show();
        doc_id = dict['topics'][4];
        $("#lemurbox").attr("src", home_prefix+url+'?e='+dict['topics'][4])
    }
}

function getQuery(){
    if (mode == 'G' || mode =='N') {return;}
    var tmp = para.split("q=");

    if (tmp.length<=1) {return;}
    $("#control_panel input").val(decodeURIComponent(tmp[1]).replace(/\+/g," "));
}

function parse(){
    dict = JSON.parse(data)

    uid = dict['userid'];
    uname = dict['username'];
    did = dict['domains'][0];
    tid = dict['topics'][0];
    tname = dict['topics'][5]
    mode = dict['topics'][1];
    level = dict['topics'][2];
    para = dict['topics'][3];

    fillDomainBar();
    fillInfo();
    getQuery();
    lemurBoxJump();
};

function valign($element){
    $element.each(function(){
        var margin_top = ($(this).parent().height() - $(this).innerHeight() - $(this).css("border-top-width").replace("px","") - $(this).css("border-bottom-width").replace("px","")) / 2;
        $(this).css("margin-top",margin_top + "px");
    });
};

function valignelements(){
    valign($("#domain_panel_description"));
    valign($("#topic_panel_description"));
    valign($("#edit_topic"));
    valign($("#add_subtopic_hint"));
    valign($("#confirm_sub"));
    valign($("#cancel_add_sub"));
};

function getSidebar(){
    if (tname != ''){
        $.ajax({
            url: "sidebarHandler.cgi",
            data: {
                topic_id: tid
            },
            dataType: "json",
            success: function(data){
                for (i=0;i<data.length;i++){
                    $subtopic = generateSubtopic(data[i][1], data[i][0]);
                    for (j=2;j<data[i].length;j++){
                        $passage = addPassageCallBack(data[i][j][1], $subtopic.find(".droppable"), data[i][j][0], data[i][j][2]);
                        if (data[i][j][3] != 0){
                        //    $passage.addClass("grey");
                            $passage.find("input").eq(data[i][j][3] - 1).prop("checked",true);
                        //    $passage.find("input").prop("disabled",true);
                        }
                    }
                }
            },
	    complete: function(){
		if (uname == "admin"){
		    $('.deleteSubtopic').hide();
		    $('.Cboxheader span').hide();
		    $('.deletePassage').hide();
		    $(".passage form input").prop("disabled",true);
		};
	    }
        });
    }
};

function generateSubtopic(subtopic_name, subtopic_id){
    $dropbox = newDropbox(subtopic_name, subtopic_id);
    $("#dropbox_list").prepend($dropbox).show()
    if ($dropbox.find("h1").width() >= 279){
        $dropbox.find("h1").attr("title",subtopic_name);
    }
    return $dropbox
}

function test(){alert('haha')};
function logCurrentPage(urlvalue) {
    $.ajax({
        method: "POST",
        url: "logstate.cgi",
        data: {
            topic_id: tid,
            logurl: encodeURIComponent(urlvalue)
        }
    });
};

/* -------------------------------- */


/* -------------------------------- */
/* ----topic panel--- */

function addTopic(){
    $screen_lock = $("<div class='screen-cover'></div>");
    $screen_lock.css({
        "position" : "absolute",
        "z-index" : 10000,
        "background-color" : "#000",
        "opacity" : 0.15
    });
    $screen_lock.width($("body").width());
    $screen_lock.height($("body").height());
    $screen_lock.prependTo($("body"));
    $("#Atopic").css({
    	"z-index" : 10001,
	"position" : "relative"
    });
    $screen_lock.click(function(){
	alertdialog(1);
    });
    $("#Ctopic").hide();
    $("#Atopic input").val("");
    $("#Atopic").css({"display":"block","opacity":0});
    $("#Atopic").fadeTo("fast",1);
    valign($("#Atopic .cancel_topic"));
};

function confirmAddTopic(){
    $.ajax({
        method: "POST",
        url: "topicHandler.cgi",
        data: {
            userid : uid,
            domain_id : did,
            topic_name : $("#Atopic input").val()
        },
        success: function(response){
            addTopicCallBack(response.trim());
        }
    });
};

function addTopicCallBack(response){
    if (response == 0){
	alertdialog(2);
    }
    else if (response == -1){
	alertdialog(6);
    }
    else{
        //alert("Topic: " + $("#Atopic input").val() + " successfully added");
        //location = location + "?topic=" + response;
        /*
	$.ajax({
	    method: "post",
	    url: "./beta.cgi",
	    data: {
		topic: response
	    },
	    success: function(){
		window.location.reload();
	    }
	})
	if (tid == 0){
	    $.ajax({
		method: "POST",
		url: "logstate.cgi",
		data: {
		    topic_id: response,
		    logurl: encodeURIComponent(document.getElementById('lemurbox').contentWindow.location.href)
		}
	    });
	};*/
	$("<form action='./beta.cgi' method='post'><input name='topic' value="+response+"></form>").submit();
	/*
	$("#Stopic").append($("<option></option>").val(response).text($("#Atopic input").val()));
        if ($("#Stopic option").length == 1){
            tid = response;
            $("#Stopic option").prop("selected", true);
        }
        $("#Atopic .cancel_topic").trigger("click");
	*/
    }
};

function editTopic(){
    if (tname != '') {
        $("#Ctopic").hide();
        $("#Etopic input").val($("#Stopic option:selected").text());
        $("#Etopic").css({"display":"block","opacity":0});
        $("#Etopic").fadeTo("fast",1);
        valign($("#Etopic .cancel_topic"));
    }
};

function confirmEditTopic(){
    $.ajax({
        method: "POST",
        url: "topicHandler.cgi",
        data: {
            userid : uid,
            domain_id : did,
            topic_id : tid,
            topic_name : $("#Etopic input").val()
        },
        success: function(response){
            editTopicCallBack(response.trim());
        }
    })
};

function editTopicCallBack(response){
    if (response == 0){
	alertdialog(2);
    }
    else if (response == -1){
	alertdialog(6);
    }
    else{
        $("#Stopic option:selected").text($("#Etopic input").val());
	$("#topicname2 span").text($("#Stopic option:selected").text());
        //alert("Topic name changed successfully");
        $("#Etopic .cancel_topic").trigger("click");
    }
};

function cancelTopic(){
    $(".screen-cover").remove();
    $(this).parent().hide();
    $("#Ctopic").fadeIn();
};

function deleteTopic(){
    if (tname != ''){
	if (confirm("are you sure you want to delete this topic?") == true){
	    $.ajax({
		method : "post",
		url: "./deleteHandler.cgi",
		data:{
		    topic_id: tid,
		    domain_id: did,
		    userid: uid
		},
		success: function(response){
		    $("<form action='./beta.cgi' method='post'><input name='topic' value="+response.trim()+"></form>").submit();	
		}
	    });
	};
    };
};
/* -------------------------------- */


/* -------------------------------- */
/* ----subtopic panel---- */

function addSubtopic(){
    if (tname != ''){
        $("#add_subtopic_hint").hide();
        $("#input_subtopic").val("");
        $("#Asubtopic").fadeIn();
        valign($("#input_subtopic"));
        valign($("#cancel_add_sub"));
    }
    else{
	   alertdialog(1);
    }
};

function cancelAddSub(){
    $("#Asubtopic").hide();
    $("#add_subtopic_hint").fadeIn();
};

function confirmAddSub(){
    $.ajax({
        method: "POST",
        url: "subtopicHandler.cgi",
        data: {
            userid : uid,
            topic_id : tid,
            subtopic_name : $("#input_subtopic").val()
        },
        success: function(response){
            addSubCallBack(response.trim());
        }
    });
};

function addSubCallBack(response){
    if (response == 0){
	alertdialog(3);
    }
    else if (response == -1){
	alertdialog(7);
    }
    else{
        $dropbox = newDropbox($("#input_subtopic").val(), response);
        $("#dropbox_list").prepend($dropbox).hide().fadeIn();
	if ($dropbox.find("h1").width() >= 279){
	    $dropbox.find("h1").attr("title",$dropbox.find("h1").text());
	}
        $("#cancel_add_sub").trigger("click");
    }
};

function newDropbox(subtopic_name, subtopic_id){
    $dropbox = $("<div class='dropbox'>\
                      <div class='boxheader'>\
                          <div class='Cboxheader'>\
                                <h1></h1>\
				<span>edit</span>\
                                <img src='./img/trash.png' class='deleteSubtopic'/>\
                                <div class='pstat'>#:<div class='pcount'>0</div>\
                                <img class='findmore_mag gufindmore' title='find more' src='./img/mag2.png'/>\
                                <img class='findmore_mag nistfindmore' title='find more' src='./img/mag1.png'/>\
                                </div>\
                                <div class='clear'></div>\
                          </div>\
                          <div class='Eboxheader'>\
                                <input type='text'/>\
                                <span>cancel</span>\
                                    <img src='./img/confirm.png'/>\
                                <div class='clear'></div>\
                          </div>\
                      </div>\
                      <div class='droppable' ondragover='return false' ondrop='annotate(event)'></div>\
                 </div>");
    $("#scount").text(parseInt($("#scount").text()) + 1);
    $dropbox.find("h1").tooltip({
        position: {my:"left top"}
    });
    $dropbox.find(".gufindmore").click(function(e){gufindmore(e);}).tooltip();
    $dropbox.find(".nistfindmore").click(function(e){nistfindmore(e);}).tooltip();
    $dropbox.find("h1").text(subtopic_name)
    $dropbox.find(".Cboxheader span").click(editSub);
    $dropbox.find(".Cboxheader .deleteSubtopic").click(deleteSub);
    $dropbox.find(".Eboxheader img").click(confirmEditSub);
    $dropbox.find(".Eboxheader input").keypress(function (e){
        if (e.which == 13){
            e.preventDefault();
            $(this).siblings('img').trigger('click');
	};
    }); 
    $dropbox.find(".Eboxheader span").click(cancelEditSub);
    $dropbox.data("subtopic_name",subtopic_name);
    $dropbox.data("subtopic_id",subtopic_id)
    return $dropbox
}

function gufindmore(e){
    mode = 'G';
    url = dict["domains"][1].replace('search', 'gtown');
    level = 'L';
    var sid = $(e.target).closest(".dropbox").data("subtopic_id");
    search_signal = 1;
    tmppara = "a=1&T=" + tid + "&q=" + sid;
    para = tmppara.replace("a=1&","");
    // ?? set mode or level ??
    $("#control_panel_2").hide();
    //$("#highlight input", parent.document).val("");
    lockscreen();

    $("#lemurbox").attr("src", home_prefix + url + "?" + tmppara);

    $.ajax({
        method: "get",
        url: home_prefix + "otherlog.cgi",
        data:{
            source: mode,
            topic_id: tid,
            color: 'pink',
            subtopic_id: sid,
            flag: 'findmore'
        }
    })
}

function nistfindmore(e){
    mode = 'N';
    url = dict["domains"][1].replace('search', 'nist');
    level = 'L';
    var sid = $(e.target).closest(".dropbox").data("subtopic_id");
    search_signal = 1;
    tmppara = "a=1&T=" + tid + "&q=" + sid;
    para = tmppara.replace("a=1&","");
    // ?? set mode or level ??
    $("#control_panel_2").hide();
    //$("#highlight input", parent.document).val("");
    lockscreen();

    $("#lemurbox").attr("src", home_prefix + url + "?" + tmppara);

    $.ajax({
        method: "get",
        url: home_prefix + "otherlog.cgi",
        data:{
            source: mode,
            topic_id: tid,
            color: 'blue',
            subtopic_id: sid,
            flag: 'findmore'
        }
    })
}

function deleteSub(){
    if (confirm("are you sure you want to delete this subtopic?") == true)
    {
	$p = $(this).closest('.dropbox');
	$.ajax({
	    method: "post",
	    url: "./deleteHandler.cgi",
	    data:{
		subtopic_id: $p.data("subtopic_id")
	    },
	    success: function(){
		$p.fadeOut(300,function(){$(this).remove();})
		$("#scount").text(parseInt($("#scount").text()) - 1);
        getCount();
	    }
	})
    };
};
/* -------------------------------- */


/* -------------------------------- */
/* ----dropbox_list---- */

function editSub(){
    $(this).parent().hide();
    $Eboxheader = $(this).parent().siblings(".Eboxheader");
    $Eboxheader.fadeIn();
    $Eboxheader.children("input").val($(this).siblings("h1").text());
    valign($Eboxheader.children("img, span"));
};

function cancelEditSub(){
    $(this).parent().hide();
    $(this).parent().siblings(".Cboxheader").fadeIn();
};

function confirmEditSub(){
    $r = $(this);
    $.ajax({
        method: "POST",
        url: "subtopicHandler.cgi",
        data: {
            userid : uid,
            topic_id : tid,
            subtopic_id : $(this).closest(".dropbox").data("subtopic_id"),
            subtopic_name : $(this).siblings("input").val()
        },
        success: function(response){
            editSubCallBack(response.trim(), $r);
        }
    });
};

function editSubCallBack(response, $target){
    if (response == 0){
	alertdialog(3);
    }
    else if (response == -1){
	alertdialog(7);
    }
    else{
        $target.closest(".boxheader").find("h1").text($target.siblings("input").val());
        $target.closest(".dropbox").data("subtopic_name", $target.siblings("input").val());
        //alert("Subtopic name changed successfully");
        $target.siblings("span").trigger("click");
    };
};

function annotate(event){
    event.preventDefault();
    if ($dragging != null){
	$drecord = $dragging;
	$dtarget = $(event.target).closest(".droppable");
	if ($drecord.closest('.droppable').is($dtarget) == false){
	    $.ajax({
		method: "post",
		url: "./updatePassage.cgi",
		data: {
		    passage_id: $drecord.data("passage_id"),
		    subtopic_id: $(event.target).closest(".dropbox").data("subtopic_id"),
		    topic_id: tid
		},
		success: function(){
		    $drecord.closest('.dropbox').find('.pcount').each(function(){
			$(this).text(parseInt($(this).text()) - 1);
		    });
		    $(event.target).closest('.dropbox').find('.pcount').each(function(){
			$(this).text(parseInt($(this).text()) + 1);
		    });
		    $drecord.appendTo($dtarget).hide().fadeIn(100);
		    $dtarget.scrollTop($dtarget[0].scrollHeight);
		}
	    });
	}
    }
    else{
	if ($("#lemurbox").contents().find("docno").length){
	    addPassage(event);
	}
	else{
	    alertdialog(4);
	};
    }
};

function addPassage(event){
    var doc_id = getDocno();
    var selection = document.getElementById('lemurbox').contentWindow.getSelection();
    if (selection.toString().trim() == "") {
	alertdialog(4);	
    }
    else {
	var start = Math.min(selection.anchorOffset,selection.focusOffset);
	var end = start + selection.toString().length;
	var $target = $(event.target).closest(".droppable");
	var sid = $target.parent().data("subtopic_id");
	var ptext = event.dataTransfer.getData("text/plain");
    lockscreen();
	$.ajax({
	    method: "post",
	    url: "passageHandler.cgi",
	    data:{
		docno: doc_id,
                offset_start: start,
	        offset_end: end,
	        subtopic_id: sid,
	        passage_name: ptext
		},
            success: function(response){
	        addPassageCallBack(ptext, $target, response.trim(), doc_id);
            getCount();
            },
            complete: function(){
                $(".screen-cover").remove();
            }
        });
    };
};

function dragstartfunc(){
    $dragging = $(this);
};

function dragendfunc(){
    $dragging = null;
};

function addPassageCallBack(ptext, $target, response, doc_id){
    if (response == -1) {
	alertdialog(12);
    }
    else{
	$passage = $('<div class="passage" draggable="true">\
			<p></p>\
			<div class="origin">\
			    <span>From doc:</span>\
			    <span class="docno"></span>\
                <a class="dupPassage">dup</a>\
			    <img class="deletePassage" src="./img/trash.png">\
			    <div class="clear"></div>\
			</div>\
			<form>\
			    <input type="radio" class="score" name="score" value="1" />\
			    marginally relevant \
			    <input type="radio" class="score" name="score" value="2" />\
			    relevant \
			    <input type="radio" class="score" name="score" value="3" />\
			    highly relevant \
			    <input type="radio" class="score" name="score" value="4" />\
			    key result \
			</form>\
		    </div>');
	$passage.on("dragstart",dragstartfunc);
	$passage.on("dragend",dragendfunc);
	$passage.find('p').text(ptext);
	$passage.find('.docno').css('cursor','pointer').click(backToDocument).text(doc_id);
	$passage.find('input').click(grade);
	$passage.find('.deletePassage').click(function(e){deletePassage(e, 2)});
    $passage.find('.dupPassage').click(function(e){deletePassage(e, 3)});
	$passage.data("passage_id",response);
	$passage.appendTo($target).hide().fadeIn(100);
	$target.closest('.dropbox').find('.pcount').each(function(){
	    $(this).text(parseInt($(this).text()) + 1);
	});
	$target.scrollTop($target[0].scrollHeight);
	return $passage
    }
}

function deletePassage(e, s){
    if ((s == 2 && confirm("are you sure it's an irrelevant passage to this subtopic?") == true) || (s ==3 && confirm("are you sure it's a duplicate passage to this subtopic?") == true))
    {
    lockscreen();
	$p = $(e.target).closest('.passage');
	$.ajax({
	    method: "post",
	    url: "./deleteHandler.cgi",
	    data:{
          signal: s,
		  passage_id: $p.data("passage_id"),
          topic_id: tid
	    },
	    success: function(){
		$p.fadeOut(300,function(){$(this).remove();})
		$p.closest('.dropbox').find('.pcount').each(function(){
		    $(this).text(parseInt($(this).text()) - 1);
		});
        getCount();
	    },
        complete: function(){
            $(".screen-cover").remove();
        }
	});
    };
};

function grade(){
    $target = $(this);
    $.ajax({
        method: "post",
        url: "grade.cgi",
        data: {
            score: $target.val(),
            passage_id: $target.closest(".passage").data("passage_id"),
            topic_id : tid
        },
        success: function(){
            //$target.siblings("input").prop('disabled',true);
            //$target.prop('disabled',true);
            //$target.closest(".passage").addClass("grey");
        }
    })
}

function getDocno(){
    return $("#lemurbox").contents().find("docno").text().trim()
};

function backToDocument(){
    window.open(dict["domains"][1].replace("search","check") + "?e=" + $(this).text(), 'check',"height=600,width=900,left=" + (screen.width-900)/2 + ",top=" + (screen.height-700)/2);
};

function displayList(type){
    if (tname != ''){
        window.open("displayListHandler.cgi?type=" + type + "&topic_id=" + tid + "&domain_id=" + did + "&username=" + uname, type, "height=600,width=900,left=" + (screen.width-900)/2 + ",top=" + (screen.height-700)/2);      
    }
    else{
        alertdialog(1);
    }
	
};

function alertdialog(onum){
    $("#dialog" + onum).dialog("open");
};

/* -------------------------------- */


/* -------------------------------- */
/* ----main---- */
$(document).ready(function(){
    $("h1").click(function(){
	$("h1").find(".side-bar__title").toggleClass("collapsed")
    });
    $dragging = null;
    
    tag = false;   // ?? 

    $("body").height(Math.max(710, $(window).height()));
    
    $("#sidebar").height($("body").height() - 35);
    
    $("#lemurbox").height($("body").height() - 232);
    
    parse(data);

    $("#loption button").click(loptionChange);

    prepareTopbar();

    valignelements();

    getSidebar();

    getCount();

    $("#total_count").tooltip();
   
    $(".dialogs").dialog({
	autoOpen: false,
    });
    
    $("#logout").click(function(e){
        e.preventDefault();
        $.ajax({
    	    method: "post",
    	    url: "./otherlog.cgi",
    	    data: {
        		flag: 'logout'
    	    },
    	    complete: function(){
    		  document.cookie = "usercookie=;";
    		  location = home_prefix + "beta.cgi";
    	    }
    	});
    });

    $("#assesshappy").click(function(){moodFeedback("happy");})
    $("#assesssad").click(function(){moodFeedback("frustrated");})

    $("#Sdomain").change(function(event){
	   $("#Sdomain").closest("form").submit();
    });

    $("#Stopic").change(function(){
        $("#Stopic").closest("form").submit();
    });

    $("#add_topic").click(addTopic);

    $("#edit_topic").click(editTopic);

    $("#Atopic .confirm_topic").click(confirmAddTopic);

    $("#Atopic input").keypress(function (e){
	if (e.which == 13){
	    e.preventDefault();
	    confirmAddTopic();
	};
    });
    
    
    $("#Etopic .confirm_topic").click(confirmEditTopic);
    
    $("#Etopic input").keypress(function (e){
        if (e.which == 13){
            e.preventDefault();
            confirmEditTopic();
	};
    });    

    $("#topic .cancel_topic").click(cancelTopic);

    $("#delete_topic").click(deleteTopic);
    
    $("#add_subtopic").click(addSubtopic);
    
    $("#confirm_sub").click(confirmAddSub);

    $("#input_subtopic").keypress(function (e){
        if (e.which == 13){
            e.preventDefault();
            confirmAddSub();
	};
    });
    
    $("#cancel_add_sub").click(cancelAddSub);

    $(".Cboxheader span").click(editSub);

    $(".Eboxheader img").click(confirmEditSub);

    $(".Eboxheader span").click(cancelEditSub);

    $("#cdoclist").click(function(){
        displayList('tagged');
    });
    
    $("#ddoclist").click(function(){
        displayList('discarded');
    });

    $("#rdoclist").click(function(){
        displayList('duplicate');
    });
    
    $("#viewanno").click(function(){
        $.ajax({
            method : "post",
            url: "./viewannotations.cgi",
            data : {
                userid: uid,
                username: uname
            },
            success: function(){
                window.location = './view/' + uname + ".csv"
            }
        });
    /* commented for log
	$.ajax({
            method : "post",
            url: "./viewannotations.cgi",
            data : {
                userid: uid,
                username: uname
            },
            success: function(){
		$.ajax({
                    method: "post",
                    url: "http://infosense.cs.georgetown.edu/annotation/otherlog.cgi",
                    data: {
                        username: uname,
                        userid: uid,
                        flag: 'download'
                    },
                    complete: function(){
                        window.location = './view/' + uname + ".csv"
                    }
                });
            }
        })
    */
    });

    $("#saveanno").hide().click(function(){});
    
    $("#finishTopic").click(function(){
	   var flag = false;
    	$(".passage form").each(function(){
    	    if ($(":radio:checked", this).val() == undefined){
    		flag = true;
    		unfinished = $(this).closest(".dropbox").find("h1").text();  
    		return false;
    	    };
    	});
        if (flag == true) {
            alert("You have ungraded passage in subtopic: " + unfinished); 
        }
    	else if (tname !=''){
    	    $.ajax({
    		method: "post",
    		url: home_prefix + "otherlog.cgi",
    		data: {
    		    username: uname,
    		    userid: uid,
    		    topic_id: tid,
    		    flag: 'finish'
    		},
    		complete: function(){
    		    window.open("https://docs.google.com/forms/d/1mSKoylcF5wvrsqkRV6WcmVzpg5k2HA0LD715Gnsr2SI/viewform?entry.287497011=" + uname + "&entry.29467982=" + $("#Stopic option:selected").text().replace(' ','%20') + "&entry.566490455=" + tid + "&entry.1105456920=" + $("#Sdomain option:selected").text()) ; 
    		}
    	    });
    	}
    });
    
    $("#summary").click(function(){
	$.ajax({
	    method: "post",
	    url: "./viewsummary.cgi",
	    data : {
                userid: uid,
                username: uname,
	    },
	    success: function(){
                window.location = './view/summary.csv'
            }
	});
    });
});
