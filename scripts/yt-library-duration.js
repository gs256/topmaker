// Calculates the total duration of your youtube starred audio tracks
// Go to https://studio.youtube.com/channel/[your_channel]/music -> Starred and run this script in the console

var es = document.querySelectorAll(
    ".style-scope.ytmus-starred-table .cell-body.style-scope.ytmus-library-row"
)
var timeStrings = []

for (e of es) {
    var text = e.textContent
    if (text.includes(":") && text.length < 8) {
        timeStrings.push(text)
    }
}

var times = []
for (timestr of timeStrings) {
    let [mins, secs] = timestr.split(":")
    var t = parseInt(mins) * 60 + parseInt(secs)
    times.push(t)
}

console.log(times)
var sum = times.reduce((r, a) => r + a, 0)

console.log("In seconds:", sum)
console.log("In minutes:", Math.floor(sum / 60) + ":" + (sum % 60))
