<template>
  <div class="blog-page area-padding">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
          <div class="page-head-blog">
            <div class="single-blog-page" v-if="isAuthenticated">
              <button type="button"
                      class="btn btn-primary btn-block btn-edit-post"
                      v-on:click.stop.prevent="$router.push({ name: 'PostUpdate', params: { post_id: post_id}})"
                      v-bind:disabled="!isHttpRequestCompleted">Update Post</button>
            </div>
            <div class="single-blog-page" v-if="isAuthenticated">
              <button type="button"
                      class="btn btn-danger btn-block btn-delete-post"
                      v-on:click.stop.prevent="deletePost()"
                      v-bind:disabled="!isHttpRequestCompleted">Delete Post</button>
            </div>
            <left-bar-profile></left-bar-profile>
            <left-bar-search></left-bar-search>
            <left-bar-tags></left-bar-tags>
          </div>
        </div>
        <!-- End left sidebar -->
        <!-- Start single blog -->
        <div class="col-md-8 col-sm-8 col-xs-12">
          <div class="row" v-if="post">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <!-- single-blog start -->
              <article class="blog-post-wrapper">
                <div class="post-information">
                  <h2>{{ post.header }}</h2>
                  <div class="entry-meta">
                    <span class="author-meta"><i class="fa fa-user"></i>{{ post.author_name }}</span>
                    <span><i class="fa fa-clock-o"></i>{{ post.last_edit_at }}</span>
                    <span>
                      <i class="fa fa-tags"></i>
                      <a href="#">life</a>
                    </span>
                    <span v-if="post.comments.length == 1"><i class="fa fa-comments-o"></i>1 comment</span>
                    <span v-else-if="post.comments.length > 1"><i class="fa fa-comments-o"></i>{{ post.comments.length }} comments</span>
                  </div>
                  <!-- <div class="entry-content" v-html="post.body"></div> -->
                  <div class="entry-content">
                    <quill-editor v-model="post.body"
                                    v-bind:options="config"
                                    v-bind:disabled="quillDisabled">
                    </quill-editor>
                    <input-tag v-if="post.tags.length > 0"
                               :read-only="true"
                               :tags.sync="post.tags"></input-tag>
                  </div>
                </div>
              </article>
              <div class="clear"></div>
              <div class="single-post-comments">
                <div class="comments-area" v-if="post.comments.length">
                  <div class="comments-heading">
                    <h3 v-if="post.comments.length == 1">1 comment</h3>
                    <h3 v-else-if="post.comments.length > 1">{{ post.comments.length }} comments</h3>
                  </div>
                  <div class="comments-list">
                    <ul>
                      <comment v-for="(comment, index) in post.comments" :key="comment.id"
                               v-bind:comment="comment"
                               v-on:deleteComment="deleteThisComment(index)"></comment>
                    </ul>
                  </div>
                </div>
                <comment-form v-bind:post="post"></comment-form>
              </div>
              <!-- single-blog end -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import LeftBarProfile from '@/components/LeftBarProfile'
import LeftBarSearch from '@/components/LeftBarSearch'
import LeftBarTags from '@/components/LeftBarTags'
import Comment from '@/components/Comment'
import CommentForm from '@/components/CommentForm'
import InputTag from 'vue-input-tag'

import { fetchPost } from '@/api'
import { submitComment } from '@/api'
import { submitDeletePost } from '@/api'
import { isEmpty } from '@/utils'
import { key_jwt, key_user_data } from '@/common'

// https://github.com/surmon-china/vue-quill-editor
// require styles
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import { quillEditor } from 'vue-quill-editor'

export default {
    name: 'Post',
    components: {
        LeftBarSearch,
        LeftBarTags,
        LeftBarProfile,
        Comment,
        CommentForm,
        quillEditor,
        InputTag
    },
    data () {
        return {
            post: undefined,
            isHttpRequestCompleted: true,
            config: {
                modules: {
                    toolbar: false
                },
                // readOnly: true
            },
            quillDisabled: true
        }
    },
    props: ['post_id'],
    beforeMount() {
        this.$nextTick(() => {
            fetchPost(this.jwt, this.post_id)
                .then(response => {
                    if (response.status === 200) {
                        this.post = response.data
                        let d = new Date(this.post['last_edit_at'] * 1000)
                        this.post['last_edit_at'] = d.toLocaleString()

                        for (let i = 0; i < this.post.comments.length; i++) {
                            let comment = this.post.comments[i]
                            let d = new Date(comment['created_at'] * 1000)
                            comment['created_at'] = d.toLocaleString()
                        }
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
            userData: function(state) {
                if (!isEmpty(state.userData)) {
                    return state.userData
                } else {
                    return JSON.parse(localStorage.getItem(key_user_data))
                }
            }
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
        deletePost: function() {
            if (confirm('Are you sure?')) {
                this.isHttpRequestCompleted = false
                submitDeletePost(this.jwt, this.post_id)
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

                            if (error.response.status == 401) {
                                this.$store.dispatch('logout')
                            }
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
        deleteThisComment: function(index) {
            this.post.comments.splice(index, 1);
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.btn-edit-post {
  margin-bottom: 10px;
}

.btn-delete-post {
  margin-bottom: 30px;
}

.entry-content {
    height: auto;
}

.entry-content .quill-editor .ql-container {
    border: 0;
}

.entry-content .vue-input-tag-wrapper {
    border: none;
}
</style>
