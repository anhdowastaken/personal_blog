<template>
    <div id="form-logout">
        <div class="button-logout" v-on:click.stop.prevent="logout()">logout <span class="fa fa-sign-out"></span></div>
    </div>
</template>

<script>
export default {
    name: 'Logout',
    data() {
        return {

        }
    },
    methods: {
        logout: function() {
            this.$store.dispatch('logout')
        }
    }
}
</script>

<style scoped>
</style>
