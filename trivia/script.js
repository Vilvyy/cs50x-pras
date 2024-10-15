// Multiple Choice Question Logic
document.querySelectorAll('.choice').forEach(button => {
    button.addEventListener('click', function() {
        const isCorrect = this.getAttribute('data-correct') === 'true';
        const resultText = document.getElementById('multiple-choice-result');

        if (isCorrect) {
            this.classList.add('correct');
            resultText.textContent = "Correct!";
            resultText.style.color = "green";
        } else {
            this.classList.add('incorrect');
            resultText.textContent = "Incorrect";
            resultText.style.color = "red";
        }
    });
});

// Free Response Question Logic
document.getElementById('submit-response').addEventListener('click', function() {
    const responseInput = document.getElementById('response-input');
    const resultText = document.getElementById('free-response-result');
    const correctAnswer = "8"; // Correct answer for the square root question

    if (responseInput.value.trim() === correctAnswer) {
        responseInput.classList.add('correct');
        resultText.textContent = "Correct!";
        resultText.style.color = "green";
    } else {
        responseInput.classList.add('incorrect');
        resultText.textContent = "Incorrect";
        resultText.style.color = "red";
    }
});
