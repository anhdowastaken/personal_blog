import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import ChangePassword from '@/components/ChangePassword'
import Post from '@/components/Post'
import PostNew from '@/components/PostNew'
import PostUpdate from '@/components/PostUpdate'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/change_password',
      name: 'ChangePassword',
      component: ChangePassword
    },
    {
      path: '/post/:post_id',
      name: 'Post',
      component: Post,
      props: true
    },
    {
      path: '/post_new',
      name: 'PostNew',
      component: PostNew
    },
    {
      path: '/post_update/:post_id',
      name: 'PostUpdate',
      component: PostUpdate,
      props: true
    }
  ]
})
