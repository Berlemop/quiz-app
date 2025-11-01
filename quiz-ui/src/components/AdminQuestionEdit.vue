<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import quizApiService from "@/services/QuizApiService";
import authStorageService from "@/services/AuthStorageService";

const router = useRouter();
const route = useRoute();

const position = ref(1);
const title = ref('');
const text = ref('');
const image = ref('');
const possibleAnswers = ref([
  { text: '', isCorrect: false },
  { text: '', isCorrect: false },
  { text: '', isCorrect: false },
  { text: '', isCorrect: false }
]);

const isEditMode = ref(false);
const questionId = ref(null);

onMounted(async () => {
  const token = authStorageService.getToken();

  if (!token) {
    router.push('/admin/login');
    return;
  }

  if (route.params.id) {
    isEditMode.value = true;
    questionId.value = route.params.id;

    const response = await quizApiService.getQuestionById(questionId.value, token);

    if (response && response.data) {
      position.value = response.data.position;
      title.value = response.data.title;
      text.value = response.data.text;
      image.value = response.data.image || '';
      possibleAnswers.value = response.data.possibleAnswers;
    }
  }
});

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      image.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}

function setCorrectAnswer(index) {
  possibleAnswers.value.forEach((answer, i) => {
    answer.isCorrect = (i === index);
  });
}

async function saveQuestion() {
  const token = authStorageService.getToken();

  const questionData = {
    position: position.value,
    title: title.value,
    text: text.value,
    image: image.value,
    possibleAnswers: possibleAnswers.value
  };

  if (isEditMode.value) {
    await quizApiService.updateQuestion(questionId.value, questionData, token);
  } else {
    await quizApiService.createQuestion(questionData, token);
  }

  router.push('/admin/questions');
}

function cancel() {
  router.push('/admin/questions');
}

function logout() {
  authStorageService.clearToken();
  router.push('/');
}
</script>

<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>{{ isEditMode ? 'Éditer la question' : 'Créer une question' }}</h1>
      <button @click="logout" class="btn btn-secondary">Déconnexion</button>
    </div>

    <div class="mb-3">
      <label for="position" class="form-label">Position</label>
      <input type="number" v-model="position" class="form-control" id="position" />
    </div>

    <div class="mb-3">
      <label for="title" class="form-label">Titre</label>
      <input type="text" v-model="title" class="form-control" id="title" />
    </div>

    <div class="mb-3">
      <label for="text" class="form-label">Intitulé</label>
      <textarea v-model="text" class="form-control" id="text" rows="3"></textarea>
    </div>

    <div class="mb-3">
      <label for="image" class="form-label">Image</label>
      <input type="file" @change="handleImageUpload" class="form-control" id="image" accept="image/*" />
      <img v-if="image" :src="image" class="img-fluid mt-3" style="max-width: 300px;" />
    </div>

    <h3>Réponses possibles</h3>
    <div v-for="(answer, index) in possibleAnswers" :key="index" class="mb-3">
      <div class="input-group">
        <span class="input-group-text">{{ index + 1 }}</span>
        <input type="text" v-model="answer.text" class="form-control" placeholder="Intitulé de la réponse" />
        <div class="input-group-text">
          <input type="checkbox"
                 :checked="answer.isCorrect"
                 @change="setCorrectAnswer(index)"
                 class="form-check-input mt-0" />
          <label class="ms-2">Correcte</label>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <button @click="saveQuestion" class="btn btn-success me-2">Sauvegarder</button>
      <button @click="cancel" class="btn btn-secondary">Annuler</button>
    </div>
  </div>
</template>
