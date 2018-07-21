import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store/index.js'
import Home from '@/components/Home'
import Login from '@/components/Login'
import ChangePassword from '@/components/ChangePassword'
import Post from '@/components/Post'
import PostNew from '@/components/PostNew'
import PostUpdate from '@/components/PostUpdate'
import Tag from '@/components/Tag'

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
      component: Login,
      beforeEnter(to, from, next) {
        if (!store.getters.isAuthenticated) {
          next()
        } else {
          next('/')
        }
      }
    },
    {
      path: '/change_password',
      name: 'ChangePassword',
      component: ChangePassword,
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          next()
        } else {
          next('/')
        }
      }
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
      component: PostNew,
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          next()
        } else {
          next('/')
        }
      }
    },
    {
      path: '/post_update/:post_id',
      name: 'PostUpdate',
      component: PostUpdate,
      props: true,
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          next()
        } else {
          next('/')
        }
      }
    },
    {
      path: '/tag/:tag_id',
      name: 'Tag',
      component: Tag,
      props: true
    }
  ]
})
