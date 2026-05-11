// Mock drawing data - replace with real API call later
const mockDrawings = [
    {
        id: 1,
        artist: "ArtistOne",
        prompt: "Dragon working at McDonald's",
        rating: 4.8,
        image: "https://via.placeholder.com/300x200",
        date: "2026-05-05"
    },
    {
        id: 2,
        artist: "SketchMaster",
        prompt: "Dragon working at McDonald's",
        rating: 4.5,
        image: "https://via.placeholder.com/300x200",
        date: "2026-05-05"
    },
    {
        id: 3,
        artist: "DoodleFan",
        prompt: "Dragon working at McDonald's",
        rating: 4.2,
        image: "https://via.placeholder.com/300x200",
        date: "2026-05-05"
    },
    {
        id: 4,
        artist: "PixelArtist",
        prompt: "Cat flying a plane",
        rating: 4.9,
        image: "https://via.placeholder.com/300x200",
        date: "2026-05-04"
    },
    {
        id: 5,
        artist: "CreativeGenius",
        prompt: "Robot on holiday",
        rating: 4.6,
        image: "https://via.placeholder.com/300x200",
        date: "2026-05-03"
    }
];

let filteredDrawings = [...mockDrawings];

function populateFilters() {
    const prompts = [...new Set(mockDrawings.map(d => d.prompt))];
    const promptSelect = document.getElementById("promptSelect");
    promptSelect.innerHTML = '<option value="">All Prompts</option>';
    prompts.forEach(prompt => {
        const option = document.createElement("option");
        option.value = prompt;
        option.textContent = prompt;
        promptSelect.appendChild(option);
    });

    const dates = [...new Set(mockDrawings.map(d => d.date))].sort().reverse();
    const dateSelect = document.getElementById("dateSelect");
    dateSelect.innerHTML = '<option value="">All Dates</option>';
    dates.forEach(date => {
        const option = document.createElement("option");
        option.value = date;
        option.textContent = date;
        dateSelect.appendChild(option);
    });
}

function renderGallery() {
    const gallery = document.getElementById("drawingGallery");
    gallery.innerHTML = "";

    if (filteredDrawings.length === 0) {
        gallery.innerHTML = '<div class="col-12"><p class="text-center text-muted">No drawings found</p></div>';
        return;
    }

    filteredDrawings.forEach(drawing => {
        const card = document.createElement("div");
        card.className = "col-md-4";
        card.innerHTML = `
            <div class="card">
                <img src="${drawing.image}" class="card-img-top" alt="drawing">
                <div class="card-body">
                    <h5 class="card-title">${drawing.artist}</h5>
                    <p class="card-text">Prompt: ${drawing.prompt}</p>
                    <p class="card-text">Rating: ${drawing.rating}</p>
                </div>
            </div>
        `;
        gallery.appendChild(card);
    });
}

function applyFilters() {
    const promptFilter = document.getElementById("promptSelect").value;
    const dateFilter = document.getElementById("dateSelect").value;

    filteredDrawings = mockDrawings.filter(drawing => {
        const matchesPrompt = !promptFilter || drawing.prompt === promptFilter;
        const matchesDate = !dateFilter || drawing.date === dateFilter;
        return matchesPrompt && matchesDate;
    });

    renderGallery();
}

document.addEventListener("DOMContentLoaded", () => {
    populateFilters();
    renderGallery();
    document.getElementById("promptSelect").addEventListener("change", applyFilters);
    document.getElementById("dateSelect").addEventListener("change", applyFilters);
});
