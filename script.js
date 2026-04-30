const dlForm = document.getElementById('dlForm');
const urlInput = document.getElementById('urlInput');
const preview = document.getElementById('preview');

// 👉 CHANGE THIS to your Railway URL
const API_URL = "https://your-app.up.railway.app";

async function processDownload(url) {
    preview.innerHTML = `
        <div style="color:white">
            ⏳ Processing video...<br>
            <small>Merging audio + video (5–15 sec)</small>
        </div>
    `;

    try {
        const res = await fetch(`${API_URL}/api/download?url=${encodeURIComponent(url)}`);
        const data = await res.json();

        if (data.status !== "success") {
            preview.innerHTML = `<p style="color:red">${data.message}</p>`;
            return;
        }

        preview.innerHTML = `
            <a href="${API_URL}${data.download_url}" 
               style="display:inline-block;margin-top:15px;padding:12px 20px;
               background:#009959;color:#fff;border-radius:10px;text-decoration:none;">
               ⬇ Download HD Video (With Sound)
            </a>
        `;

    } catch (err) {
        preview.innerHTML = `<p style="color:red">Server error</p>`;
    }
}

dlForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const url = urlInput.value.trim();

    if (!url) return alert("Paste URL");

    processDownload(url);
});