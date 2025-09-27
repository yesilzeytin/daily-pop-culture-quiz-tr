let questions = [];
let current = 0;
let score = 0;

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
    // 7% chance to append " Belediyesİ"
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

  if (selectedIdx === correctIdx) score++;
  document.getElementById("next").style.display = "block";
}

function nextQuestion() {
  current++;
  if (current < questions.length) {
    showQuestion();
  } else {
    document.getElementById("quiz").innerHTML = `
      <h2>Skorunuz: ${score} / ${questions.length}</h2>
      <p>Yeni sorular için yarın yeniden uğra!</p>
    `;
  }
}

window.onload = loadQuestions;
