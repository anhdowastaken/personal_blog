<template>
  <div id="app">
    <notification></notification>

    <the-header></the-header>
    <the-header-image></the-header-image>

    <router-view/>

    <the-footer></the-footer>
    <button-go-to-top></button-go-to-top>
  </div>
</template>

<script>
import Notification from '@/components/global/Notification'
import TheHeader from '@/components/global/TheHeader'
import TheHeaderImage from '@/components/global/TheHeaderImage'
import TheFooter from '@/components/global/TheFooter'
import ButtonGoToTop from '@/components/global/ButtonGoToTop'

export default {
  name: 'App',
  components: {
    Notification,
    TheHeader,
    TheHeaderImage,
    TheFooter,
    ButtonGoToTop
  },
}
</script>

<style>
</style>
