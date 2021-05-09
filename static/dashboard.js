//event handling for different light mode buttons

var button1 = $("#light_mode1");
button1.click(function() {
    if (button1.text() === "Random Mode") {
        button1.text("Random Mode On");
        button2.text("Snake Flash");
        button3.text("Strobe Party");
        button4.text("Illuminate");
        button5.text("Music Mode");
        $.ajax({
            url: "/light_mode1_on",
            type: "post",
            timeout: 100
        });
    } else {
        button1.text("Random Mode");
        $.ajax({
            url: "/light_mode1_off",
            type: "post"
        })
    }
});

var button2 = $("#light_mode2");
button2.click(function() {
    if (button2.text() === "Snake Flash") {
        button1.text("Random Mode");
        button2.text("Snake Flash On");
        button3.text("Strobe Party");
        button4.text("Illuminate");
        button5.text("Music Mode");
        $.ajax({
            url: "/light_mode2_on",
            type: "post",
            timeout: 100
        });
    } else {
        button2.text("Snake Flash");
        $.ajax({
            url: "/light_mode2_off",
            type: "post"
        })
    }
});

var button3 = $("#light_mode3");
button3.click(function() {
    if (button3.text() === "Strobe Party") {
        button1.text("Random Mode");
        button2.text("Snake Flash");
        button3.text("Strobe Party On");
        button4.text("Illuminate");
        button5.text("Music Mode");
        $.ajax({
            url: "/light_mode3_on",
            type: "post",
            timeout: 100
        });
    } else {
        button3.text("Strobe Party");
        $.ajax({
            url: "/light_mode3_off",
            type: "post"
        })
    }
});

var button4 = $("#illuminate");
button4.click(function() {
    if (button4.text() === "Illuminate") {
        button1.text("Random Mode");
        button2.text("Snake Flash");
        button3.text("Strobe Party");
        button4.text("Illuminate On");
        button5.text("Music Mode");
        $.ajax({
            url: "/illuminate_on",
            type: "post",
            timeout: 100
        });
    } else {
        button4.text("Illuminate");
        $.ajax({
            url: "/illuminate_off",
            type: "post"
        })
    }
});

var button5 = $("#music_mode");
button5.click(function() {
    if (button5.text() === "Music Mode") {
        button1.text("Random Mode");
        button2.text("Snake Flash");
        button3.text("Strobe Party");
        button4.text("Illuminate");
        button5.text("Music Mode On");
        $.ajax({
            url: "/music_mode_on",
            type: "post",
            timeout: 100
        });
    } else {
        button5.text("Music Mode");
        $.ajax({
            url: "/music_mode_off",
            type: "post"
        })
    }
});
