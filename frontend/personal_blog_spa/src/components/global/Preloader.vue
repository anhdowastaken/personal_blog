<template>
  <div id="preloader"></div>
</template>

<script>
export default {
    name: 'Back',
    data() {
        return {

        }
    },
    mounted() {
        $(window).on('load', function() {
            var pre_loader = $('#preloader');
            pre_loader.fadeOut('slow', function() {
                $(this).remove();
            });
        });
    },
    methods: {

    }
}
</script>

<style scoped>
</style>
