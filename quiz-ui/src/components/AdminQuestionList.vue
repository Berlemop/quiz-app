<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from "@/services/QuizApiService";
import authStorageService from "@/services/AuthStorageService";

const router = useRouter();
const questions = ref([]);

onMounted(async () => {
  const token = authStorageService.getToken();

  if (!token) {
    router.push('/admin/login');
    return;
  }

  await loadQuestions();
});

async function loadQuestions() {
  const token = authStorageService.getToken();
  const response = await quizApiService.getAllQuestions(token);

  if (response && response.data) {
    questions.value = response.data;
  }
}

function logout() {
  authStorageService.clearToken();
  router.push('/');
}

function goToQuestionDetail(questionId) {
  router.push('/admin/questions/' + questionId);
}

function createQuestion() {
  router.push('/admin/questions/create');
}
</script>

<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Liste des questions</h1>
      <button @click="logout" class="btn btn-secondary">Déconnexion</button>
    </div>

    <button @click="createQuestion" class="btn btn-success mb-3">Créer une question</button>

    <div class="list-group">
      <a v-for="question in questions"
         :key="question.id"
         @click="goToQuestionDetail(question.id)"
         class="list-group-item list-group-item-action">
        Position {{ question.position }} - {{ question.title }}
      </a>
    </div>
  </div>
</template>
