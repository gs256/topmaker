// Script to manually query images from Yandex
// Go to https://yandex.ru/images/, scroll to the very bottom and paste this script to the console

var elements = document.querySelectorAll(".serp-item__thumb.justifier__thumb")
var result = []

var i = 1
for (e of elements) {
    result.push({ thumbnail: e.src, page: 0, position: i })
    i += 1
}

console.log("length: ", result.length)
console.log(JSON.stringify({ items: result }))
