<template>
  <div class="comment-respond"
       v-if="isAuthenticated">
    <h3 class="comment-reply-title">Leave a Reply </h3>
    <form action="#">
      <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 comment-form-comment">
          <p>Comment</p>
          <textarea id="message-box" cols="30" rows="10" v-model="content"></textarea>
          <input type="submit" value="Post Comment"
                 v-on:click.stop.prevent="postComment()"
                 v-on:submit.stop.prevent="postComment()"/>
        </div>
      </div>
    </form>
  </div>
  <div class="comment-respond" v-else>
    <h3 class="comment-reply-title">Leave a Reply </h3>
    <span class="email-notes">Your email address will not be published. Required fields are marked *</span>
    <form action="#">
      <div class="row">
        <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
          <p>Name *</p>
          <input type="text" v-model="author_name"/>
        </div>
        <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12">
          <p>Email *</p>
          <input type="email" v-model="author_email"/>
        </div>
        <div class="col-lg-12 col-md-12 col-sm-12 comment-form-comment">
          <p>Comment *</p>
          <textarea id="message-box" cols="30" rows="10" v-model="content"></textarea>
          <input type="submit" value="Post Comment"
                 v-on:click.stop.prevent="postComment()"
                 v-on:submit.stop.prevent="postComment()"/>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'

import { submitComment } from '@/api'
import { isEmpty } from '@/utils'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Post',
    components: {
    },
    data () {
        return {
            content: '',
            author_name: '',
            author_email: '',
            isHttpRequestCompleted: true
        }
    },
    props: ['post'],
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
        postComment: function() {
            if (this.isAuthenticated) {
                this.author_name = this.userData['username']
                this.author_email = this.userData['email']
            }
            submitComment(this.jwt, this.post.post_id, this.content, this.author_name, this.author_email)
                .then(response => {
                    if (response.status == 201) {
                        this.author_name = ''
                        this.author_email = ''
                        this.content = ''

                        let comment = response.data['comment']
                        this.post.comments.push(comment)
                    }
                })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
