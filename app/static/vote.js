const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

const voteBtn = document.querySelector(".vote-btn");
if (voteBtn) {
voteBtn.addEventListener("click", () => {
    const drawingId = voteBtn.dataset.drawingId;
    fetch("/vote", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            drawing_id: drawingId
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            const voteCount = document.getElementById(
                `vote-count-${drawingId}`
            );
            voteCount.textContent = data.vote_count;
            voteBtn.disabled = true;
            voteBtn.textContent = "Voted";
            voteBtn.classList.remove("btn-primary");
            voteBtn.classList.add("btn-success");
        }
    })
    .catch(error => {
        console.error(error);
        alert("Error voting!");
    });
});
}