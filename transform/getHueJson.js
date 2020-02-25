(function(i) {
    return i;
    var json = JSON.parse(i);
    return parseInt(json["state"]["buttonevent"]);
})(input)