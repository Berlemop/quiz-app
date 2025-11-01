export default {
  clear() {
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
    return window.localStorage.getItem("participationScore");
  },
  saveAnswers(answers) {
    window.localStorage.setItem("answers", JSON.stringify(answers));
  },
  getAnswers() {
    const answers = window.localStorage.getItem("answers");
    return answers ? JSON.parse(answers) : [];
  }
};
