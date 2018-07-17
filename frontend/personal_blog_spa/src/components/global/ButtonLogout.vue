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
            'setPosts',
            'setPageInfo'
        ]),
        logout: function() {
            this.$store.dispatch('logout')
                .then(() => {
                    let page = 1
                    if (this.$router.currentRoute['name'] == 'Home') {
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
                    } else {
                        this.$router.push('/')
                    }
                })
        }
    }
}
</script>

<style scoped>
</style>
