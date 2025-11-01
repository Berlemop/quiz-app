<script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import quizApiService from "@/services/QuizApiService";
  import authStorageService from "@/services/AuthStorageService";
  import QuestionsList from "../components/QuestionList.vue";
  import QuestionAdminDisplay from "../components/QuestionAdminDisplay.vue";
  import QuestionEdition from "../components/QuestionEdition.vue";

  const router = useRouter();
  const token = ref('');
  const password = ref('');
  const errorMessage = ref('');
  const adminMode = ref('list');
  const selectedQuestionId = ref(null);
  const questionsListRef = ref(null);

  onMounted(() => {
    token.value = authStorageService.getToken();
    if (token.value) {
      adminMode.value = 'list';
    }
  });

  async function login() {
    errorMessage.value = '';

    const response = await quizApiService.login(password.value);

    if (response && response.status === 200 && response.data.token) {
      authStorageService.saveToken(response.data.token);
      token.value = response.data.token;
      adminMode.value = 'list';
    } else {
      errorMessage.value = 'Mauvais mot de passe';
    }
  }

  function logout() {
    authStorageService.clearToken();
    token.value = '';
    password.value = '';
    router.push('/');
  }

  function viewQuestion(questionId) {
    selectedQuestionId.value = questionId;
    adminMode.value = 'display';
  }

  function editQuestion(questionId) {
    selectedQuestionId.value = questionId;
    adminMode.value = 'edit';
  }

  function createQuestion() {
    selectedQuestionId.value = null;
    adminMode.value = 'edit';
  }

  function backToList() {
    adminMode.value = 'list';
    selectedQuestionId.value = null;
    if (questionsListRef.value) {
      questionsListRef.value.loadQuestions();
    }
  }

  function handleSaveSuccess() {
    backToList();
  }

  function handleCancel() {
    backToList();
  }
</script>

<template>
  <div class="container">
    <!--si pas de token form admin-->
    <div v-if="!token">
      <h1>Administration - Connexion</h1>

      <div>
        <label for="password" class="form-label">Mot de passe</label>
        <input type="password"
               v-model="password"
               class="form-control"
               id="password"
               @keyup.enter="login" />
      </div>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>

      <button @click="login" class="btn btn-primary">Connexion</button>
    </div>

    <!--si token vue admin-->
    <div v-else>
      <div >
        <h1>Administration</h1>
        <button @click="logout" class="btn btn-secondary">Déconnexion</button>
      </div>

      <QuestionsList v-if="adminMode === 'list'"
                     ref="questionsListRef"
                     @view-question="viewQuestion"
                     @edit-question="editQuestion"
                     @create-question="createQuestion"
                     @delete-question="backToList" />

      <QuestionAdminDisplay v-if="adminMode === 'display'"
                            :questionId="selectedQuestionId"
                            @edit-question="editQuestion"
                            @back-to-list="backToList" />

      <QuestionEdition v-if="adminMode === 'edit'"
                       :questionId="selectedQuestionId"
                       @save-success="handleSaveSuccess"
                       @cancel="handleCancel" />
    </div>
  </div>
</template>
