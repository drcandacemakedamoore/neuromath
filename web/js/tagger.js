Dropzone.autoDiscover = false;

$(function () {
    $("[data-toggle='tooltip']").tooltip();

    function swatchOnClick(e) {
        $("#swatch").remove();
        var id = e.currentTarget.id;
        var classList = e.currentTarget.className.split(" ");
        var bg = classList.pop();
        $("body").append("<div id='swatch' class='swatch " + bg + "'>");
        $("#swatch").attr("data-sample", bg);
        e.stopPropagation();
    }

    // Most of the time we don't need to pass more than one argument,
    // but some JS api pass more useless arguments.
    function $$ (x) { return $(x); }

    var swatches = [
        "#lesion",
        "#liver",
        "#soft-tissue",
        "#spleen",
        "#bowel",
        '#lung',
        '#bone',
        '#fat'
    ].map($$);

    swatches.forEach(function (s) {
        s.click(swatchOnClick);
    });

    var stats = $("#stats").DataTable({
        data: [],
        createdRow: function (row, data, index) {
            $("td", row).addClass(data[1]);
        }
    });
    var uploads = new Dropzone("#dicom-uploads");
    var tagCounter = 1;

    uploads.on("complete", function (response) {
        console.log("complete response " + response.xhr.response);
        var img = SVG.get("#sample-image");
        img.load(JSON.parse(response.xhr.response)).loaded(function(loader) {
            this.size(loader.width, loader.height);
            var parent = this.parent();
            this.move(
                (parent.width() - loader.width) >> 1,
                (parent.height() - loader.height) >> 1
            );
        });
    });

    function imageTagSuccess(section, x, y, w, h, response) {
        stats.row.add([
            tagCounter,
            section,
            response[0].toFixed(6),                // dissimilarity
            response[1].toFixed(6),                // correlation
            response[2].toFixed(6),                // std
            response[3].toFixed(6),                // entropy
            x | 0,
            y | 0
        ]).draw(false);
        tagCounter++;
    }

    function addRow(section, x, y, swatch) {
        var image = $("#sample-image")[0].href.baseVal;
        var w = swatch.width();
        var h = swatch.height();
        $.ajax({
            type: "POST",
            url: "/sample/tag/" + image,
            data: JSON.stringify({
                area: [x, y, w, h]}),
            success: function (response) {
                return imageTagSuccess(section, x, y, w, h, response);
            },
            dataType: "json"
        });
    }
    
    $("body").click(function (e) {
        var swatch = $("#swatch");
        if (swatch.length) {
            var svgParent = $("#swatches").parent();
            var tl = SVG.get("#swatches");
            var bgcolor = swatch.css('background-color');
            var offset = svgParent.offset();
            var ioffset = $("#sample-image").offset();
            var x = e.pageX - offset.left;
            var y = e.pageY - offset.top;
            var ix = e.pageX - ioffset.left;
            var iy = e.pageY - ioffset.top;
            var section = swatch.attr("data-sample");
            var label = tl.text("" + tagCounter).move(x + 15, y).fill(bgcolor);
            tl.rect(13, 11).move(x, y).fill(bgcolor).click(function (e) {
                e.stopPropagation();
                var t = +label.text();
                this.remove();
                label.remove();
                stats.row(function (i, data, node) {
                    return t == data[0];
                }).remove().draw(false);
            }).attr("data:sample", section);
            addRow(section, ix, iy, swatch);
        }
        $("#swatch").remove();
        $("body").css({cursor: "auto"});
    });

    $("body").mousemove(function (e) {
        var swatch = $("#swatch");
        if (swatch.length) {
            $("body").css({cursor: "none"});
            swatch.css({top: e.pageY, left: e.pageX});
        }
    });

    $("#submit").click(function (e) {
        var image = $("#sample-image")[0].href.baseVal;

        console.log("image: " + image);
        function success (response) {
            console.log("response: " + response);
        }
        $("#swatches").children("rect").each(function (i, elt) {
            elt = $(elt);
            var x = elt.attr("x");
            var y = elt.attr("y");
            var width = elt.attr("width");
            var height = elt.attr("height");
            var sample = elt.attr("data:sample");

            $.ajax({
                type: "POST",
                url: "/sample/" + sample,
                data: JSON.stringify({
                    image: image,
                    area: [x, y, width, height]
                }),
                success: success,
                dataType: "json"
            });
        });
    });
});
