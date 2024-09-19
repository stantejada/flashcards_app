const card = document.getElementById('card-container');
const flipButton = document.getElementById('flip-btn');

flipButton.addEventListener('click', function () {
    card.classList.toggle('flipped'); // Flip the card

    // Update button text based on the flipped state
    if (card.classList.contains('flipped')) {
        flipButton.innerText = 'Show Question';
    } else {
        flipButton.innerText = 'Show Answer';
    }
});

