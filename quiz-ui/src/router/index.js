import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionsManager from '../components/QuestionsManager.vue'
import AdminLogin from '../components/AdminLogin.vue'
import AdminQuestionList from '../components/AdminQuestionList.vue'
import AdminQuestionDetail from '../components/AdminQuestionDetail.vue'
import AdminQuestionEdit from '../components/AdminQuestionEdit.vue'
import ScorePage from '../views/ScorePage.vue'


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
      path: '/admin/login',
      name: 'AdminLogin',
      component: AdminLogin,
    },
    {
      path: '/admin/questions',
      name: 'AdminQuestionList',
      component: AdminQuestionList,
    },
    {
      path: '/admin/questions/create',
      name: 'AdminQuestionCreate',
      component: AdminQuestionEdit,
    },
    {
      path: '/admin/questions/:id',
      name: 'AdminQuestionDetail',
      component: AdminQuestionDetail,
    },
    {
      path: '/admin/questions/:id/edit',
      name: 'AdminQuestionEdit',
      component: AdminQuestionEdit,
    },
  ],
})

export default router
