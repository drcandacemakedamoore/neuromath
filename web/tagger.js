$(function () {
    $("[data-toggle='tooltip']").tooltip();

    function swatchOnClick(e) {
        $("#swatch").remove();
        var id = e.currentTarget.id;
        var classList = e.currentTarget.className.split(" ");
        var bg = classList.pop();
        $("body").append("<div id='swatch' class='swatch " + bg + "'>");
        console.log("clicked: " + e.currentTarget.id);
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

    $("body").click(function () {
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
});
