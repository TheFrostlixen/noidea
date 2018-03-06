function open_media(media_name) {
	var dataDictionary = []; // create an empty array

	dataDictionary.push({
		media_name: media_name
	});

	var request = new XMLHttpRequest();
	request.open('POST', '/play', true);
	request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
	request.send(JSON.stringify(dataDictionary));
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

function clear_search() {
	document.getElementById('search-bar').value = "";
	update_list();
}

function play_random() {
	var itemlist = [];
	
	Array.from(document.getElementsByClassName("item")).forEach(function(item) {
		if (!(isHidden(item))) {
			itemlist.push(item);
		}
	});
	
	var rand_index = Math.floor(Math.random() * itemlist.length);
	eval(itemlist[rand_index].onclick());
}

function isHidden(el) {
	var style = window.getComputedStyle(el);
	return ((style.display === 'none') || (style.visibility === 'hidden'))
}
