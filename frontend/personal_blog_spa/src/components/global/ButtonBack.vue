<template>
  <a v-on:click.stop.prevent="goBack">back</a>
</template>

<script>
export default {
    name: 'Back',
    data() {
        return {

        }
    },
    methods: {
        goBack: function() {
            if (window.history.length > 1) {
                this.$router.go(-1)
            } else {
                this.$router.push('/')
            }
        }
    }
}
</script>

<style scoped>
</style>
