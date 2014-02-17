var count = 10;
var arr = new Array(100);
var items = new Array(100);
var item_id = new Array(100);

init();

function init() {
    $.getJSON("driver.php", function (json) {
        var data = eval(json);
        // 顶点数目
        var counter = data[0].length;
        console.log(counter);
        initItem(data, counter);
    });
}

function initItem(data, limit) {
    var collection = $("#ItemCollection");
    for (var i = 0; i < limit; i++) {
        arr[i] = new DrawArg(i);
        makeItem(i);
        console.log(items[i]);
        console.log(items[i].attr("no"));
        collection.append(items[i]);
        console.log(i);
    }

    function makeItem(i) {
        item_id[i] = "#item" + i;
        console.log(i);
        items[i] = $("<div></div>");

        $("#item" + i).click(function () {
            if ($(this).hasClass('noclick')) {
                $(this).removeClass('noclick');
            }
            else {
                showUp($("#item" + i).text(), $("#item" + i).position().x, $("#item" + i).position().y);
            }
        });
        $($("#item" + i).draggable({revert: true,
            start: function (event, ui) {
                $(this).addClass('noclick');
            }}));
        $("#item" + i).droppable({
            drop: function (event, ui) {
                console.log(event);
                console.log(event.toElement.innerText, "->", event.target.innerText);
                var isConnect = confirm("确定要建立从\"" + event.toElement.innerText + "\'到\"" + event.target.innerText + "\"的关联吗？");
            }
        });
        var item_radius = arr[i].R;
        items[i].attr('id', "item" + data[0][i][0]);
        items[i].text(data[0][i][1]);
        items[i].attr('context', data[0][i][2]);
        items[i].attr('url', data[0][i][3]);
        items[i].attr('no', i);
//        items[i].attr('draggable', "true");
        items[i].css('width', item_radius * 2 + "px");
        items[i].css('height', item_radius * 2 + "px");
        items[i].css('border', item_radius + "px yellow");
        items[i].css('border-radius', item_radius + "px");
        items[i].css('background-color', "orange");
        items[i].css('position', "absolute");
        items[i].css('top', arr[i].y - item_radius + "px");
        items[i].css('bottom', arr[i].y + item_radius + "px");
        items[i].css('left', arr[i].x + item_radius + "px");
        items[i].css('right', arr[i].x - item_radius + "px");
    };
}

function DrawArg(id) {
    this.x = Math.round(Math.random() * 800);
    this.y = Math.round(Math.random() * 600);
    this.R = Math.round(Math.random() * 20) + 50;
    this.ID = id;
}

function showUp(str, xset, yset) {
    $("#show").text(str);
    $("#show").dialog({
        autoOpen: false,
        show: {
            effect: "explode",
            duration: 1000
        },
        hide: {
            effect: "explode",
            duration: 1000
        },
        position: {
            x: xset,
            y: yset
        }
    });
    $("#show").dialog("open");
}