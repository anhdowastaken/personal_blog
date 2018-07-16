<template>
  <div id="app">
    <notification></notification>
    <router-view/>
  </div>
</template>

<script>
import Notification from '@/components/Notification'

export default {
  name: 'App',
  components: {
    Notification
  },
}
</script>

<style>
</style>
