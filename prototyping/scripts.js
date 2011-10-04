function onLoad()
{
	$("#search").hover(function(){
		if ($("#search").val() == "Search for projects!")
		{
			$(this).val("");
			$(this).removeClass("graytext");
			$(this).focus();
		}
	}, function() {
		if ($(this).val() == "")
		{
			$(this).val("Search for projects!");
			$(this).addClass("graytext");
			$(this).blur();
		}
	});

	$("#search").focusout(function(){
		if ($(this).val() == "")
		{
			$(this).val("Search for projects!");
			$(this).addClass("graytext");
		}
	});
}