// ID Structure: REGION ROUND INDEX e.g. S 0 0
// Hidden Input Structure is the same but with a preceeding I

function bracketClick(team) {
    var name = $(team).text();
    var args = $(team).attr('id').split(' ');
    var region = args[0];
    var round = parseInt(args[1]);
    var index = parseInt(args[2]);

    var nextRound = round + 1;
    var nextIndex = Math.floor(index/2);

    var targetID = region + ' ' + nextRound + ' ' + nextIndex;

    // for whatever reason, $(#...) isn't working here...
    $(document.getElementById(targetID)).text(name);
    $(document.getElementById('I' + targetID)).val(name);

    // if we've just picked a Final Four guy, also set him in the FF bracket
    if (nextRound === 4) {

        if (region === 'south') {
            nextIndex = 0;
        } else if (region === 'west') {
            nextIndex = 1;
        } else if (region === 'east') {
            nextIndex = 2;
        } else if (region === 'midwest') {
            nextIndex = 3;
        }

        region = 'F';
        var targetID = region + ' ' + nextRound + ' ' + nextIndex;

        

        // for whatever reason, $(#...) isn't working here...
        $(document.getElementById(targetID)).text(name);
        $(document.getElementById('I' + targetID)).val(name);
    }
}
function resetBracketClick() {
    for (var row=1;row<5;row++) {
        for (var x=0;x<[8,4,2,1][row-1];x++) {
            var targetID = 'south ' + row + ' ' + x;
            $(document.getElementById(targetID)).text("[None]");
            $(document.getElementById('I' + targetID)).val("");
            var targetID = 'west ' + row + ' ' + x;
            $(document.getElementById(targetID)).text("[None]");
            $(document.getElementById('I' + targetID)).val("");
            var targetID = 'east ' + row + ' ' + x;
            $(document.getElementById(targetID)).text("[None]");
            $(document.getElementById('I' + targetID)).val("");
            var targetID = 'midwest ' + row + ' ' + x;
            $(document.getElementById(targetID)).text("[None]");
            $(document.getElementById('I' + targetID)).val("");
        }
    }
    for (var row=4;row<7;row++) {
        for (var x=0;x<[4,2,1][row-4];x++) {
            var targetID = 'F ' + row + ' ' + x;
            $(document.getElementById(targetID)).text("[None]");
            $(document.getElementById('I' + targetID)).val("");
        }
    }
}





