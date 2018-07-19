<template>
  <div class="blog-page area-padding">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-lg-offset-4 col-md-4 col-md-offset-4 col-sm-4 col-sm-offset-4 col-xs-12">
          <form class="form-change-password">
            <h2 class="form-change-password-heading"></h2>
            <label for="inputOldPassword" class="sr-only">Old Password</label>
            <input type="password" id="inputOldPassword" class="form-control" placeholder="old password" required autofocus v-model="oldPassword">
            <label for="inputNewPassword" class="sr-only">New Password</label>
            <input type="password" id="inputNewPassword" class="form-control" placeholder="new password" required v-model="newPassword">
            <button class="btn btn-primary btn-block"
                    v-on:click.stop.prevent="changePassword()"
                    v-on:submit.stop.prevent="changePassword()"
                    v-bind:disabled="!isHttpRequestCompleted">Change</button>
          </form> 
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex' 
import { mapMutations } from 'vuex'

import { submitChangePassword } from '@/api'
import { key_jwt, key_user_data } from '@/common'

export default {
    name: 'ChangePassword',
    data() {
        return {
            oldPassword: "",
            newPassword: "",
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
            }
        })
    },
    methods: {
        ...mapMutations([
            'setNotificationContent',
            'showNotification'
        ]),
        changePassword: function() {
            if (this.oldPassword == '' || this.newPassword == '') {
                this.setNotificationContent({ header: 'Error',
                                              body: 'Old password and new password can\'t be empty' })
                this.showNotification()
            } else {
                this.isHttpRequestCompleted = false
                submitChangePassword(this.jwt, this.oldPassword, this.newPassword)
                    .then(response => {
                        this.isHttpRequestCompleted = true
                        if (response.status === 200) {
                            this.oldPassword = ''
                            this.newPassword = ''
                            this.setNotificationContent({ header: '',
                                                          body: response.data['message'] })
                            this.showNotification()
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
}
</script>

<style scoped>
.form-change-password {
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;
}
.form-change-password .form-change-password-heading,
.form-change-password .checkbox {
    margin-bottom: 10px;
}
.form-change-password .checkbox {
    font-weight: normal;
}
.form-change-password .form-control {
    position: relative;
    height: auto;
    -webkit-box-sizing: border-box;
       -moz-box-sizing: border-box;
            box-sizing: border-box;
    padding: 10px;
    font-size: 14px;
}
.form-change-password .form-control:focus {
    z-index: 2;
}
.form-change-password input#inputOldPassword {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
}
.form-change-password input#inputNewPassword {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}
</style>
