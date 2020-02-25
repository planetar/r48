(function(i) {
    //return i ;
    var json = JSON.parse(i);
    //return json["sensordatavalues"] ;
    return json["sensordatavalues"][0]["value"] ;
})(input)