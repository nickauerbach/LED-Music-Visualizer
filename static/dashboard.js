//event handling for different light mode buttons

var button1 = $("#light_mode1");
button1.click(function() {
    if (button1.text() === "Slow Mode") {
        $.ajax({
            url: "/light_mode1_on",
            type: "post",
            success: function(response) {
                console.log(response);
                button1.text("Slow Mode On");
                button2.text("Medium Flash");
                button3.text("Strobe Party");
                button4.text("Illuminate");
                button5.text("Music Mode");
            }
        });
    } else {
        $.ajax({
            url: "/light_mode1_off",
            type: "post",
            success: function() {
                button1.text("Slow Mode");
            }
        })
    }
});

var button2 = $("#light_mode2");
button2.click(function() {
    if (button2.text() === "Medium Flash") {
        $.ajax({
            url: "/light_mode2_on",
            type: "post",
            success: function(response) {
                console.log(response);
                button1.text("Slow Mode");
                button2.text("Medium Flash On");
                button3.text("Strobe Party");
                button4.text("Illuminate");
                button5.text("Music Mode");
            }
        });
    } else {
        $.ajax({
            url: "/light_mode2_off",
            type: "post",
            success: function() {
                button2.text("Medium Flash");
            }
        })
    }
});

var button3 = $("#light_mode3");
button3.click(function() {
    if (button3.text() === "Strobe Party") {
        $.ajax({
            url: "/light_mode3_on",
            type: "post",
            success: function(response) {
                console.log(response);
                button1.text("Slow Mode");
                button2.text("Medium Flash");
                button3.text("Strobe Party On");
                button4.text("Illuminate");
                button5.text("Music Mode");
            }
        });
    } else {
        $.ajax({
            url: "/light_mode3_off",
            type: "post",
            success: function() {
                button3.text("Strobe Party");
            }
        })
    }
});

var button4 = $("#illuminate");
button4.click(function() {
    if (button4.text() === "Illuminate") {
        $.ajax({
            url: "/illuminate_on",
            type: "post",
            success: function(response) {
                console.log(response);
                button1.text("Slow Mode");
                button2.text("Medium Flash");
                button3.text("Strobe Party");
                button4.text("Illuminate On");
                button5.text("Music Mode");
            }
        });
    } else {
        $.ajax({
            url: "/illuminate_off",
            type: "post",
            success: function() {
                button4.text("Illuminate");
            }
        })
    }
});

var button5 = $("#music_mode");
button5.click(function() {
    if (button5.text() === "Music Mode") {
        $.ajax({
            url: "/music_mode_on",
            type: "post",
            success: function(response) {
                console.log(response);
                button1.text("Slow Mode");
                button2.text("Medium Flash");
                button3.text("Strobe Party");
                button4.text("Illuminate");
                button5.text("Music Mode On");
            }
        });
    } else {
        $.ajax({
            url: "/music_mode_off",
            type: "post",
            success: function() {
                button5.text("Music Mode");
            }
        })
    }
});
