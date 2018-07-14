<template>
    <div>
        <router-link to="/login" v-if="!isAuthenticated">login</router-link>
        <logout v-else></logout>
        <router-link to="/new_post" v-if="isAuthenticated">new post</router-link>
        <div v-for="post in posts" :key="post.id">
            <router-link :to="{ name: 'Post', params: { post_id: post.post_id }}"><h3>{{ post.header }}</h3></router-link>
            <!-- <router-link :to="{ name: 'Post', params: { post_id: post.id } }"><h3>{{ post.header }}</h3></router-link> -->
            <!-- <div v-html="post.body"></div> -->
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import Login from '@/components/Login'
import Logout from '@/components/Logout'
import NewPost from '@/components/NewPost'
import Post from '@/components/Post'

import { fetchAllPosts } from '@/api'
import { fetchPublicPosts } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Home',
    components: {
        Login,
        Logout,
        NewPost,
        Post
    },
    data () {
        return {
            isHttpRequestCompleted: true
        }
    },
    beforeMount() {
        if (this.isAuthenticated) {
            fetchAllPosts(this.jwt)
                .then(response => {
                    if (response.status === 200) {
                        let posts = response.data
                        this.setPosts({ posts: posts })
                    }
                })
        } else {
            fetchPublicPosts()
                .then(response => {
                    if (response.status === 200) {
                        let posts = response.data
                        this.setPosts({ posts: posts })
                    }
                })
        }
    },
    computed: {
        ...mapState({
            jwt: function(state) {
                if (state.jwt) {
                    return state.jwt 
                } else {
                    return localStorage.getItem(key_jwt)
                }
            },
            posts: state => state.posts
        }),
        ...mapGetters([
            'isAuthenticated',
        ])
    },
    methods: {
        ...mapMutations([
            'setPosts'
        ])
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
