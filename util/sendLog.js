function sendLog(logData, url) {
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(logData),
  })
    .then((response) => response.json())
    .then((data) => console.log("Log sent", data))
    .catch((error) => console.error("Error sending log", error));
}

function sendLogToTeddify(logData) {
  sendLog(logData, "https://teddify.co/api/nesterlog");
}
