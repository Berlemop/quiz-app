<script setup>
  import { ref, onMounted } from 'vue';
  import quizApiService from "@/services/QuizApiService";

  const registeredScores = ref([]);

  onMounted(async () => {
    console.log("Home page mounted");

    const response = await quizApiService.getQuizInfo();

    if (response && response.data) {
      registeredScores.value = response.data.scores;
    }
  });
</script>

<template>
  <div class="container">
    <h1>Quiz Application</h1>

    <div class="text-center my-5">
      <router-link to="/new-quiz" class="btn btn-primary btn-lg">Démarrer le quiz !</router-link>
    </div>

    <h2>Meilleurs scores</h2>
    <div class="list-group">
      <div v-for="(scoreEntry, index) in registeredScores"
           :key="scoreEntry.date"
           class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ index + 1 }}. {{ scoreEntry.playerName }}</span>
        <span class="badge bg-primary rounded-pill">{{ scoreEntry.score }}</span>
      </div>
    </div>

    <div v-if="registeredScores.length === 0" class="alert alert-info mt-3">
      Aucun score enregistré pour le moment. Soyez le premier à participer !
    </div>
  </div>
</template>
