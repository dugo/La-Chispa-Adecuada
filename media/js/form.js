function init_form()
{
	$( "#addcomment" ).dialog({
		autoOpen: false,
		height: 380,
		width: 350,
		modal: true,
		resizable:false,
		buttons: {
			"Enviar": function() {
				var bValid = true;
				
				var name = $( "#name" );
				var email = $( "#email" );
				var comment = $( "#comment" );
				var slug = $( "#slug" );

				$('#name, #email, #comment').removeClass( "ui-state-error" );

				bValid = bValid && checkLength( name, "nombre o alias", 3, 40 );
				bValid = bValid && checkLength( email, "email", 0, 80 );
				bValid = bValid && checkLength( comment, "comentario", 1, 1000 );

				if (email.val().length)
					bValid = bValid && checkRegexp( email, /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i, "eg. ui@jquery.com" );

				if ( bValid ) {
					/** Si todo es válido **/
					$.ajax({
						url:MAIN_URL+slug.val()+'/comments/',
						async:false,
						type:'POST',
						data:$(this).find('form').serialize(), 
						success: updatecomments(slug.val())
						});
					$( this ).dialog( "close" );
				}
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
			$('#name, #email, #comment').removeClass( "ui-state-error" );
		}
	});
}

function updateTips( t ) {
	$( ".validateTips" )
		.text( t )
		.addClass( "ui-state-highlight" );
	setTimeout(function() {
		tips.removeClass( "ui-state-highlight", 1500 );
	}, 500 );
}

function checkLength( o, n, min, max ) {
	if ( o.val().length > max || o.val().length < min ) {
		o.addClass( "ui-state-error" );
		updateTips( "La longitud del " + n + " debe estar entre " +
			min + " y " + max + " caracteres." );
		return false;
	} else {
		return true;
	}
}

function checkRegexp( o, regexp, n ) {	
	if ( !( regexp.test( o.val() ) ) ) {
		o.addClass( "ui-state-error" );
		updateTips( n );
		return false;
	} else {
		return true;
	}
}
