
function expand(evento,id)
{
	if (evento) evento.preventDefault();
	$( "#"+id+"-content div.comments" ).hide();
	$( "#"+id+"-content" ).stop().addClass( "content_expanded1");
	$( "#"+id+"-content" ).addClass( "content_expanded0", "slow");
}

function contract(evento,id)
{
	evento.preventDefault();
	if ($( "#"+id+"-content:animated" )[0]) return;
	$( "#"+id+"-content" ).stop().removeClass( "content_expanded0", "slow", function(){$( "#"+id+"-content" ).removeClass( "content_expanded1");});
}

function updatecomments(slug)
{
    $.ajax({
		url:MAIN_URL+slug+'/ajaxcomments',
		success:function(data) {
        $("#"+slug+"-content div.comments").html(data);
    }});
}
