<template>
  <div class="single-blog-page">
    <div class="left-blog">
      <div class="profile">
        <img :src="avatar">
        <div v-html="profile"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { key_jwt, key_user_data, profile, avatar } from '@/common'

export default {
    name: 'LeftBarProfile',
    data() {
        return {
            profile: profile,
            avatar: avatar
        }
    },
    methods: {

    }
}
</script>

<style scoped>
.profile {
  padding: 20px;
}
.profile img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 10px;
  border-radius: 6px;
}
</style>
