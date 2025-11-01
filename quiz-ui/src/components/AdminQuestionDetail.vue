<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import quizApiService from "@/services/QuizApiService";
import authStorageService from "@/services/AuthStorageService";

const router = useRouter();
const route = useRoute();
const question = ref(null);

onMounted(async () => {
  const token = authStorageService.getToken();

  if (!token) {
    router.push('/admin/login');
    return;
  }

  const questionId = route.params.id;
  const response = await quizApiService.getQuestionById(questionId, token);

  if (response && response.data) {
    question.value = response.data;
  }
});

function editQuestion() {
  router.push('/admin/questions/' + question.value.id + '/edit');
}

async function deleteQuestion() {
  if (confirm('Voulez-vous vraiment supprimer cette question ?')) {
    const token = authStorageService.getToken();
    await quizApiService.deleteQuestion(question.value.id, token);
    router.push('/admin/questions');
  }
}

function logout() {
  authStorageService.clearToken();
  router.push('/');
}

function goBack() {
  router.push('/admin/questions');
}
</script>

<template>
  <div class="container" v-if="question">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Détail de la question</h1>
      <button @click="logout" class="btn btn-secondary">Déconnexion</button>
    </div>

    <div class="mb-3">
      <button @click="editQuestion" class="btn btn-warning me-2">Éditer</button>
      <button @click="deleteQuestion" class="btn btn-danger me-2">Supprimer</button>
      <button @click="goBack" class="btn btn-secondary">Retour</button>
    </div>

    <div class="card">
      <div class="card-body">
        <h2 class="card-title">{{ question.title }}</h2>
        <p class="card-text">{{ question.text }}</p>
        <img v-if="question.image" :src="question.image" class="img-fluid mb-3" />

        <h3>Réponses possibles :</h3>
        <ul class="list-group">
          <li v-for="(answer, index) in question.possibleAnswers"
              :key="index"
              class="list-group-item">
            {{ answer.text }}
            <span v-if="answer.isCorrect" class="badge bg-success ms-2">Correcte</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
