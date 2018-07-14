<template>
    <div>
        <router-link to="/login" v-if="!isAuthenticated">login</router-link>
        <logout v-else></logout>
        <router-link to="/new_post" v-if="isAuthenticated">new post</router-link>
        <back></back>

        <div v-if="post">
            <h3>{{ post.header }}</h3>
            <div v-html="post.body"></div>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import Login from '@/components/Login'
import Logout from '@/components/Logout'
import Back from '@/components/Back'

import { fetchPost } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Post',
    components: {
        Login,
        Logout,
        Back
    },
    data () {
        return {
            post: undefined,
            isHttpRequestCompleted: true
        }
    },
    props: ['post_id'],
    beforeMount() {
        fetchPost(this.jwt, this.post_id)
            .then(response => {
                if (response.status === 200) {
                    this.post = response.data
                }
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
        }),
        ...mapGetters([
            'isAuthenticated',
        ])
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
