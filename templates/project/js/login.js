$("body").delegate("button[data-do*='login-modal-cancel']", "click", function(){
	$('#loginModal').foundation('reveal', 'close');
	return false;
});

$("body").delegate("button[data-do*='profile-modal-cancel']", "click", function(){
	$('#profileModal').foundation('reveal', 'close');
	return false;
});
