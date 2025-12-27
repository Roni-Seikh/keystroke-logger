let logging = false;

function toggleLogging() {
    logging = !logging;
    document.getElementById("status").textContent =
        logging ? "Logging ON" : "Logging OFF";
}

document.getElementById("inputBox").addEventListener("keydown", (e) => {
    if (!logging) return;

    fetch("/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key: e.key })
    });
});
