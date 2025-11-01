<script setup>
  import { defineProps, defineEmits } from 'vue';

  const props = defineProps({
    question: Object
  });

  const emit = defineEmits(['answer-clicked']);
</script>

<template>
  <div class="container">
    <h2>{{ question.title }}</h2>
    <p>{{ question.text }}</p>
    <img v-if="question.image" :src="question.image" class="img-fluid mb-3" />

    <div class="list-group">
      <a v-for="(answer, index) in question.possibleAnswers"
         :key="index"
         @click="emit('answer-clicked', index)"
         class="list-group-item list-group-item-action">
        {{ answer.text }}
      </a>
    </div>
  </div>
</template>
