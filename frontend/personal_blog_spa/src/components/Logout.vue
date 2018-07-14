<template>
    <a class="button-logout" v-on:click.stop.prevent="logout()">logout</span></a>
</template>

<script>
import { mapMutations } from 'vuex'

import { fetchPublicPosts } from '@/api'

export default {
    name: 'Logout',
    data() {
        return {

        }
    },
    methods: {
        ...mapMutations([
            'setPosts'
        ]),
        logout: function() {
            this.$store.dispatch('logout')
                .then(() => {
                    window.location = '/'
                    // FIXME: How to fetch when come back to home?
                    // fetchPublicPosts()
                    //     .then(response => {
                    //         if (response.status === 200) {
                    //             let posts = response.data
                    //             this.setPosts({ posts: posts })
                    //         }
                    //         this.$router.push({ name: 'Home' })
                    //     })
                })
        }
    }
}
</script>

<style scoped>
</style>
