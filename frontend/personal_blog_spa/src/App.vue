<template>
  <div id="app">
    <notification></notification>

    <!-- <preloader></preloader> -->
    <the-header></the-header>
    <the-header-image></the-header-image>

    <router-view :key="$route.fullPath"/>

    <the-footer></the-footer>
    <button-go-to-top></button-go-to-top>
  </div>
</template>

<script>
import Notification from '@/components/global/Notification'
// import Preloader from '@/components/global/Preloader'
import TheHeader from '@/components/global/TheHeader'
import TheHeaderImage from '@/components/global/TheHeaderImage'
import TheFooter from '@/components/global/TheFooter'
import ButtonGoToTop from '@/components/global/ButtonGoToTop'

export default {
  name: 'App',
  components: {
    Notification,
    // Preloader,
    TheHeader,
    TheHeaderImage,
    TheFooter,
    ButtonGoToTop
  },
  mounted() {
    // Stick menu on top
    var s = $("#sticker");
    var pos = s.position();
    $(window).on('scroll', function() {
      var windowpos = $(window).scrollTop() > 100;
      if (windowpos > pos.top) {
        s.addClass("stick");
      } else {
        s.removeClass("stick");
      }
    });

    new WOW().init();
  }
}
</script>

<style>
</style>
