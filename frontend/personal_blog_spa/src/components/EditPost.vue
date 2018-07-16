<template>
    <div>
        <header-component></header-component>
        <header-image-component></header-image-component>

        <div class="blog-page area-padding">
          <div class="container">
            <div class="row" v-if="isAuthenticated && post">
              <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                <input type="text"
                       class="form-control"
                       id="newpost-form-title"
                       placeholder="Title"
                       v-model="post.header">

                <quill-editor id="newpost-form-editor"
                              v-model="post.body"
                              v-bind:options="config">
                </quill-editor>

                <div>
                  <label>Private</label>
                  <label class="switch">
                    <input type="checkbox" v-model="post.private_post">
                    <span class="slider round"></span>
                  </label>
                </div>

                <div>
                  <button class="btn btn-primary"
                          id="newpost-form-button-submit"
                          v-on:click.stop.prevent="updatePost()"
                          v-on:submit.stop.prevent="updatePost()"
                          v-bind:disabled="!isHttpRequestCompleted">Submit</button>
                  <button class="btn btn-danger"
                          id="newpost-form-button-discard"
                          v-on:click.stop.prevent="discardUpdatePost()"
                          v-bind:disabled="!isHttpRequestCompleted">Discard</button>
                </div>
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
import { mapMutations } from 'vuex'

import HeaderComponent from '@/components/HeaderComponent'
import HeaderImageComponent from '@/components/HeaderImageComponent'
import FooterComponent from '@/components/FooterComponent'
import Login from '@/components/Login'
import Logout from '@/components/Logout'

import { fetchPost } from '@/api'
import { submitUpdatePost } from '@/api'
import { key_jwt, key_user_data } from '@/common'

// https://github.com/surmon-china/vue-quill-editor
// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import { quillEditor } from 'vue-quill-editor'

export default {
    name: 'EditPost',
    components: {
        HeaderComponent,
        HeaderImageComponent,
        FooterComponent,
        Login,
        Logout,
        quillEditor
    },
    props: ['post_id'],
    data () {
        return {
            post: undefined,
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
    beforeMount() {
        this.$nextTick(() => {
            fetchPost(this.jwt, this.post_id)
                .then(response => {
                    if (response.status === 200) {
                        this.post = response.data
                    }
                })
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
            posts: state => state.posts
        }),
        ...mapGetters([
            'isAuthenticated',
        ])
    },
    methods: {
        ...mapMutations([
            'setNotificationContent',
            'showNotification'
        ]),
        updatePost: function() {
            if (this.post.header == '') {
                this.setNotificationContent({ header: 'Error',
                                              body: 'Title can\'t be empty' })
                this.showNotification()
            } else {
                this.isHttpRequestCompleted = false
                submitUpdatePost(this.jwt, this.post.post_id, this.post.header, this.post.body, this.post.private_post)
                    .then(response => {
                        this.isHttpRequestCompleted = true
                        if (response.status === 200) {
                            this.$router.push({ name: "Home" })
                        }
                    })
                    .catch(error => {
                        this.isHttpRequestCompleted = true
                        if (error.response.data['message']) {
                            this.setNotificationContent({ header: 'Error',
                                                          body: error.response.data['message'] })
                            this.showNotification()
                        } else if (error) {
                            this.setNotificationContent({ header: 'Error',
                                                          body: 'Error Authenticating: ' + error })
                            this.showNotification()
                        } else {
                            this.setNotificationContent({ header: 'Error',
                                                          body: 'Error' })
                            this.showNotification()
                        }
                    })
            }
        },
        discardUpdatePost: function() {
            if (confirm('Are you sure?')) {
                this.$router.push('/')
            }
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

#newpost-form-button-submit,
#newpost-form-button-discard {
    margin-top: 20px;
}

/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
  margin-top: 20px;
}

/* Hide default HTML checkbox */
.switch input {display:none;}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>
