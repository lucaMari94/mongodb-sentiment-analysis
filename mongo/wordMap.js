function wordMap(){

	//var words = this.word.match(/\w+/g);
    //var words =  this.word.match(/(\:\w+\:|\<[\/\\]?3|[\(\)\\\D|\*\$][\-\^]?[\:\;\=]|[\:\;\=B8][\-\^]?[3DOPp\@\$\*\\\)\(\/\|])(?=\s|[\!\.\?]|$)/g);
	//var words =  this.word.match(/(.*)/g);
    var words =  this.word.match(/^\s*\S+(\s?\S)*\s*$/g);
	if(words == null) {
		return;
	}

	for (var i = 0; i < words.length; i++){
		emit(words[i], {count: 1});
	}
}