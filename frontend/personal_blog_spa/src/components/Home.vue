<template>
    <div>
        <login v-if="!isAuthenticated"></login>
        <logout v-else></logout>
        <div v-for="post in posts" :key="post.id">
            <h3>{{ post.header }}</h3>
            <p>{{ post.body }}</p>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import Login from '@/components/Login'
import Logout from '@/components/Logout'

import { fetchAllPosts } from '@/api'
import { fetchPublicPosts } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Home',
    components: {
        Login,
        Logout
    },
    data () {
        return {
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
