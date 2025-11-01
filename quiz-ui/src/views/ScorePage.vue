<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

const router = useRouter();
const playerName = ref('');
const score = ref(0);
const totalQuestions = ref(0);
const allScores = ref([]);
const playerRank = ref(0);

onMounted(async () => {
  console.log("Score Page mounted");

  playerName.value = participationStorageService.getPlayerName();
  score.value = parseInt(participationStorageService.getParticipationScore());

  const quizInfo = await quizApiService.getQuizInfo();

  if (quizInfo && quizInfo.data) {
    totalQuestions.value = quizInfo.data.size;
    allScores.value = quizInfo.data.scores;

    let rank = 1;
    for (let i = 0; i < allScores.value.length; i++) {
      if (allScores.value[i].score > score.value) {
        rank++;
      }
    }
    playerRank.value = rank;
  }
});

function goHome() {
  participationStorageService.clear();
  router.push('/');
}
</script>

<template>
  <div class="container">
    <h1>Résultat du Quiz</h1>

    <div class="card mb-4">
      <div class="card-body text-center">
        <h2 class="card-title">Félicitations {{ playerName }} !</h2>
        <p class="card-text display-4">{{ score }} / {{ totalQuestions }}</p>
        <p class="card-text">Votre classement : {{ playerRank }}{{ playerRank === 1 ? 'er' : 'ème' }}</p>
      </div>
    </div>

    <h2>Meilleurs scores</h2>
    <div class="list-group mb-4">
      <div v-for="(scoreEntry, index) in allScores"
           :key="index"
           class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ index + 1 }}. {{ scoreEntry.playerName }}</span>
        <span class="badge bg-primary rounded-pill">{{ scoreEntry.score }}</span>
      </div>
    </div>

    <button @click="goHome" class="btn btn-primary">Retour à l'accueil</button>
  </div>
</template>
