<template>
    <div>
        <header-component></header-component>
        <header-image-component></header-image-component>

        <div class="blog-page area-padding">
          <div class="container">
            <div class="row" v-if="isAuthenticated">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                <input type="text"
                       class="form-control"
                       id="newpost-form-title"
                       placeholder="Title"
                       v-model="header">
                <quill-editor id="newpost-form-editor"
                              v-model="body"
                              v-bind:options="config">
                </quill-editor>
                <button class="btn btn-lg btn-primary btn-block"
                        id="newpost-form-button-submit"
                        v-on:click.stop.prevent="submitNewPost()"
                        v-on:submit.stop.prevent="submitNewPost()"
                        v-bind:disabled="!isHttpRequestCompleted">Submit</button>
              </div>
            </div>
          </div>
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

// https://github.com/surmon-china/vue-quill-editor
// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import { quillEditor } from 'vue-quill-editor'

export default {
    name: 'NewPost',
    components: {
        HeaderComponent,
        HeaderImageComponent,
        FooterComponent,
        Login,
        Logout,
        Back,
        quillEditor
    },
    data () {
        return {
            header: '',
            body: '',
            config: {
                modules: {
                    toolbar: {
                        container: [
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
                .then(response => {
                    if (response.status == 201) {
                        this.$router.push('/')
                    }
                })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#newpost-form-title {
    margin-bottom: 20px;
}

.ql-container {
    height: 375px;
}

#newpost-form-button-submit {
    margin-top: 20px;
}
</style>
