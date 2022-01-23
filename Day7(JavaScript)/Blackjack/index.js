let player = {
    name: "9qlina",
    chips: 200
}

let amountlose = 0

let cards = []
let total = 0
let addbetposs = false
let hasBlackJack = false
let stopu = false
let isAlive = false
let bigpot = 0
let robottot = 0

let messageEl = document.getElementById("message-el")
let sumEl = document.getElementById("sum-el")
let cardsEl = document.getElementById("cards-el")
let playerEl = document.getElementById("player-el")
let potEl = document.getElementById("pot-el")

playerEl.textContent = player.name + ": $" + player.chips

function startGame(){
    stopu = false
    bigpot = 0
    robottot = 0 
    let first = firstgetCard()
    let second = firstgetCard()
    cards = [first,second]
    total = first + second
    isAlive = true
    playerEl.textContent = player.name + ": $" + player.chips
    potEl.textContent = "Pot: " + bigpot
    renderGame()
}

function firstgetCard(){
    let randomnum = Math.floor(Math.random()*13) +1
    if (randomnum > 10) {
        return 10
    } else if (randomnum === 1) {
        return 11
    } else {
        return randomnum
    }
}

function renderGame(){
    cardsEl.textContent  = "Cards: "
    for (let i = 0; i < cards.length; i++) {
        cardsEl.textContent += cards[i] + " "
    }
    sumEl.textContent = "Sum: " + total

    // Determine the hand by increment card
    if (total <= 20) {
        message = "Do you want to draw a new card?"
        addbetposs = true
    } else if (total === 21) {
        message = "You've got Blackjack!"
        hasBlackJack = true
        addbetposs = false
        player.chips += bigpot
    } else {
        message = "You're out of the game!"
        isAlive = false
        addbetposs = false
    }

    if (stopu == true){
        if (robottot > total){
            message = "You're out of the game! Dealer beat you at: " + robottot
            isAlive = false
            addbetposs = false
        }
        else{
            message = "You've beat the dealer! Dealer is at: " + robottot
            player.chips += bigpot*2
            isAlive = false
        }
    }
    playerEl.textContent = player.name + ": $" + player.chips
    messageEl.textContent = message
}

function newCard() {
    if (isAlive === true && hasBlackJack === false) {
        let card = firstgetCard()
        total += card
        cards.push(card)
        renderGame()        
    }
}

function addBet(){
    if (addbetposs == true){
        player.chips -= 20
        bigpot += 20
        playerEl.textContent = player.name + ": $" + player.chips
        potEl.textContent = "Pot: " + bigpot
    }
}

function stop(){
    let robot1 = firstgetCard()
    let robot2 = firstgetCard()
    robottot = robot1 + robot2
    stopu = true
    while (robottot < 18){
        robottot += firstgetCard()
    }
    renderGame()
}
