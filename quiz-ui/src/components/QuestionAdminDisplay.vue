<script setup>
  import { ref, onMounted, watch } from 'vue';
  import quizApiService from "@/services/QuizApiService";
  import authStorageService from "@/services/AuthStorageService";

  const props = defineProps(['questionId']);
  const emit = defineEmits(['edit-question', 'back-to-list']);

  const question = ref(null);

  onMounted(async () => {
    await loadQuestion();
  });

  watch(() => props.questionId, async () => {
    if (props.questionId) {
      await loadQuestion();
    }
  });

  async function loadQuestion() {
    const token = authStorageService.getToken();
    const response = await quizApiService.getQuestionById(props.questionId, token);

    if (response && response.data) {
      question.value = response.data;
    }
  }

  function editQuestion() {
    emit('edit-question', props.questionId);
  }

  function goBack() {
    emit('back-to-list');
  }
</script>

<template>
  <div v-if="question">
    <div>
      <h1>Détail de la question</h1>
      <div>
        <button @click="editQuestion" class="btn btn-warning me-2">Éditer</button>
        <button @click="goBack" class="btn btn-secondary">Retour</button>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <h2 class="card-title">{{ question.title }}</h2>
        <p class="card-text"><strong>Position :</strong> {{ question.position }}</p>
        <p class="card-text">{{ question.text }}</p>
        <img v-if="question.image" :src="question.image" class="img-fluid" />

        <h3>Réponses possibles :</h3>
        <ul class="list-group">
          <li v-for="(answer, index) in question.possibleAnswers"
              :key="index"
              class="list-group-item">
            {{ answer.text }}
            <span v-if="answer.isCorrect" class="badge bg-success">✓ Correcte</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
