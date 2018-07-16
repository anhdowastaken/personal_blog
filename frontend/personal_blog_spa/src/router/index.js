import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import NewPost from '@/components/NewPost'
import Post from '@/components/Post'
import EditPost from '@/components/EditPost'

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
      path: '/new_post',
      name: 'NewPost',
      component: NewPost
    },
    {
      path: '/post/:post_id',
      name: 'Post',
      component: Post,
      props: true
    },
    {
      path: '/edit_post/:post_id',
      name: 'EditPost',
      component: EditPost,
      props: true
    }
  ]
})
