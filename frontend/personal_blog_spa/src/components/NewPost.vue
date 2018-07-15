<template>
    <div>
        <header-component></header-component>
        <header-image-component></header-image-component>

        <div v-if="isAuthenticated">
        <input type="text" class="form-control" v-model="header">
            <div>
                <quill-editor v-model="body"
                              v-bind:options="config">
                </quill-editor>
            </div>
            <button class="btn btn-lg btn-primary btn-block"
                    v-on:click.stop.prevent="submitNewPost()"
                    v-on:submit.stop.prevent="submitNewPost()"
                    v-bind:disabled="!isHttpRequestCompleted">Submit</button>
        </div>

        <footer-component></footer-component>
    </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'

import HeaderComponent from '@/components/HeaderComponent'
import HeaderImageComponent from '@/components/HeaderImageComponent'
import FooterComponent from '@/components/FooterComponent'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import Back from '@/components/Back'

import { createNewPost } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'NewPost',
    components: {
        HeaderComponent,
        HeaderImageComponent,
        FooterComponent,
        Login,
        Logout,
        Back
    },
    data () {
        return {
            header: '',
            body: 'YEAH! It works!!!',
            config: {
                modules: {
                    toolbar: [
                        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                        ['bold', 'italic', 'underline', 'strike'],
                        ['blockquote', 'code-block'],
                        [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                        [{ 'script': 'sub' }, { 'script': 'super' }],
                        [{ 'indent': '-1' }, { 'indent': '+1' }],
                        [{ 'font': [] }],
                        [{ 'color': [] }, { 'background': [] }],
                        [{ 'align': [] }],
                        // ['link', 'image', 'video'], // FIXME: Enable uploading image
                        ['clean']
                    ]
                }
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
