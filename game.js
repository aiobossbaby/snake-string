const tg = window.Telegram.WebApp;
tg.expand(); // Expand full screen

const user = tg.initDataUnsafe.user || { id: 0, first_name: "Guest" };
document.getElementById("playerName").textContent = user.first_name;

let position = 0;
const ladders = { 3: 22, 5: 8, 11: 26, 20: 29 };
const snakes = { 27: 1, 21: 9, 17: 4, 19: 7 };

function rollDice() {
  const roll = Math.floor(Math.random() * 6) + 1;
  let newPos = position + roll;
  let msg = `🎲 Rolled: ${roll}\n`;

  if (newPos in ladders) {
    msg += `🪜 Ladder! ${newPos} → ${ladders[newPos]}\n`;
    newPos = ladders[newPos];
  } else if (newPos in snakes) {
    msg += `🐍 Snake! ${newPos} → ${snakes[newPos]}\n`;
    newPos = snakes[newPos];
  }

  if (newPos >= 30) {
    msg += `🏁 Finished! You win!\n`;
    sendScore(roll);
    newPos = 30;
  }

  position = newPos;
  document.getElementById("position").textContent = position;
  alert(msg);
}

function sendScore(score) {
  fetch("https://your-server.com/api/save-score", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      id: user.id,
      name: user.first_name,
      score: score
    })
  });
}

document.getElementById("rollBtn").addEventListener("click", rollDice);