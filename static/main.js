let dateJson = null
let dateList = null

const CURRENT_MONTH = "current_month"
const NEXT_MONTH = "next_month"
let monthSelection = NEXT_MONTH


function updateList(arr) {
    while (dateList.firstChild) {
        dateList.firstChild.remove()
    }

    arr.forEach((date) => {
        const dateItem = document.createElement("li")
        dateItem.textContent = date
        dateList.appendChild(dateItem)
    })
}


async function getAvailability() {
    const loadingItem = document.createElement("li")
    loadingItem.textContent = "Loading..."
    dateList.appendChild(loadingItem)

    await fetch('/availability')
        .then(response => response.json())
        .then(json => {
            dateList.removeChild(loadingItem)
            dateJson = json
        })   

}


document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector("#nextButton")
    const currentButton = document.querySelector("#currentButton")

    nextButton.addEventListener("click", function() {
        if(monthSelection != NEXT_MONTH) {
            monthSelection = NEXT_MONTH

            if (dateJson != null) {
                updateList(dateJson[monthSelection])
            }

            nextButton.disabled = true
            currentButton.disabled = false
        }
    })

    currentButton.addEventListener("click", function() {
        if(monthSelection != CURRENT_MONTH) {
            monthSelection = CURRENT_MONTH

            if (dateJson != null) {
                updateList(dateJson[monthSelection])
            }

            currentButton.disabled = true
            nextButton.disabled = false
        }
    })

    dateList = document.querySelector("#dateList")

    getAvailability().then(() => {
        updateList(dateJson[monthSelection])
        }
    )
}, false)
