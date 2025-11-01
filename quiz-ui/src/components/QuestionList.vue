<script setup>
  import { ref, onMounted } from 'vue';
  import quizApiService from "@/services/QuizApiService";
  import authStorageService from "@/services/AuthStorageService";

  const emit = defineEmits(['edit-question', 'view-question', 'create-question', 'delete-question']);
  const questions = ref([]);

  onMounted(async () => {
    await loadQuestions();
  });

  async function loadQuestions() {
    const token = authStorageService.getToken();
    const response = await quizApiService.getAllQuestions(token);

    if (response && response.data) {
      questions.value = response.data;
    }
  }

  function viewQuestion(questionId) {
    emit('view-question', questionId);
  }

  function createQuestion() {
    emit('create-question');
  }

  async function deleteQuestion(questionId) {
    if (confirm('Voulez-vous vraiment supprimer cette question ?')) {
      const token = authStorageService.getToken();
      await quizApiService.deleteQuestion(questionId, token);
      await loadQuestions();
      emit('delete-question');
    }
  }

  defineExpose({ loadQuestions });
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Liste des questions</h1>
      <button @click="createQuestion" class="btn btn-success">Créer une question</button>
    </div>

    <div class="list-group">
      <div v-for="question in questions"
           :key="question.id"
           class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <span @click="viewQuestion(question.id)" style="cursor: pointer; flex: 1;">
            Position {{ question.position }} - {{ question.title }}
          </span>
          <button @click="deleteQuestion(question.id)" class="btn btn-danger btn-sm">Supprimer</button>
        </div>
      </div>
    </div>

    <div v-if="questions.length === 0" class="alert alert-info mt-3">
      Aucune question créée pour le moment.
    </div>
  </div>
</template>
