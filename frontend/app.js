document.getElementById("shipmateForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const requestText = document.getElementById("request").value;
  document.getElementById("responseBox").innerText = "Shipmate is thinking...";
  const response = await fetch("http://localhost:8000/shipmate/respond", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input: requestText })
  });
  const data = await response.json();
  document.getElementById("responseBox").innerText = data.response || "No response received.";
});