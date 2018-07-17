<template>
  <a href="#" class="back-to-top"
     v-on:click.stop.prevent="goToTop()"><i class="fa fa-chevron-up"></i></a>
</template>

<script>
export default {
    name: 'ButtonGoToTop',
    data() {
        return {

        }
    },
    mounted() {
        $(window).scroll(function() {
            if ($(this).scrollTop() > 100) {
                $('.back-to-top').fadeIn('slow');
            } else {
                $('.back-to-top').fadeOut('slow');
            }
        });
    },
    methods: {
        goToTop: function() {
            $('html, body').animate({scrollTop : 0}, 1500);
        }
    }
}
</script>

<style scoped>
</style>
