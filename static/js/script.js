document.getElementById('review-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    console.log("Form submitted");

    const review = document.getElementById('review').value.trim();
    const resultSection = document.getElementById('result-section');
    const resultText = document.getElementById('result-text');
    const resultDescription = document.getElementById('result-description');

    // Reset visibility and text
    resultSection.hidden = true;
    resultText.textContent = '';
    if (resultDescription) resultDescription.textContent = '';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ review: review })
        });

        const data = await response.json();
        console.log(data);

        if (data.sentiment && data.confidence !== undefined) {
            const sentiment = data.sentiment;
            const confidence = data.confidence;

            resultText.textContent = `${sentiment} (Confidence: ${confidence})`;

            // Add a contextual description
            if (resultDescription) {
                if (sentiment.includes("Positive")) {
                    resultDescription.textContent = "This review was considered positive because it expresses satisfaction or optimism.";
                } else if (sentiment.includes("Negative")) {
                    resultDescription.textContent = "This review was marked negative due to signs of dissatisfaction or negative tone.";
                }
            }

            // Show with fade-in effect
            resultSection.hidden = false;
            resultSection.style.opacity = 0;
            setTimeout(() => resultSection.style.opacity = 1, 100);
        } else {
            resultText.textContent = 'An error occurred.';
            resultSection.hidden = false;
            resultSection.style.opacity = 1;
        }

    } catch (err) {
        console.error("Fetch failed:", err);
        resultText.textContent = 'An error occurred while connecting to the server.';
        resultSection.hidden = false;
        resultSection.style.opacity = 1;
    }
});
