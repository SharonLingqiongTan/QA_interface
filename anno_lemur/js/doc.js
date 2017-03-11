function snapSelectionToWord() {
    rangy.getSelection().expand("word");
    //winodow.getSelection.collapseToStart() 
};

function highlighting(signal){
    var re;
    var terms = $("#highlight input", parent.document).val().split(/[^\w\.]+/);

    if (terms == "") {
        terms = $("#control_panel input", parent.document).val().split(/[^\w\.]+/);
    }
    if (terms.indexOf('<')>-1 || terms.indexOf('>')>-1) {
        alert("Invalid query, please do not use < or >");
        return;
    }

    $("docno").siblings("text").html(ohtml);

    for (var i=0;i<terms.length;i++){
        if (stopwords.indexOf(terms[i].toLowerCase()) == -1 && terms[i].length>=2){
        //re1 = new RegExp('(>[^<>]*)('+ terms[i] + ')([^<>]*>)','gi');
        //re2 = new RegExp('(<[^<>]*)('+ terms[i] + ')([^<>]*<)','gi');
        re3 = new RegExp('(>[^<>]*)('+ terms[i] + ')([^<>]*<)','gi');
        //$("docno").siblings("text").html($("docno").siblings("text").html().replace(re1, '$1<span class="lemurhighlight">$2</span>$3'));
        //$("docno").siblings("text").html($("docno").siblings("text").html().replace(re2, '$1<span class="lemurhighlight">$2</span>$3'));
        //$("docno").siblings("extracted_text").html($("docno").siblings("extracted_text").html().replace(re3, '$1<span class="lemurhighlight">$2</span>$3'));

        };
    };

    if (signal == 0) {return;}

    $.ajax({
        method: "get",
        url: parent.home_prefix + "otherlog.cgi",
        data:{
            flag: 'highlight',
            topic_id: parent.tid,
            docno: parent.doc_id,
            hstring: $("#highlight input", parent.document).val()
        }
    });
};


function logCurrentPage(){
    $.ajax({
        method: "post",
        url: parent.home_prefix + "logstate.cgi",
        data:{
            topic_id: parent.tid,
            docno: parent.doc_id
        },
        success: function(response){
            if (response.trim() == "1"){
                $("#tagflag", parent.document).html("tagged");
            }
            else{
                $("#tagflag", parent.document).html(" ");              
            }
        }
    });
}

$(document).ready(function(){

    $(".screen-cover", parent.document).remove();

    ohtml = $("docno").siblings("text").html();

    parent.getCount();

    $("docno").after("<br/><br/>");

    //$("#highlight input", parent.document).val("");

    logCurrentPage();
 
    highlighting(0); //where's highlight html?
    
    $("docno").siblings("text").mouseup(snapSelectionToWord);

    $("text a").click(function(e){
	window.open(this.href,"outlink","height=600,width=900,left=" + (screen.width-900)/2 + ",top=" + (screen.height-700)/2);
	e.preventDefault();
    });
    var imgs = Array.prototype.slice.apply(document.getElementsByTagName('img'));
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].addEventListener("dragstart", function(ev) {
        ev.dataTransfer.setData("text", ev.target.src);}, false);
    }
});
