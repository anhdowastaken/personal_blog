<template>
  <header>
    <!-- header-area start -->
    <div id="sticker" class="header-area">
      <div class="container">
        <div class="row">
          <div class="col-md-12 col-sm-12">

            <!-- Navigation -->
            <nav class="navbar navbar-default">
              <!-- Brand and toggle get grouped for better mobile display -->
              <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".bs-example-navbar-collapse-1" aria-expanded="false">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                </button>
                <!-- Brand -->
                <router-link to="/"
                             class="navbar-brand page-scroll sticky-logo">
                  <h1><span>anh</span>DO</h1>
                </router-link>
              </div>
              <!-- Collect the nav links, forms, and other content for toggling -->
              <div class="collapse navbar-collapse main-menu bs-example-navbar-collapse-1" id="navbar-example">
                <ul class="nav navbar-nav navbar-right">
                  <li class="active">
                    <router-link to="/">Home</router-link>
                  </li>
                  <li>
                    <router-link to="/login"
                                 v-if="!isAuthenticated">login</router-link>
                    <button-logout v-else></button-logout>
                  </li>
                </ul>
              </div>
              <!-- navbar-collapse -->
            </nav>
            <!-- END: Navigation -->
          </div>
        </div>
      </div>
    </div>
    <!-- header-area end -->
  </header>
</template>

<script>
import { mapGetters } from 'vuex'

import ButtonLogout from '@/components/global/ButtonLogout'

export default {
    name: 'HeaderComponent',
    components: {
        ButtonLogout
    },
    data() {
        return {

        }
    },
    computed: {
        ...mapGetters([
            'isAuthenticated',
        ])
    }
}
</script>

<style scoped>
</style>
