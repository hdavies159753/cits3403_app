const voteBtn = document.querySelector(".vote-btn")
voteBtn.addEventListener("click", () => {
    const drawingId = voteBtn.dataset.drawingId;
    fetch("/vote", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            drawing_id: drawingId
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            const votewCount = document.getElementById(
                'vote-count-$(drawingId)'
            );
            votewCount.textContent = data.vote_count;
        }
    })
    .catch(error => {
        console.error(error);
        alert("Error submitting!")
    });
});