<template>
    <div id="form-logout">
        <a class="button-logout" v-on:click.stop.prevent="logout()">logout</span></a>
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
