function timestampToDate() {
    var inputTimestamp = document.getElementById('input_timestamp').value;
    var newDate = new Date();
    newDate.setTime(inputTimestamp * 1000);
    document.getElementById('output_time').value = newDate.format("yyyy-MM-dd hh:mm:ss");
}

function dateToTimestamp() {
    var inputDate = document.getElementById('input_time').value;
    var timestamp = Date.parse(new Date(inputDate));
    document.getElementById('output_timestamp').value = timestamp / 1000;
}

function currentDate() {
    var newDate = new Date();
    document.getElementById('current_date').innerHTML = newDate.format("yyyy-MM-dd hh:mm:ss");
}
function currentTimestamp() {
    var timestamp = Date.parse(new Date());
    timestamp = timestamp / 1000;
    document.getElementById('current_timestamp').innerHTML = timestamp;
}

function base64Decode() {
    var inputText = document.getElementById('base64_text_output').value;
    document.getElementById('base64_text_input').value = Base64.decode(inputText);
}

function base64Encode() {
    var inputText = document.getElementById('base64_text_input').value;
    document.getElementById('base64_text_output').value = Base64.encode(inputText);
}

function md5Encode() {
    var inputText = document.getElementById('md5_text_input').value;
    document.getElementById('md5_text_output').value = md5(inputText);
}

function encodeImg() {
    var file = document.getElementById('upload_file').files[0];
    if (!/image\/\w+/.test(file.type)) {
        alert("请确保文件为图像类型");
        return false;
    }
    var reader = new FileReader();
    reader.onload = function () {
        document.getElementById('base64_img_output').value = reader.result;
    };
    reader.readAsDataURL(file);
}

function decodeImg() {
    var img = document.getElementById('img_decode');
    img.src = document.getElementById('base64_img_output').value;
}
Date.prototype.format = function (format) {
    var date = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S+": this.getMilliseconds()
    };
    if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    for (var k in date) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1
                ? date[k] : ("00" + date[k]).substr(("" + date[k]).length));
        }
    }
    return format;
};

setInterval(currentDate, 1000);
setInterval(currentTimestamp, 1000);