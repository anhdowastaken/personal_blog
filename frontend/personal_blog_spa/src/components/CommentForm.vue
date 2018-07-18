<template>
  <div class="comment-respond">
    <h3 class="comment-reply-title">Leave a Reply </h3>
    <span class="email-notes" v-if="!isAuthenticated">Your email address will not be published. Required fields are marked *</span>
    <form action="#">
      <div class="row">
        <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12"
             v-if="!isAuthenticated">
          <p>Name *</p>
          <input type="text" v-model="author_name"/>
        </div>
        <div class="col-lg-4 col-md-4 col-sm-4 col-xs-12"
             v-if="!isAuthenticated">
          <p>Email *</p>
          <input type="email" v-model="author_email"/>
        </div>
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
          <p>Comment *</p>
          <textarea id="message-box" cols="30" rows="10" v-model="content"></textarea>
          <div class="g-recaptcha" :data-sitekey="rcapt_sig_key"
               v-if="!isAuthenticated"></div>
          <button class="btn btn-primary"
                  v-on:click.stop.prevent="postComment()"
                  v-on:submit.stop.prevent="postComment()"
                  v-bind:disabled="!isHttpRequestCompleted">Post Comment</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapGetters } from 'vuex'
import { mapMutations } from 'vuex'

import { submitComment } from '@/api'
import { isEmpty } from '@/utils'
import { key_jwt, key_user_data } from '@/common'
import { recaptcha_data_sitekey } from '@/common'

export default {
    name: 'Post',
    components: {
    },
    data () {
        return {
            content: '',
            author_name: '',
            author_email: '',
            rcapt_sig_key: recaptcha_data_sitekey,
            rcapt_id: 0,
            isHttpRequestCompleted: true
        }
    },
    props: ['post'],
    mounted() {
        if (!this.isAuthenticated) {
            this.initReCaptcha()
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
            'showNotification'
        ]),
        initReCaptcha: function () {
            setTimeout(() => {
                if (typeof grecaptcha === 'undefined' || typeof grecaptcha.render ==='undefined') {
                    this.initReCaptcha();
                } else {
                    try {
                        this.rcapt_id = grecaptcha.render($('.g-recaptcha')[0], { sitekey : this.rcapt_sig_key });
                    } catch (error) {
                        // FIXME: Error: reCAPTCHA has already been rendered in this element
                        console.log(error)
                    }
                }
            }, 100);
        },
        postComment: function() {
            let recaptcha_response = ''

            if (this.isAuthenticated) {
                this.author_name = this.userData['username']
                this.author_email = this.userData['email']
            } else {
                recaptcha_response = grecaptcha.getResponse(this.rcapt_id);
                if (recaptcha_response.length == 0) {
                    alert("Please complete captcha challenge!")
                    return
                }
            }

            this.isHttpRequestCompleted = false
            submitComment(this.jwt, this.post.post_id, this.content, this.author_name, this.author_email, recaptcha_response)
                .then(response => {
                    this.isHttpRequestCompleted = true
                    if (response.status == 201) {
                        this.author_name = ''
                        this.author_email = ''
                        this.content = ''

                        let comment = response.data['comment']
                        let d = new Date(comment['created_at'] * 1000)
                        comment['created_at'] = d.toLocaleString()
                        this.post.comments.push(comment)
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
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
