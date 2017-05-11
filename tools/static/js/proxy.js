function last_page() {
    if (page != 1) {
        page = page - 1;
    }
    get_proxy_ip(page, 15, 'last');
}

function next_page() {
    page = page + 1;
    get_proxy_ip(page, 15, 'next');
}

function get_proxy_ip(page, num, click_btn) {
    var timestamp = Date.parse(new Date());
    timestamp = timestamp / 1000;
    var token = md5(String(page) + String(num) + String(timestamp));
    $.get('../proxy?page=' + page + '&num=' + num + '&token=' + token + '&t=' + timestamp, function (result) {
        if (result.status === 'true') {
            var setHtml = "";
            $("#ip-list").html(setHtml);
            var items = result.list;
            for (var index = 0; index < items.length; ++index) {
                item = items[index];
                setHtml += "<tr>\n<td>" + (index + 1) + "</td>\n";
                setHtml += "<td>" + item.ip.toString() + "</td>\n";
                setHtml += "<td>" + item.port.toString() + "</td>\n";
                setHtml += "<td>" + item.time.toString() + "</td>\n</tr>\n";
            }
            $("#ip-list").html(setHtml);
            if (click_btn === 'next') {
                document.getElementById("last-page").disabled = false;
                if (items.length < 15) {
                    document.getElementById("next-page").disabled = true;
                }
            } else {
                document.getElementById("next-page").disabled = false;
                if (page === 1) {
                    document.getElementById("last-page").disabled = true;
                }
            }

        }
    });
}
var page = 1;
next_page();
