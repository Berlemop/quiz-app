<script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import QuestionDisplay from "../components/QuestionDisplay.vue";
  import quizApiService from "@/services/QuizApiService";
  import participationStorageService from "@/services/ParticipationStorageService";

  const router = useRouter();
  const currentQuestion = ref(null);
  const currentQuestionPosition = ref(1);
  const totalNumberOfQuestion = ref(0);
  const userAnswers = ref([]);

  onMounted(async () => {
    console.log("Questions Manager mounted");

    participationStorageService.saveAnswers([]);

    const quizInfo = await quizApiService.getQuizInfo();
    if (quizInfo && quizInfo.data) {
      totalNumberOfQuestion.value = quizInfo.data.size;
      userAnswers.value = new Array(quizInfo.data.size).fill(null);
    }
    await loadQuestionByPosition(1);
  });

  async function loadQuestionByPosition(position) {
    const response = await quizApiService.getQuestion(position);
    if (response && response.data) {
      currentQuestion.value = response.data;
      currentQuestionPosition.value = position;
    }
  }

  async function answerClickedHandler(answerPosition) {
    console.log("Answer clicked:", answerPosition);

    userAnswers.value[currentQuestionPosition.value - 1] = answerPosition;
    participationStorageService.saveAnswers(userAnswers.value);

    if (currentQuestionPosition.value < totalNumberOfQuestion.value) {
      await loadQuestionByPosition(currentQuestionPosition.value + 1);
    } else {
      await endQuiz();
    }
  }

  async function endQuiz() {
    console.log("Quiz ended");

    const playerName = participationStorageService.getPlayerName();
    const answers = participationStorageService.getAnswers();

    const response = await quizApiService.submitParticipation(playerName, answers);

    if (response && response.data) {
      participationStorageService.saveParticipationScore(response.data.score);
      router.push('/score');
    }
  }
</script>

<template>
  <div class="container">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
    <QuestionDisplay v-if="currentQuestion"
                     :question="currentQuestion"
                     @answer-clicked="answerClickedHandler" />
  </div>
</template>
