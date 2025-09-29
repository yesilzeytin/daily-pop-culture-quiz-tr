let questions = [];
let current = 0;
let score = 0;
let answers = []; // store per-question results (true/false)

async function loadQuestions() {
  const res = await fetch("questions.json");
  const data = await res.json();
  questions = data.questions;
  showQuestion();
}

function showQuestion() {
  const q = questions[current];
  document.getElementById("question").textContent = q.question;
  const optionsDiv = document.getElementById("options");
  optionsDiv.innerHTML = "";

  q.options.forEach((opt, idx) => {
    // 7% chance to append "Belediyesi"
    if (Math.random() < 0.07) {
      opt += " Belediyesi";
    }

    const btn = document.createElement("button");
    btn.textContent = opt;
    btn.onclick = () => checkAnswer(btn, idx, q.correct);
    optionsDiv.appendChild(btn);
  });

  document.getElementById("next").style.display = "none";
}

function checkAnswer(selectedBtn, selectedIdx, correctIdx) {
  const buttons = document.querySelectorAll("#options button");
  buttons.forEach((btn, idx) => {
    btn.disabled = true;
    if (idx === correctIdx) btn.classList.add("correct");
    if (idx === selectedIdx && idx !== correctIdx) btn.classList.add("incorrect");
  });

  const result = (selectedIdx === correctIdx);
  answers.push(result);

  if (result) score++;
  document.getElementById("next").style.display = "block";
}

function nextQuestion() {
  current++;
  if (current < questions.length) {
    showQuestion();
  } else {
    showResult();
  }
}

function showResult() {
  const today = new Date().toISOString().split("T")[0];
  let shareText = `Daily Chip Quiz ${today} ${score}/${questions.length}\n\n`;

  // build emoji line
  answers.forEach(correct => {
    shareText += correct ? "🟩" : "⬛";
  });
  shareText += "\n";

  document.getElementById("quiz").innerHTML = `
    <h2>Your Score: ${score} / ${questions.length}</h2>
    <p>Come back tomorrow for new questions!</p>
    <button onclick="shareResult(\`${shareText}\`)">📋 Share</button>
  `;
}

function shareResult(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert("✅ Result copied to clipboard! Paste it anywhere to share.");
  }).catch(err => {
    alert("❌ Failed to copy result: " + err);
  });
}

window.onload = loadQuestions;
