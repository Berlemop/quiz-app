<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from "@/services/QuizApiService";
import authStorageService from "@/services/AuthStorageService";

const router = useRouter();
const password = ref('');
const errorMessage = ref('');

async function login() {
  errorMessage.value = '';

  const response = await quizApiService.login(password.value);

  if (response && response.status === 200 && response.data.token) {
    authStorageService.saveToken(response.data.token);
    router.push('/admin/questions');
  } else {
    errorMessage.value = 'Mauvais mot de passe';
  }
}
</script>

<template>
  <div class="container">
    <h1>Administration - Connexion</h1>

    <div class="mb-3">
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
</template>
