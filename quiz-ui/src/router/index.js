import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionsManager from '../components/QuestionsManager.vue'
import ScorePage from '../views/ScorePage.vue'
import Admin from '../views/Admin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: "/new-quiz",
      name: "NewQuizPage",
      component: NewQuizPage,
    },
    {
      path: '/questions',
      name: 'QuestionsManager',
      component: QuestionsManager,
    },
    {
      path: '/score',
      name: 'ScorePage',
      component: ScorePage,
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin,
    },
  ],
})

export default router
