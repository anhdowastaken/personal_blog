<template>
    <div>
        <router-link to="/login" v-if="!isAuthenticated">login</router-link>
        <logout v-else></logout>
        <router-link to="/new_post" v-if="isAuthenticated">new post</router-link>
        <div v-for="post in posts" :key="post.id">
            <router-link :to="{ name: 'Post', params: { post_id: post.post_id }}"><h3>{{ post.header }}</h3></router-link>
        </div>
        <a v-if="has_prev"
           v-on:click.stop.prevent="fetchPosts(prev_num)">&lt;</a>
        <a v-if="has_next"
           v-on:click.stop.prevent="fetchPosts(next_num)">&gt;</a>
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
        this.$nextTick(() => {
            this.fetchPosts(this.currentPage)
        })
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
            posts: state => state.posts,
            currentPage: state => state.currentPage,
            has_next: state => state.has_next,
            has_prev: state => state.has_prev,
            next_num: state => state.next_num,
            prev_num: state => state.prev_num
        }),
        ...mapGetters([
            'isAuthenticated',
        ])
    },
    methods: {
        ...mapMutations([
            'setPosts',
            'setPageInfo'
        ]),
        fetchPosts: function(page) {
            if (this.isAuthenticated) {
                fetchAllPosts(this.jwt, page)
                    .then(response => {
                        if (response.status === 200) {
                            this.setPosts({ posts: response.data['posts'] })
                            this.setPageInfo({ currentPage: page,
                                               has_next: response.data['has_next'],
                                               has_prev: response.data['has_prev'],
                                               next_num: response.data['next_num'],
                                               prev_num: response.data['prev_num']
                                             })
                        }
                    })
            } else {
                fetchPublicPosts(page)
                    .then(response => {
                        if (response.status === 200) {
                            this.setPosts({ posts: response.data['posts'] })
                            this.setPageInfo({ currentPage: page,
                                               has_next: response.data['has_next'],
                                               has_prev: response.data['has_prev'],
                                               next_num: response.data['next_num'],
                                               prev_num: response.data['prev_num']
                                             })
                        }
                    })
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
