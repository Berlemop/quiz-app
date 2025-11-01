<script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import participationStorageService from "@/services/ParticipationStorageService";

  const router = useRouter();
  const username = ref('');

  onMounted(() => {
    console.log("New Quiz Page mounted");
  });

  function launchNewQuiz() {
    console.log("Launch new quiz with", username.value);
    participationStorageService.savePlayerName(username.value);
    router.push('/questions');
  }
</script>

<template>
  <div class="container">
    <h1>Nouveau Quiz</h1>
    <p>Nom du joueur</p>
    <input type="text" v-model="username" class="form-control mb-3" />
    <button @click="launchNewQuiz" class="btn btn-primary">Démarrer</button>
  </div>
</template>
