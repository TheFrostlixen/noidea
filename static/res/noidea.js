function open_media(media_name) {
	window.open('play/?media=' + media_name, '_blank');
}

function update_list() {
	var searchName = document.getElementById('search-bar').value;
	
	var itemlist = document.querySelectorAll('#media-table')[0].children;
	for (i = 0; i < itemlist.length; i++) {
		var searchResult = itemlist[i].outerText.toLowerCase().trim().indexOf( searchName.toLowerCase() );
		if (searchResult < 0) {
			itemlist[i].style.display = 'none';
		}
		else {
			itemlist[i].style.display = '';
		}
	}
}
