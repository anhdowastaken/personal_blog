<template>
  <div class="blog-page area-padding">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 col-lg-offset-4 col-md-4 col-md-offset-4 col-sm-4 col-sm-offset-4 col-xs-12">
          <form class="form-signin">
            <h2 class="form-signin-heading"></h2>
            <label for="inputUsername" class="sr-only">Username</label>
            <input type="username" id="inputUsername" class="form-control" placeholder="username" required autofocus v-model="username">
            <label for="inputPassword" class="sr-only">Password</label>
            <input type="password" id="inputPassword" class="form-control" placeholder="password" required v-model="password">
            <button class="btn btn-primary btn-block"
                    v-on:click.stop.prevent="login()"
                    v-on:submit.stop.prevent="login()"
                    v-bind:disabled="!isHttpRequestCompleted">Login</button>
          </form> 
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
import { submitLogin } from '@/api'

export default {
    name: 'Login',
    data() {
        return {
            username: "",
            password: "",
            isHttpRequestCompleted: true
        }
    },
    methods: {
        ...mapMutations([
            'setJwtToken',
            'setUserData',
            'setNotificationContent',
            'showNotification'
        ]),
        login: function() {
            if (this.username == '' || this.password == '') {
                this.setNotificationContent({ header: 'Error',
                                              body: 'Username and password can\'t be empty' })
                this.showNotification()
            } else {
                this.isHttpRequestCompleted = false
                submitLogin(this.username, this.password)
                    .then(response => {
                        this.isHttpRequestCompleted = true
                        if (response.status === 200) {
                            this.setJwtToken({ jwt: response.data['token'] })
                            this.setUserData({ userData: response.data['user_data'] })
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
        }
    }
}
</script>

<style scoped>
</style>
