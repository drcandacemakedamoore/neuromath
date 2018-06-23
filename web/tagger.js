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
        "#lesion-one",
        "#lesion-two",
        "#liver-one",
        "#liver-two",
        "#soft-tissue-one",
        "#soft-tissue-two",
        "#spleen",
        "#bowel"
    ].map($$);

    swatches.forEach(function (s) {
        s.click(swatchOnClick);
    });

    $("body").click(function (e) {
        var swatch = $("#swatch");
        if (swatch.length) {
            var svgParent = $("#swatches").parent();
            var tl = SVG.get("#swatches");
            var bgcolor = swatch.css('background-color');
            var offset = svgParent.offset();
            tl.rect(13, 11).move(
                e.pageX - offset.left,
                e.pageY - offset.top
            ).fill(bgcolor).click(function (e) {
                e.stopPropagation();
                this.remove();
            }).attr("data:sample", swatch.attr("data-sample"));
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
