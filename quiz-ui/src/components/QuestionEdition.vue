<script setup>
  import { ref, onMounted, watch } from 'vue';
  import quizApiService from "@/services/QuizApiService";
  import authStorageService from "@/services/AuthStorageService";
  import ImageUpload from "../components/ImageUpload.vue";

  const props = defineProps(['questionId']);
  const emit = defineEmits(['save-success', 'cancel']);

  const position = ref(1);
  const title = ref('');
  const text = ref('');
  const imageAsb64 = ref('');
  const possibleAnswers = ref([
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false }
  ]);

  const isEditMode = ref(false);

  onMounted(async () => {
    if (props.questionId) {
      isEditMode.value = true;
      await loadQuestion();
    }
  });

  watch(() => props.questionId, async (newValue) => {
    if (newValue) {
      isEditMode.value = true;
      await loadQuestion();
    } else {
      resetForm();
    }
  });

  async function loadQuestion() {
    const token = authStorageService.getToken();
    const response = await quizApiService.getQuestionById(props.questionId, token);

    if (response && response.data) {
      const questionData = response.data;
      position.value = questionData.position;
      title.value = questionData.title;
      text.value = questionData.text;
      imageAsb64.value = questionData.image || '';
      possibleAnswers.value = [...questionData.possibleAnswers];
    }
  }

  function resetForm() {
    isEditMode.value = false;
    position.value = 1;
    title.value = '';
    text.value = '';
    imageAsb64.value = '';
    possibleAnswers.value = [
      { text: '', isCorrect: false },
      { text: '', isCorrect: false },
      { text: '', isCorrect: false },
      { text: '', isCorrect: false }
    ];
  }

  function imageFileChangedHandler(b64String) {
    imageAsb64.value = b64String;
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
      image: imageAsb64.value,
      possibleAnswers: possibleAnswers.value
    };

    if (isEditMode.value) {
      await quizApiService.updateQuestion(props.questionId, questionData, token);
    } else {
      await quizApiService.createQuestion(questionData, token);
    }

    emit('save-success');
  }

  function cancel() {
    emit('cancel');
  }
</script>

<template>
  <div>
    <h1>{{ isEditMode ? 'Éditer la question' : 'Créer une question' }}</h1>

    <div>
      <label for="position" class="form-label">Position</label>
      <input type="number" v-model="position" class="form-control" id="position" />
    </div>

    <div>
      <label for="title" class="form-label">Titre</label>
      <input type="text" v-model="title" class="form-control" id="title" />
    </div>

    <div>
      <label for="text" class="form-label">Intitulé</label>
      <textarea v-model="text" class="form-control" id="text" rows="3"></textarea>
    </div>

    <div >
      <label class="form-label">Image</label>
      <ImageUpload @file-change="imageFileChangedHandler" :fileDataUrl="imageAsb64" />
      <img v-if="imageAsb64" :src="imageAsb64" class="img-fluid mt-3" style="max-width: 300px;" />
    </div>

    <h3>Réponses possibles</h3>
    <div v-for="(answer, index) in possibleAnswers" :key="index" >
      <div class="input-group">
        <span class="input-group-text">{{ index + 1 }}</span>
        <input type="text" v-model="answer.text" class="form-control" placeholder="Intitulé de la réponse" />
        <div class="input-group-text">
          <input type="checkbox"
                 :checked="answer.isCorrect"
                 @change="setCorrectAnswer(index)"
                 class="form-check-input mt-0" />
          <label >Correcte</label>
        </div>
      </div>
    </div>

    <div >
      <button @click="saveQuestion" class="btn btn-success">Sauvegarder</button>
      <button @click="cancel" class="btn btn-secondary">Annuler</button>
    </div>
  </div>
</template>
