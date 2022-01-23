//document.getElementById("count-el").innerText = 5
let count = 0 
let countshow = document.getElementById("count-el")
let saveshow = document.getElementById("save-el")

function increment(){
    count = count + 1 
    countshow.innerText = count
}

function save(){
    saveshow.textContent += " " + count + " -"
    count = 0
    countshow.innerText = count
}
