<template>
    <div>
        <router-link to="/login" v-if="!isAuthenticated">login</router-link>
        <logout v-else></logout>

        <div v-if="isAuthenticated">
        <input type="text" class="form-control" v-model="header">
            <div>
                <trumbowyg v-model="body"
                           :config="config"
                           class="form-control" name="content"></trumbowyg>
            </div>
            <button class="btn btn-lg btn-primary btn-block"
                    v-on:click.stop.prevent="submitNewPost()"
                    v-on:submit.stop.prevent="submitNewPost()"
                    v-bind:disabled="!isHttpRequestCompleted">Submit</button>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'

import Login from '@/components/Login'
import Logout from '@/components/Logout'

import { createNewPost } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'NewPost',
    components: {
        Login,
        Logout
    },
    data () {
        return {
            header: '',
            body: '<h1>YEAH! It works!!!</h1>',
            config: {
                // Any option from 
                // https://alex-d.github.io/Trumbowyg/documentation/#basic-options
                btns: [
                    ['formatting'],
                    ['strong', 'em', 'del'],
                    ['superscript', 'subscript'],
                    ['link'],
                    ['insertImage'],
                    ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
                    ['unorderedList', 'orderedList'],
                    ['horizontalRule'],
                    ['removeformat'],
                ]
            },
            isHttpRequestCompleted: true
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
        submitNewPost: function() {
            createNewPost(this.jwt, this.header, this.body)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
