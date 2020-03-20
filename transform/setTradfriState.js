// Transforms an input value of 0 or 1 to "OFF" or "ON" respectively and formats as JSON
(function(x) {
    var result = new Object();
    if (x == 1) {
    result.state = "ON"
    }
    else if (x == 0) {
    result.state = "OFF"
    }
    else if (x == "1") {
    result.state = "ON"
    }
    else if (x == "0") {
    result.state = "OFF"
    }
    else result.state = x
    return JSON.stringify(result);
    })(input)
    