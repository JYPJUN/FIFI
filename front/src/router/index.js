import { createRouter, createWebHistory } from 'vue-router'
import { useCustomerStore } from '@/stores/customer'
import HomeView from '@/views/HomeView.vue'
// accounts
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import PasswordChangeView from '@/views/PasswordChangeView.vue'
import ProfileView from '@/views/profile/ProfileView.vue'
import ProfileUpdateView from '@/views/profile/ProfileUpdateView.vue'
import InterestView from '@/views/profile/InterestView.vue'
// Article CRUD
import ArticleView from '@/views/ArticleView.vue'
import TrendArticleView from '@/views/TrendArticleView.vue'
import MyArticleView from '@/views/MyArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import UpdateView from '@/views/UpdateView.vue'
// MAP
import KakaoView from '@/views/KakaoView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
// Product
import ProductView from '@/views/ProductView.vue'
import FinancialCoView from '@/views/product/FinancialCoView.vue'
import TimeDepositView from '@/views/product/TimeDepositView.vue'
import TimeDepositListView from '@/views/product/TimeDepositListView.vue'
import TimeDepositCompareView from '@/views/product/TimeDepositCompareView.vue'
import TimeDepositDetailView from '@/views/product/TimeDepositDetailView.vue'
import SavingView from '@/views/product/SavingView.vue'
import SavingListView from '@/views/product/SavingListView.vue'
import SavingDetailView from '@/views/product/SavingDetailView.vue'
import SavingCompareView from '@/views/product/SavingCompareView.vue'

// RecommendView
import RecommendView from '@/views/product/RecommendView.vue'
import RecommendDepositView from '@/views/product/RecommendDepositView.vue'
import RecommendSavingView from '@/views/product/RecommendSavingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name:'HomeView',
      component: HomeView
    },
    // accounts
    {
      path:'/signup',
      name:'SignUpView',
      component: SignUpView
    },
    {
      path:'/login',
      name:'LogInView',
      component: LogInView
    },
    {
      path:'/password/change',
      name:'PasswordChangeView',
      component: PasswordChangeView
    },
    {
      path:'/profile',
      name:'ProfileView',
      component: ProfileView
    },
    {
      path:'/profile/:id',
      name:'ProfileUpdateView',
      component: ProfileUpdateView
    },
    {
      path:'/interest',
      name:'InterestView',
      component: InterestView
    },
    // article CRUD
    {
      path:'/articles',
      name:'ArticleView',
      component: ArticleView
    },
    {
      path:'/articlebyliked',
      name:'TrendArticleView',
      component: TrendArticleView
    },
    {
      path:'/myarticle',
      name:'MyArticleView',
      component: MyArticleView
    },
    {
      path:'/articles/:id',
      name:'DetailView',
      component: DetailView
    },
    {
      path:'/create',
      name:'CreateView',
      component: CreateView
    },
    {
      path:'/update/:id',
      name:'UpdateView',
      component: UpdateView
    },
    // MAP
    {
      path:'/kakao',
      name:'KakaoView',
      component: KakaoView
    },
    // EXCHANGE
    {
      path:'/exchange',
      name:'ExchangeView',
      component: ExchangeView
    },
    // PRODUCT
    {
      path: '/product',
      name: 'product',
      component: ProductView,
      redirect: '/product/Financial',
      children: [
        { path: 'Financial', name: 'FinancialCoView', component: FinancialCoView },
        { 
          path: '/timedeposit', 
          name: 'TimeDepositView',
          component: TimeDepositView,
          redirect: '/timedeposit/prductlist',
          children: [
            { path: 'prductlist', name: 'TimeDepositListView', component: TimeDepositListView },
            { path: 'compare', name: 'TimeDepositCompareView', component: TimeDepositCompareView },
            { path: '/product/:id', name: 'TimeDepositDetailView', component: TimeDepositDetailView },
          ]
        },
        {
          path: '/saving',
          name: 'SavingView',
          component: SavingView,
          redirect: '/saving/savinglist',
          children: [
            { path: 'savinglist', name: 'SavingListView', component: SavingListView },
            { path: 'compare', name: 'SavingCompareView', component: SavingCompareView },
            { path: '/saving/:id', name: 'SavingDetailView', component: SavingDetailView },
          ]
        },
        // RECOMMEND
        {
          path: '/recommend',
          name: 'RecommendView',
          component: RecommendView,
          redirect: '/recommend/deposit',
          children: [
            { path: 'deposit', name: 'RecommendDepositView', component: RecommendDepositView },
            { path: 'saving', name: 'RecommendSavingView', component: RecommendSavingView },
          ]
        
        },
        
      ]
    },
  ]
})

// 라우터 가드
router.beforeEach(async (to, from, next) => {
  const store = useCustomerStore()

  if ((to.name === 'MyArticleView' || to.name === 'FinancialCoView') && !store.isLoggin) {
    alert('로그인 해주세요.')
    next({ name: 'LogInView' })
  } else if (to.name === 'RecommendDepositView') {
    // 비동기로 프로필 데이터를 로드하고 기다림
    const profile = await store.getProfile()
    if (profile && profile.income === null) {
      alert('연봉을 기입해주세요.')
      next({ name: 'ProfileView' })
    } else {
      next()
    }
  } else {
    next()
  }
})




export default router
