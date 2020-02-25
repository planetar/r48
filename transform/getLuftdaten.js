(function(i) {
    return i ;
    var json = JSON.parse(i.response);
    return parseInt(json["sensordatavalues"][0]) ;
})(input)