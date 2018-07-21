<template>
  <li v-if="comment">
    <div class="comments-details">
      <div class="comments-list-img">
        <img v-bind:src="comment.author_avatar" alt="post-author">
      </div>
      <div class="comments-content-wrap">
        <button type="button" class="close"
                v-if="isAuthenticated"
                v-on:click.stop.prevent="deleteComment()"
                v-bind:disabled="!isHttpRequestCompleted">&times;</button>
        <span>
          <b>{{ comment.author_name }}</b>
          <span class="post-time">{{ comment.created_at }}</span>
        </span>
        <p>{{ comment.content }}</p>
      </div>
    </div>
  </li>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import { submitDeleteComment } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'Comment',
    components: {
    },
    data () {
        return {
            isHttpRequestCompleted: true
        }
    },
    props: {
        comment: {
            type: Object,
            default: undefined
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
            'showNotification',
            'setNotificationRedirectAfterClose'
        ]),
        deleteComment: function() {
            if (confirm('Are you sure?')) {
                this.isHttpRequestCompleted = false
                submitDeleteComment(this.jwt, this.comment.comment_id)
                    .then(response => {
                        this.isHttpRequestCompleted = true
                        if (response.status === 200) {
                            this.$emit('deleteComment')
                        }
                    })
                    .catch(error => {
                        this.isHttpRequestCompleted = true
                        if (error.response.data['message']) {
                            this.setNotificationContent({ header: 'Error',
                                                          body: error.response.data['message'] })
                            this.showNotification()

                            if (error.response.status == 401) {
                                this.setNotificationRedirectAfterClose({ redirect: true,
                                                                         component_name: 'Login' })
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
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.comments-content-wrap p {
  word-wrap: break-word;
}
</style>
